"""Collect public drug registration data from DAV.

This script uses the same public JSON endpoint as the DAV search page. It stores
raw JSONL plus a normalized JSONL/CSV suitable for RAG preprocessing.
"""
from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urljoin
from urllib.request import Request, urlopen


BASE_URL = "https://dichvucong.dav.gov.vn"
SEARCH_ENDPOINT = f"{BASE_URL}/api/services/app/soDangKy/GetAllPublicServerPaging"


def post_json(url: str, payload: Dict[str, Any], timeout: int = 60) -> Dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "RAG_BOT_NLP_Project/1.0 (+educational data collection)",
        },
        method="POST",
    )
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def safe_get(data: Dict[str, Any], *path: str) -> Any:
    value: Any = data
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def build_payload(dataset: str, skip: int, page_size: int, query: str = "") -> Dict[str, Any]:
    filters: Dict[str, Any] = {}
    if dataset == "otc":
        filters["thongTinThuocCoBan_LoaiThuocId"] = 1

    return {
        "filterText": query,
        "SoDangKyThuoc": filters,
        "KichHoat": True,
        "skipCount": skip,
        "maxResultCount": page_size,
        "sorting": None,
    }


def normalize_item(item: Dict[str, Any], dataset: str) -> Dict[str, Any]:
    basic = item.get("thongTinThuocCoBan") or {}
    registration = item.get("thongTinDangKyThuoc") or {}
    documents = item.get("thongTinTaiLieu") or {}
    manufacturer = item.get("congTySanXuat") or {}
    registrant = item.get("congTyDangKy") or {}

    return {
        "source_dataset": f"dav_{dataset}",
        "source_url": "https://dichvucong.dav.gov.vn/congbothuockhongkedon/index"
        if dataset == "otc"
        else "https://dichvucong.dav.gov.vn/congbothuoc/index",
        "dav_id": item.get("id"),
        "drug_name": item.get("tenThuoc"),
        "registration_number": item.get("soDangKy"),
        "old_registration_number": item.get("soDangKyCu"),
        "active_ingredient": basic.get("hoatChatChinh"),
        "strength": basic.get("hamLuong"),
        "dosage_form": basic.get("dangBaoChe"),
        "packaging": basic.get("dongGoi"),
        "route": basic.get("tenDuongDung"),
        "quality_standard": basic.get("tieuChuan"),
        "shelf_life_months": basic.get("tuoiTho"),
        "drug_type_id": basic.get("loaiThuocId"),
        "drug_group_id": basic.get("nhomThuocId"),
        "decision_number": registration.get("soQuyetDinh"),
        "registration_date": registration.get("ngayCapSoDangKy"),
        "expiry_date": registration.get("ngayHetHanSoDangKy"),
        "batch_round": registration.get("dotCap"),
        "is_revoked": item.get("isDaRutSoDangKy"),
        "manufacturer_name": manufacturer.get("tenCongTySanXuat"),
        "manufacturer_country": manufacturer.get("nuocSanXuat"),
        "manufacturer_address": manufacturer.get("diaChiSanXuat"),
        "registrant_name": registrant.get("tenCongTyDangKy"),
        "registrant_country": registrant.get("nuocDangKy"),
        "registrant_address": registrant.get("diaChiDangKy"),
        "label_url": documents.get("urlNhan"),
        "leaflet_url": documents.get("urlHuongDanSuDung"),
        "label_leaflet_url": documents.get("urlNhanVaHDSD"),
        "raw_document_json": documents.get("jsonTaiLieuTCCL"),
    }


def iter_document_urls(row: Dict[str, Any]) -> Iterable[str]:
    for key in ("label_url", "leaflet_url", "label_leaflet_url"):
        value = row.get(key)
        if value:
            yield urljoin(BASE_URL, str(value))


def download_documents(rows: List[Dict[str, Any]], output_dir: Path, delay: float) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for row in rows:
        reg = (row.get("registration_number") or str(row.get("dav_id")) or "unknown").replace("/", "_")
        for index, url in enumerate(iter_document_urls(row), 1):
            suffix = Path(url.split("?")[0]).suffix or ".pdf"
            target = output_dir / f"{reg}_{index}{suffix}"
            if target.exists():
                continue
            try:
                request = Request(url, headers={"User-Agent": "RAG_BOT_NLP_Project/1.0"})
                with urlopen(request, timeout=60) as response:
                    target.write_bytes(response.read())
                row.setdefault("downloaded_documents", []).append(str(target))
                time.sleep(delay)
            except Exception as exc:
                row.setdefault("document_download_errors", []).append({"url": url, "error": str(exc)})


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def collect(dataset: str, page_size: int, max_pages: Optional[int], delay: float, query: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    raw_rows: List[Dict[str, Any]] = []
    total_count: Optional[int] = None
    page = 0

    while True:
        if max_pages is not None and page >= max_pages:
            break

        skip = page * page_size
        payload = build_payload(dataset, skip, page_size, query=query)
        response = post_json(SEARCH_ENDPOINT, payload)
        result = response.get("result") or {}
        total_count = result.get("totalCount", total_count)
        items = result.get("items") or []

        print(f"page={page + 1} skip={skip} items={len(items)} total={total_count}")
        raw_rows.extend(items)
        rows.extend(normalize_item(item, dataset) for item in items)

        if not items or (total_count is not None and len(rows) >= total_count):
            break
        page += 1
        time.sleep(delay)

    write_jsonl(Path(f"data/raw/dav/{dataset}_raw.jsonl"), raw_rows)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=["otc", "all"], default="otc")
    parser.add_argument("--page-size", type=int, default=500)
    parser.add_argument("--max-pages", type=int, default=None)
    parser.add_argument("--delay", type=float, default=0.4)
    parser.add_argument("--query", default="")
    parser.add_argument("--download-docs", action="store_true")
    args = parser.parse_args()

    rows = collect(args.dataset, args.page_size, args.max_pages, args.delay, args.query)
    if args.download_docs:
        download_documents(rows, Path("data/raw/documents/dav"), args.delay)

    output_base = f"data/processed/dav_{args.dataset}_drugs"
    write_jsonl(Path(f"{output_base}.jsonl"), rows)
    write_csv(Path(f"{output_base}.csv"), rows)
    print(f"saved {len(rows)} normalized rows to {output_base}.jsonl/.csv")


if __name__ == "__main__":
    main()

