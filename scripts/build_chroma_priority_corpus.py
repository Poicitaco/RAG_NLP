"""Build a source-prioritized JSONL corpus for Chroma indexing.

The full RAG corpus is dominated by DAV registry chunks. For vector retrieval,
that can make safety, recall, and leaflet evidence harder to surface while also
making local embedding builds slow. This script keeps all high-value safety/PDF
evidence and adds a bounded registry slice for semantic lookup.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterator, List


DEFAULT_INPUTS = ["data/chunks/rag_corpus_parts"]
PRIORITY_SOURCES = {"dav_recall", "canhgiacduoc", "dav_pdf", "dav_pdf_ocr"}


def iter_jsonl_paths(inputs: List[str]) -> Iterator[Path]:
    for input_name in inputs:
        path = Path(input_name)
        if path.is_dir():
            yield from sorted(path.glob("*.jsonl"))
        elif path.exists():
            yield path


def read_chunks(inputs: List[str]) -> Iterator[Dict[str, Any]]:
    for path in iter_jsonl_paths(inputs):
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    yield json.loads(line)


def row_source(row: Dict[str, Any]) -> str:
    metadata = row.get("metadata") or {}
    return str(metadata.get("source") or metadata.get("source_dataset") or "")


def row_type(row: Dict[str, Any]) -> str:
    metadata = row.get("metadata") or {}
    return str(metadata.get("type") or "")


def should_keep_registry(row: Dict[str, Any], registry_count: int, max_registry: int) -> bool:
    if registry_count >= max_registry:
        return False
    metadata = row.get("metadata") or {}
    section = str(metadata.get("section") or "")
    doc_type = row_type(row)
    return section in {"identity", "composition", "registration"} or doc_type == "drug_info"


def build_priority_corpus(inputs: List[str], output: Path, max_registry: int) -> Dict[str, Any]:
    output.parent.mkdir(parents=True, exist_ok=True)
    seen_ids: set[str] = set()
    source_counts: Counter[str] = Counter()
    type_counts: Counter[str] = Counter()
    registry_count = 0
    total = 0

    with output.open("w", encoding="utf-8", newline="\n") as handle:
        for row in read_chunks(inputs):
            row_id = str(row.get("id") or "")
            if not row_id or row_id in seen_ids:
                continue
            source = row_source(row)
            keep = source in PRIORITY_SOURCES
            if not keep and source == "dav_all" and should_keep_registry(row, registry_count, max_registry):
                keep = True
                registry_count += 1
            if not keep:
                continue

            seen_ids.add(row_id)
            source_counts[source] += 1
            type_counts[row_type(row)] += 1
            total += 1
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    manifest = {
        "output": str(output),
        "inputs": inputs,
        "total_chunks": total,
        "max_registry": max_registry,
        "source_counts": dict(source_counts),
        "type_counts": dict(type_counts),
    }
    manifest_path = output.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="*", default=DEFAULT_INPUTS)
    parser.add_argument("--output", default="data/chunks/chroma_priority_corpus.jsonl")
    parser.add_argument("--max-registry", type=int, default=12000)
    args = parser.parse_args()

    manifest = build_priority_corpus(args.inputs, Path(args.output), args.max_registry)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
