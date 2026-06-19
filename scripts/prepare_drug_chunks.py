"""Prepare structured DAV drug rows as RAG chunks."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


def read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def make_chunk(row: Dict[str, Any], section: str, text: str) -> Dict[str, Any]:
    source_id = clean(row.get("registration_number")) or clean(row.get("dav_id"))
    return {
        "id": f"{source_id}:{section}",
        "document": text,
        "metadata": {
            "source": row.get("source_dataset"),
            "source_url": row.get("source_url"),
            "section": section,
            "drug_name": row.get("drug_name"),
            "active_ingredient": row.get("active_ingredient"),
            "registration_number": row.get("registration_number"),
            "decision_number": row.get("decision_number"),
            "updated_at": row.get("registration_date"),
            "type": "drug_info",
            "otc_status": "otc" if row.get("source_dataset") == "dav_otc" else "unknown",
        },
    }


def row_to_chunks(row: Dict[str, Any]) -> List[Dict[str, Any]]:
    name = clean(row.get("drug_name"))
    active = clean(row.get("active_ingredient"))
    strength = clean(row.get("strength"))
    form = clean(row.get("dosage_form"))
    reg = clean(row.get("registration_number"))

    identity = (
        f"Tên thuốc: {name}. Số đăng ký/GPLH: {reg}. "
        f"Hoạt chất chính: {active}. Hàm lượng: {strength}. "
        f"Dạng bào chế: {form}. Quy cách đóng gói: {clean(row.get('packaging'))}."
    )
    registration = (
        f"Thuốc {name} được ghi nhận trong dữ liệu DAV. "
        f"Số quyết định: {clean(row.get('decision_number'))}. "
        f"Ngày cấp: {clean(row.get('registration_date'))}. "
        f"Ngày hết hạn: {clean(row.get('expiry_date'))}. "
        f"Trạng thái thu hồi: {clean(row.get('is_revoked'))}."
    )
    manufacturer = (
        f"Thông tin sản xuất/đăng ký của {name}: "
        f"Cơ sở sản xuất: {clean(row.get('manufacturer_name'))}, "
        f"nước sản xuất: {clean(row.get('manufacturer_country'))}. "
        f"Công ty đăng ký: {clean(row.get('registrant_name'))}, "
        f"nước đăng ký: {clean(row.get('registrant_country'))}."
    )

    chunks = [
        make_chunk(row, "identity", identity),
        make_chunk(row, "registration", registration),
        make_chunk(row, "manufacturer", manufacturer),
    ]

    doc_urls = [
        clean(row.get("leaflet_url")),
        clean(row.get("label_url")),
        clean(row.get("label_leaflet_url")),
    ]
    doc_urls = [url for url in doc_urls if url]
    if doc_urls:
        chunks.append(
            make_chunk(
                row,
                "documents",
                f"Thuốc {name} có tài liệu nhãn/HDSD từ DAV: " + "; ".join(doc_urls),
            )
        )

    return [chunk for chunk in chunks if chunk["document"].strip()]


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/processed/dav_otc_drugs.jsonl")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else Path("data/chunks") / f"{input_path.stem}_chunks.jsonl"

    chunks: List[Dict[str, Any]] = []
    for row in read_jsonl(input_path):
        chunks.extend(row_to_chunks(row))

    count = write_jsonl(output_path, chunks)
    print(f"saved {count} chunks to {output_path}")


if __name__ == "__main__":
    main()

