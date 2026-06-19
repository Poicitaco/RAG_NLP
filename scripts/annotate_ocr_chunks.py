"""Attach OCR validation metadata to OCR chunks."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable


def read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> int:
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunks", default="data/chunks/dav_otc_pdf_ocr_chunks.jsonl")
    parser.add_argument("--validation", default="data/processed/dav_otc_ocr_validation.jsonl")
    args = parser.parse_args()

    validation = {
        (row.get("registration_number"), row.get("document_type")): row
        for row in read_jsonl(Path(args.validation))
    }

    annotated = []
    for chunk in read_jsonl(Path(args.chunks)):
        metadata = chunk.setdefault("metadata", {})
        key = (metadata.get("registration_number"), metadata.get("document_type"))
        audit = validation.get(key, {})
        metadata["trust_level"] = "unverified_ocr"
        metadata["requires_human_review"] = True
        metadata["validation_status"] = audit.get("validation_status", "needs_review")
        metadata["validation_flags"] = audit.get("flags", ["ocr_unverified"])
        metadata["registry_active_ingredient"] = audit.get("registry_active_ingredient")
        metadata["registry_strength"] = audit.get("registry_strength")
        annotated.append(chunk)

    count = write_jsonl(Path(args.chunks), annotated)
    print(f"annotated {count} OCR chunks with validation metadata")


if __name__ == "__main__":
    main()
