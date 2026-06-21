"""Prepare TrungTamThuoc Dược thư monographs as RAG chunks."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


DEFAULT_INPUT = "data/processed/trungtamthuoc_duocthu_monographs.jsonl"
DEFAULT_OUTPUT = "data/chunks/trungtamthuoc_duocthu_chunks.jsonl"
DEFAULT_MANIFEST = "data/processed/trungtamthuoc_duocthu_chunks_manifest.json"

SECTION_TO_TYPE = {
    "interaction": "interaction",
    "contraindication": "safety",
    "dosage": "dosage",
    "pregnancy_lactation": "safety",
    "adverse_effect": "safety",
    "indication": "drug_info",
    "overdose": "safety",
    "storage": "drug_info",
}


def clean(value: Any) -> str:
    return " ".join(str(value or "").split())


def read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def split_text(text: str, max_chars: int) -> List[str]:
    text = text.strip()
    if len(text) <= max_chars:
        return [text] if text else []
    parts: List[str] = []
    paragraphs = [part.strip() for part in text.split("\n") if part.strip()]
    current = ""
    for paragraph in paragraphs:
        if len(current) + len(paragraph) + 1 <= max_chars:
            current = f"{current}\n{paragraph}".strip()
            continue
        if current:
            parts.append(current)
        if len(paragraph) <= max_chars:
            current = paragraph
        else:
            for start in range(0, len(paragraph), max_chars):
                parts.append(paragraph[start : start + max_chars])
            current = ""
    if current:
        parts.append(current)
    return parts


def chunk_type(section_types: List[str], source_kind: str) -> str:
    for section_type in section_types:
        if section_type in SECTION_TO_TYPE:
            return SECTION_TO_TYPE[section_type]
    return "drug_info" if source_kind == "active_ingredient" else "safety"


def build_chunks(row: Dict[str, Any], max_chars: int) -> List[Dict[str, Any]]:
    title = clean(row.get("title"))
    if not title or "404" in title or int(row.get("text_length") or 0) < 120:
        return []
    chunks: List[Dict[str, Any]] = []
    source_kind = row.get("source_kind") or "active_ingredient"
    for section_index, section in enumerate(row.get("sections") or [], 1):
        heading = clean(section.get("heading"))
        text = (section.get("text") or "").strip()
        if len(text) < 80:
            continue
        section_types = section.get("types") or []
        doc_type = chunk_type(section_types, source_kind)
        for part_index, part in enumerate(split_text(text, max_chars), 1):
            document = f"{title}\n{heading}\n{part}".strip()
            chunk_id = f"trungtamthuoc:{row.get('slug')}:{section_index}:{part_index}"
            chunks.append(
                {
                    "id": chunk_id,
                    "document": document,
                    "metadata": {
                        "source": "trungtamthuoc_duocthu",
                        "source_url": row.get("source_url"),
                        "source_kind": source_kind,
                        "title": title,
                        "slug": row.get("slug"),
                        "section": heading,
                        "section_types": section_types,
                        "type": doc_type,
                        "trust_level": "secondary_duocthu_reference",
                        "requires_review": True,
                    },
                }
            )
    return chunks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    parser.add_argument("--max-chars", type=int, default=1600)
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    source_rows = 0
    skipped_rows = 0
    chunk_count = 0
    type_counts: Dict[str, int] = {}
    source_kind_counts: Dict[str, int] = {}
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in read_jsonl(input_path):
            source_rows += 1
            chunks = build_chunks(row, args.max_chars)
            if not chunks:
                skipped_rows += 1
                continue
            source_kind_counts[row.get("source_kind") or "unknown"] = (
                source_kind_counts.get(row.get("source_kind") or "unknown", 0) + 1
            )
            for chunk in chunks:
                handle.write(json.dumps(chunk, ensure_ascii=False) + "\n")
                chunk_count += 1
                doc_type = chunk["metadata"]["type"]
                type_counts[doc_type] = type_counts.get(doc_type, 0) + 1

    manifest = {
        "input": str(input_path),
        "output": str(output_path),
        "source_rows": source_rows,
        "skipped_rows": skipped_rows,
        "chunk_count": chunk_count,
        "type_counts": dict(sorted(type_counts.items())),
        "source_kind_counts": dict(sorted(source_kind_counts.items())),
        "trust_level": "secondary_duocthu_reference",
        "requires_review": True,
    }
    manifest_path = Path(args.manifest)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
