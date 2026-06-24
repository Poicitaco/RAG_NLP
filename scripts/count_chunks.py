"""Count Duoc Thu source characters and reproduced RAG chunks."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable

from prepare_trungtamthuoc_duocthu_chunks import (
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_CHUNK_SIZE,
    HIGH_RISK_CHUNK_OVERLAP,
    HIGH_RISK_SECTION_TYPES,
    clean,
    clean_ocr_text,
    should_skip_document,
    split_text,
)


INPUT_PATH = Path("data/processed/trungtamthuoc_duocthu_monographs.jsonl")


def read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def count_duocthu_chunks(path: Path) -> int:
    chunk_count = 0

    for row in read_jsonl(path):
        title = clean(row.get("title"))
        if not title or should_skip_document(row):
            continue

        for section in row.get("sections") or []:
            text = clean_ocr_text(section.get("text") or "")
            if len(text) < 80:
                continue

            section_types = set(section.get("types") or [])
            chunk_overlap = (
                HIGH_RISK_CHUNK_OVERLAP
                if len(text) > DEFAULT_CHUNK_SIZE and section_types & HIGH_RISK_SECTION_TYPES
                else DEFAULT_CHUNK_OVERLAP
            )
            chunk_count += len(split_text(text, DEFAULT_CHUNK_SIZE, chunk_overlap))

    return chunk_count


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    total_chars = len(INPUT_PATH.read_text(encoding="utf-8"))
    total_chunks = count_duocthu_chunks(INPUT_PATH)

    print(f"File dữ liệu: {INPUT_PATH}")
    print(f"Chunk size: {DEFAULT_CHUNK_SIZE}")
    print(f"Default chunk overlap: {DEFAULT_CHUNK_OVERLAP}")
    print(f"High-risk chunk overlap: {HIGH_RISK_CHUNK_OVERLAP}")
    print(f"High-risk section types: {', '.join(sorted(HIGH_RISK_SECTION_TYPES))}")
    print(f"Tổng số ký tự của file dữ liệu: {total_chars}")
    print(f"Tổng số chunk sau khi chia: {total_chunks}")


if __name__ == "__main__":
    main()
