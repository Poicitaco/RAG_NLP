"""Build a combined RAG corpus from prepared chunk files."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


DEFAULT_INPUTS = [
    "data/chunks/dav_otc_drugs_chunks.jsonl",
    "data/chunks/dav_otc_pdf_chunks.jsonl",
    "data/chunks/dav_recalls_chunks.jsonl",
]


def read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="*", default=DEFAULT_INPUTS)
    parser.add_argument("--output", default="data/chunks/rag_corpus.jsonl")
    parser.add_argument("--manifest", default="data/processed/rag_corpus_manifest.json")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    source_counts: Dict[str, int] = {}
    type_counts: Dict[str, int] = {}
    total = 0
    seen_ids = set()
    with output.open("w", encoding="utf-8") as handle:
        for input_name in args.inputs:
            input_path = Path(input_name)
            if not input_path.exists():
                continue
            count = 0
            for row in read_jsonl(input_path):
                row_id = row.get("id") or f"{input_path.stem}:{count}"
                if row_id in seen_ids:
                    row_id = f"{input_path.stem}:{count}:{row_id}"
                    row["id"] = row_id
                seen_ids.add(row_id)
                metadata = row.get("metadata") or {}
                source = str(metadata.get("source") or "unknown")
                chunk_type = str(metadata.get("type") or "unknown")
                source_counts[source] = source_counts.get(source, 0) + 1
                type_counts[chunk_type] = type_counts.get(chunk_type, 0) + 1
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
                count += 1
                total += 1
            print(f"{input_path}: {count} chunks")

    manifest = {
        "output": args.output,
        "total_chunks": total,
        "inputs": args.inputs,
        "source_counts": source_counts,
        "type_counts": type_counts,
    }
    write_json(Path(args.manifest), manifest)
    print(f"saved {total} combined chunks to {args.output}")
    print(f"saved manifest to {args.manifest}")


if __name__ == "__main__":
    main()
