"""Validate DAV OCR output against trusted DAV registry metadata.

This does not certify OCR as medically safe. It creates an audit layer so OCR
chunks can be filtered, reviewed, and treated as unverified evidence.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, Iterable, List

from extract_dav_pdf_chunks import repair_mojibake


NUMERIC_UNIT_RE = re.compile(
    r"\b\d+(?:[,.]\d+)?\s*(?:mg|g|mcg|µg|ug|kg|ml|mL|%|giờ|gio|ngày|ngay|tuổi|tuoi|lần|lan|viên|vien)\b",
    re.I,
)


HIGH_RISK_TERMS = [
    "liều",
    "liều dùng",
    "quá liều",
    "chống chỉ định",
    "cảnh báo",
    "thận trọng",
    "tương tác",
    "tác dụng không mong muốn",
    "trẻ em",
    "phụ nữ có thai",
    "cho con bú",
    "suy gan",
    "suy thận",
]


def read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def strip_accents(value: str) -> str:
    value = repair_mojibake(value or "")
    text = unicodedata.normalize("NFD", value or "")
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"[^a-zA-Z0-9%.,]+", " ", text)
    return " ".join(text.lower().split())


def split_ingredients(value: str) -> List[str]:
    parts = re.split(r"[;,+/]| và | va | and ", value or "", flags=re.I)
    cleaned = []
    for part in parts:
        text = re.sub(r"\b(bp|usp|ep|hydrochloride|hydroclorid|hydrochlorid)\b", "", strip_accents(part))
        text = re.sub(r"\b\d+(?:[,.]\d+)?\s*(?:mg|g|mcg|µg|ug|%)\b", "", text, flags=re.I)
        text = " ".join(token for token in text.split() if len(token) > 2)
        if text:
            cleaned.append(text)
    return cleaned


def numeric_units(value: str) -> List[str]:
    value = repair_mojibake(value or "")
    return sorted({re.sub(r"\s+", "", match.group(0).lower().replace(",", ".")) for match in NUMERIC_UNIT_RE.finditer(value or "")})


def contains_any(text_norm: str, terms: List[str]) -> bool:
    return any(strip_accents(term) in text_norm for term in terms)


def load_registry(path: Path) -> Dict[str, Dict[str, Any]]:
    return {
        str(row.get("registration_number")): row
        for row in read_jsonl(path)
        if row.get("registration_number")
    }


def validate_doc(doc: Dict[str, Any], registry: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    reg = str(doc.get("registration_number") or "")
    trusted = registry.get(reg, {})
    text = "\n".join(page.get("text") or "" for page in doc.get("pages") or [])
    text = repair_mojibake(text)
    text_norm = strip_accents(text)

    expected_ingredients = split_ingredients(str(trusted.get("active_ingredient") or ""))
    found_ingredients = [item for item in expected_ingredients if item and item in text_norm]
    missing_ingredients = [item for item in expected_ingredients if item and item not in text_norm]

    expected_strength_units = numeric_units(str(trusted.get("strength") or ""))
    text_units = numeric_units(text)
    found_strength_units = [item for item in expected_strength_units if item in text_units]
    missing_strength_units = [item for item in expected_strength_units if item not in text_units]

    flags = ["ocr_unverified"]
    if missing_ingredients:
        flags.append("ingredient_mismatch")
    if missing_strength_units:
        flags.append("strength_unit_not_found")
    if text_units:
        flags.append("numeric_risk")
    if contains_any(text_norm, HIGH_RISK_TERMS):
        flags.append("medical_high_risk_terms")

    validation_status = "needs_review" if set(flags) - {"ocr_unverified"} else "metadata_aligned"
    if "ingredient_mismatch" in flags or "strength_unit_not_found" in flags:
        validation_status = "needs_review"

    return {
        "registration_number": reg,
        "drug_name": doc.get("drug_name"),
        "document_type": doc.get("document_type"),
        "local_path": doc.get("local_path"),
        "source_url": doc.get("url"),
        "ocr_engine": doc.get("ocr_engine"),
        "ocr_language": doc.get("ocr_language"),
        "total_text_chars": doc.get("total_text_chars", 0),
        "registry_active_ingredient": trusted.get("active_ingredient"),
        "registry_strength": trusted.get("strength"),
        "expected_ingredients": expected_ingredients,
        "found_ingredients": found_ingredients,
        "missing_ingredients": missing_ingredients,
        "expected_strength_units": expected_strength_units,
        "found_strength_units": found_strength_units,
        "missing_strength_units": missing_strength_units,
        "ocr_numeric_units_sample": text_units[:40],
        "flags": flags,
        "validation_status": validation_status,
        "requires_human_review": validation_status == "needs_review",
    }


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "registration_number",
        "drug_name",
        "document_type",
        "validation_status",
        "requires_human_review",
        "registry_active_ingredient",
        "registry_strength",
        "missing_ingredients",
        "missing_strength_units",
        "flags",
        "local_path",
        "source_url",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            flattened = dict(row)
            for key in ["missing_ingredients", "missing_strength_units", "flags"]:
                flattened[key] = "; ".join(str(item) for item in row.get(key) or [])
            writer.writerow(flattened)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default="data/processed/dav_otc_drugs.jsonl")
    parser.add_argument("--ocr", default="data/processed/dav_otc_pdf_ocr_text.jsonl")
    parser.add_argument("--output", default="data/processed/dav_otc_ocr_validation.jsonl")
    parser.add_argument("--csv-output", default="data/processed/dav_otc_ocr_validation.csv")
    args = parser.parse_args()

    registry = load_registry(Path(args.registry))
    rows = [validate_doc(doc, registry) for doc in read_jsonl(Path(args.ocr))]
    write_jsonl(Path(args.output), rows)
    write_csv(Path(args.csv_output), rows)

    total = len(rows)
    needs_review = sum(1 for row in rows if row["requires_human_review"])
    print(f"validated {total} OCR docs")
    print(f"needs_review={needs_review} metadata_aligned={total - needs_review}")
    print(f"saved {args.output} and {args.csv_output}")


if __name__ == "__main__":
    main()
