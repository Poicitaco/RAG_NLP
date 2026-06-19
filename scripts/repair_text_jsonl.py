"""Repair mojibake in JSONL files containing OCR/extracted text."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from extract_dav_pdf_chunks import repair_mojibake


def repair_value(value: Any) -> Any:
    if isinstance(value, str):
        return repair_mojibake(value)
    if isinstance(value, list):
        return [repair_value(item) for item in value]
    if isinstance(value, dict):
        return {key: repair_value(item) for key, item in value.items()}
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()

    for path_name in args.paths:
        path = Path(path_name)
        rows = []
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    rows.append(repair_value(json.loads(line)))
        with path.open("w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"repaired {len(rows)} rows in {path}")


if __name__ == "__main__":
    main()
