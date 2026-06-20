"""Prepare CanhGiacDuoc safety articles as RAG chunks."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, Iterable, List


def read_jsonl(path: Path) -> Iterable[Dict[str, str]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def normalize_text(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text or "")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, max_chars: int = 1600, overlap: int = 180) -> List[str]:
    text = normalize_text(text)
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]

    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        window = text[start:end]
        cut = max(window.rfind("\n"), window.rfind(". "), window.rfind("; "))
        if cut > max_chars * 0.45:
            end = start + cut + 1
            window = text[start:end]
        chunks.append(window.strip())
        if end >= len(text):
            break
        start = max(0, end - overlap)
    return [chunk for chunk in chunks if chunk]


def article_to_chunks(row: Dict[str, str], index: int) -> List[Dict[str, object]]:
    text = row.get("article_text") or row.get("title") or ""
    title = row.get("title") or "CanhGiacDuoc article"
    chunks = []
    for chunk_index, chunk in enumerate(chunk_text(text), 1):
        chunks.append(
            {
                "id": f"canhgiacduoc:{index}:{chunk_index}",
                "document": chunk,
                "metadata": {
                    "source": "canhgiacduoc",
                    "source_url": row.get("url"),
                    "title": title,
                    "published_date": row.get("published_date"),
                    "section": row.get("source_type") or "safety_article",
                    "type": "safety_article",
                    "trust_level": "trusted_safety_article",
                },
            }
        )
    return chunks


def write_jsonl(path: Path, rows: Iterable[Dict[str, object]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/processed/canhgiacduoc_safety_articles.jsonl")
    parser.add_argument("--output", default="data/chunks/canhgiacduoc_safety_chunks.jsonl")
    args = parser.parse_args()

    chunks = []
    for index, row in enumerate(read_jsonl(Path(args.input)), 1):
        chunks.extend(article_to_chunks(row, index))
    count = write_jsonl(Path(args.output), chunks)
    print(f"saved {count} safety article chunks to {args.output}")


if __name__ == "__main__":
    main()
