"""Rebuild normalized DAV processed files from raw API JSONL.

Use this when raw DAV data is already collected and processed text needs to be
regenerated with clean Vietnamese encoding.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


def read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


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
        "active_ingredient": basic.get("hoatChatChinh") or item.get("hoatChatChinh") or item.get("tenHoatChatChinh"),
        "strength": basic.get("hamLuong") or item.get("hamLuong"),
        "dosage_form": basic.get("dangBaoChe") or item.get("dangBaoChe"),
        "packaging": basic.get("dongGoi") or item.get("dongGoi"),
        "route": basic.get("tenDuongDung"),
        "quality_standard": basic.get("tieuChuan") or item.get("tieuChuan"),
        "shelf_life_months": basic.get("tuoiTho") or item.get("tuoiTho"),
        "drug_type_id": basic.get("loaiThuocId") or item.get("thongTinThuocCoBan_LoaiThuocId"),
        "drug_group_id": basic.get("nhomThuocId") or item.get("thongTinThuocCoBan_NhomThuocId"),
        "decision_number": registration.get("soQuyetDinh") or item.get("soQuyetDinh"),
        "registration_date": registration.get("ngayCapSoDangKy") or item.get("ngayCapSoDangKy"),
        "expiry_date": registration.get("ngayHetHanSoDangKy"),
        "batch_round": registration.get("dotCap") or item.get("dotCap"),
        "is_revoked": item.get("isDaRutSoDangKy"),
        "manufacturer_name": manufacturer.get("tenCongTySanXuat") or item.get("tenCongTySanXuat"),
        "manufacturer_country": manufacturer.get("nuocSanXuat") or item.get("nuocSanXuat"),
        "manufacturer_address": manufacturer.get("diaChiSanXuat") or item.get("diaChiSanXuat"),
        "registrant_name": registrant.get("tenCongTyDangKy") or item.get("tenCongTyDangKy"),
        "registrant_country": registrant.get("nuocDangKy") or item.get("nuocDangKy"),
        "registrant_address": registrant.get("diaChiDangKy") or item.get("diaChiDangKy"),
        "label_url": documents.get("urlNhan"),
        "leaflet_url": documents.get("urlHuongDanSuDung"),
        "label_leaflet_url": documents.get("urlNhanVaHDSD"),
        "raw_document_json": documents.get("jsonTaiLieuTCCL"),
    }


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=["otc", "all"], default="otc")
    parser.add_argument("--raw", default=None)
    parser.add_argument("--output-base", default=None)
    args = parser.parse_args()

    raw_path = Path(args.raw or f"data/raw/dav/{args.dataset}_raw.jsonl")
    output_base = args.output_base or f"data/processed/dav_{args.dataset}_drugs"
    rows = [normalize_item(item, args.dataset) for item in read_jsonl(raw_path)]
    write_jsonl(Path(f"{output_base}.jsonl"), rows)
    write_csv(Path(f"{output_base}.csv"), rows)
    print(f"rebuilt {len(rows)} rows from {raw_path} -> {output_base}.jsonl/.csv")


if __name__ == "__main__":
    main()
