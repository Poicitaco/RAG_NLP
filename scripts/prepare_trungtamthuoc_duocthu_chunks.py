"""Prepare TrungTamThuoc Dược thư monographs as RAG chunks."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List


DEFAULT_INPUT = "data/processed/trungtamthuoc_duocthu_monographs.jsonl"
DEFAULT_OUTPUT = "data/chunks/trungtamthuoc_duocthu_chunks.jsonl"
DEFAULT_MANIFEST = "data/processed/trungtamthuoc_duocthu_chunks_manifest.json"
DEFAULT_CHUNK_SIZE = 1600
DEFAULT_CHUNK_OVERLAP = 0
HIGH_RISK_CHUNK_OVERLAP = 160
MIN_DOCUMENT_CHARS = 200
HIGH_RISK_SECTION_TYPES = {
    "indication",
    "contraindication",
    "dosage",
    "interaction",
    "pregnancy_lactation",
    "adverse_effect",
    "overdose",
}

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


BOILERPLATE_PATTERNS = [
    re.compile(r"^\s*\d+\s+sản phẩm\s*$", re.IGNORECASE),
    re.compile(r"^\s*Dược sĩ\b.*$", re.IGNORECASE),
    re.compile(r"^\s*Ước tính:\s*.*$", re.IGNORECASE),
    re.compile(r"^\s*Nếu phát hiện nội dung không chính xác.*$", re.IGNORECASE),
    re.compile(r"^\s*Xem thêm\s*$", re.IGNORECASE),
]


def _should_join_lines(previous: str, current: str) -> bool:
    if not previous or not current:
        return False
    if len(previous) <= 3 or len(current) <= 3:
        return False
    if previous.endswith((".", ":", ";", "?", "!", ")", "]")):
        return False
    if re.match(r"^[-+•*]|\d+[\).]", current):
        return False
    return bool(
        previous.endswith((",", "-", "–", "—"))
        or current[:1].islower()
        or re.match(r"^(và|hoặc|của|cho|trong|với|để|khi|nếu|do|tại|là)\b", current, re.IGNORECASE)
    )


def clean_ocr_text(text: str) -> str:
    """Normalize noisy scraped/OCR text before chunk splitting."""
    if not text:
        return ""

    value = str(text)
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = value.replace("\u00a0", " ")
    value = re.sub(r"[\u200b-\u200f\ufeff]", "", value)
    value = re.sub(r"[^\S\n]+", " ", value)
    value = re.sub(r"[^\x09\x0a\x0d\x20-\uFFFF]", "", value)

    cleaned_lines: List[str] = []
    for raw_line in value.split("\n"):
        line = raw_line.strip()
        if not line:
            continue
        if any(pattern.match(line) for pattern in BOILERPLATE_PATTERNS):
            continue
        if re.match(r"^(?:trang\s*)?\d{1,4}$", line, re.IGNORECASE):
            continue
        line = re.sub(r"\s+([,.;:!?%)\]])", r"\1", line)
        line = re.sub(r"([(\[])\s+", r"\1", line)
        line = re.sub(r"\[\s*(\d+(?:\s*[-,]\s*\d+)*)\s*\]", r"[\1]", line)
        line = re.sub(r"\s{2,}", " ", line)

        if cleaned_lines and _should_join_lines(cleaned_lines[-1], line):
            cleaned_lines[-1] = re.sub(r"\s{2,}", " ", f"{cleaned_lines[-1].rstrip('-–—,')} {line}")
        else:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


def read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def should_skip_document(row: Dict[str, Any]) -> bool:
    title = clean(row.get("title"))
    text = str(row.get("text") or "")
    text_length = int(row.get("text_length") or len(text))
    haystack = f"{title}\n{text}"
    return text_length < MIN_DOCUMENT_CHARS or "404 - Not Found" in haystack


def split_text(text: str, max_chars: int, chunk_overlap: int = DEFAULT_CHUNK_OVERLAP) -> List[str]:
    text = text.strip()
    if len(text) <= max_chars:
        return [text] if text else []
    if chunk_overlap >= max_chars:
        raise ValueError("chunk_overlap must be smaller than max_chars")
    parts: List[str] = []
    paragraphs = [part.strip() for part in text.split("\n") if part.strip()]
    current = ""
    for paragraph in paragraphs:
        if len(current) + len(paragraph) + 1 <= max_chars:
            current = f"{current}\n{paragraph}".strip()
            continue
        if current:
            parts.append(current)
            overlap_prefix = current[-chunk_overlap:].strip() if chunk_overlap > 0 else ""
        else:
            overlap_prefix = ""
        if len(paragraph) <= max_chars:
            candidate = f"{overlap_prefix}\n{paragraph}".strip() if overlap_prefix else paragraph
            current = candidate if len(candidate) <= max_chars else paragraph
        else:
            step = max_chars - chunk_overlap
            source = f"{overlap_prefix}\n{paragraph}".strip() if overlap_prefix else paragraph
            for start in range(0, len(source), step):
                parts.append(source[start : start + max_chars])
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
    if not title or should_skip_document(row):
        return []
    chunks: List[Dict[str, Any]] = []
    source_kind = row.get("source_kind") or "active_ingredient"
    for section_index, section in enumerate(row.get("sections") or [], 1):
        heading = clean(section.get("heading"))
        text = clean_ocr_text(section.get("text") or "")
        if len(text) < 80:
            continue
        section_types = section.get("types") or []
        chunk_overlap = (
            HIGH_RISK_CHUNK_OVERLAP
            if len(text) > max_chars and set(section_types) & HIGH_RISK_SECTION_TYPES
            else DEFAULT_CHUNK_OVERLAP
        )
        doc_type = chunk_type(section_types, source_kind)
        for part_index, part in enumerate(split_text(text, max_chars, chunk_overlap), 1):
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
    parser.add_argument("--max-chars", type=int, default=DEFAULT_CHUNK_SIZE)
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
        "chunk_size": args.max_chars,
        "default_chunk_overlap": DEFAULT_CHUNK_OVERLAP,
        "high_risk_chunk_overlap": HIGH_RISK_CHUNK_OVERLAP,
        "high_risk_section_types": sorted(HIGH_RISK_SECTION_TYPES),
        "min_document_chars": MIN_DOCUMENT_CHARS,
        "trust_level": "secondary_duocthu_reference",
        "requires_review": True,
    }
    manifest_path = Path(args.manifest)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
