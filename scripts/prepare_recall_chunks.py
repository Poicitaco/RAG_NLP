"""Prepare DAV recall listings as safety-oriented RAG chunks."""
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
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/processed/dav_recalls.jsonl")
    parser.add_argument("--output", default="data/chunks/dav_recalls_chunks.jsonl")
    args = parser.parse_args()

    chunks = []
    for index, row in enumerate(read_jsonl(Path(args.input)), 1):
        title = row.get("title") or ""
        date = row.get("published_date") or ""
        chunks.append(
            {
                "id": f"dav_recall:{index}",
                "document": f"Cảnh báo/thu hồi thuốc DAV ngày {date}: {title}",
                "metadata": {
                    "source": "dav_recall",
                    "source_url": row.get("url"),
                    "title": title,
                    "published_date": date,
                    "section": "recall",
                    "type": "safety_recall",
                },
            }
        )

    count = write_jsonl(Path(args.output), chunks)
    print(f"saved {count} recall chunks to {args.output}")


if __name__ == "__main__":
    main()
