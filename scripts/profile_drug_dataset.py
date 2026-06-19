"""Profile normalized drug JSONL files for NLP/RAG reporting."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


CORE_FIELDS = [
    "drug_name",
    "registration_number",
    "active_ingredient",
    "strength",
    "dosage_form",
    "packaging",
    "decision_number",
    "registration_date",
    "expiry_date",
    "manufacturer_name",
    "manufacturer_country",
]


def read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def present(value: Any) -> bool:
    return value is not None and str(value).strip() != ""


def top_values(rows: List[Dict[str, Any]], field: str, limit: int = 20) -> List[Dict[str, Any]]:
    counter = Counter(str(row.get(field)).strip() for row in rows if present(row.get(field)))
    return [{"value": value, "count": count} for value, count in counter.most_common(limit)]


def profile(path: Path) -> Dict[str, Any]:
    rows = list(read_jsonl(path))
    total = len(rows)
    missing = {
        field: {
            "missing": sum(1 for row in rows if not present(row.get(field))),
            "coverage": round(
                (
                    (total - sum(1 for row in rows if not present(row.get(field)))) / total
                    if total
                    else 0.0
                ),
                4,
            ),
        }
        for field in CORE_FIELDS
    }

    doc_fields = ["leaflet_url", "label_url", "label_leaflet_url", "raw_document_json"]
    doc_coverage = {
        field: sum(1 for row in rows if present(row.get(field)))
        for field in doc_fields
    }
    any_document = sum(1 for row in rows if any(present(row.get(field)) for field in doc_fields))

    return {
        "input_file": str(path),
        "total_rows": total,
        "unique_registration_numbers": len(
            {row.get("registration_number") for row in rows if present(row.get("registration_number"))}
        ),
        "unique_drug_names": len({row.get("drug_name") for row in rows if present(row.get("drug_name"))}),
        "unique_active_ingredients": len(
            {row.get("active_ingredient") for row in rows if present(row.get("active_ingredient"))}
        ),
        "document_coverage": {
            **doc_coverage,
            "any_document": any_document,
            "any_document_rate": round(any_document / total if total else 0.0, 4),
        },
        "missing_fields": missing,
        "top_active_ingredients": top_values(rows, "active_ingredient"),
        "top_dosage_forms": top_values(rows, "dosage_form"),
        "top_manufacturer_countries": top_values(rows, "manufacturer_country"),
    }


def write_markdown(report: Dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Drug Dataset Profile",
        "",
        f"Input file: `{report['input_file']}`",
        f"Total rows: **{report['total_rows']}**",
        f"Unique registration numbers: **{report['unique_registration_numbers']}**",
        f"Unique drug names: **{report['unique_drug_names']}**",
        f"Unique active ingredients: **{report['unique_active_ingredients']}**",
        "",
        "## Document Coverage",
        "",
    ]
    for key, value in report["document_coverage"].items():
        lines.append(f"- `{key}`: {value}")

    lines.extend(["", "## Field Coverage", ""])
    for field, stats in report["missing_fields"].items():
        lines.append(f"- `{field}`: coverage {stats['coverage']}, missing {stats['missing']}")

    for section, key in [
        ("Top Active Ingredients", "top_active_ingredients"),
        ("Top Dosage Forms", "top_dosage_forms"),
        ("Top Manufacturer Countries", "top_manufacturer_countries"),
    ]:
        lines.extend(["", f"## {section}", ""])
        for item in report[key]:
            lines.append(f"- {item['value']}: {item['count']}")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/processed/dav_otc_drugs.jsonl")
    parser.add_argument("--json-output", default="data/processed/dav_otc_profile.json")
    parser.add_argument("--md-output", default="data/processed/dav_otc_profile.md")
    args = parser.parse_args()

    report = profile(Path(args.input))
    json_path = Path(args.json_output)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(report, Path(args.md_output))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
