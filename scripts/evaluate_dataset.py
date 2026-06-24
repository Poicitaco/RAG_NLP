"""Evaluate the TrungTamThuoc Duoc Thu JSONL dataset for RAG readiness."""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from prepare_trungtamthuoc_duocthu_chunks import (
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_CHUNK_SIZE,
    HIGH_RISK_CHUNK_OVERLAP,
    HIGH_RISK_SECTION_TYPES,
    MIN_DOCUMENT_CHARS,
    clean_ocr_text,
    should_skip_document,
    split_text,
)


INPUT_PATH = Path("data/processed/trungtamthuoc_duocthu_monographs.jsonl")
CHUNK_SIZE = DEFAULT_CHUNK_SIZE
CHUNK_OVERLAP = DEFAULT_CHUNK_OVERLAP
SHORT_DOC_THRESHOLD = MIN_DOCUMENT_CHARS
LONG_DOC_THRESHOLD = 50_000
CORE_FIELDS = [
    "source",
    "source_kind",
    "source_url",
    "slug",
    "title",
    "section_count",
    "sections",
    "text",
    "text_length",
]
IMPORTANT_SECTION_TYPES = [
    "indication",
    "contraindication",
    "dosage",
    "interaction",
    "adverse_effect",
    "pregnancy_lactation",
    "overdose",
    "storage",
]
RISK_SECTION_TYPES = HIGH_RISK_SECTION_TYPES
SENTENCE_ENDINGS = (".", "!", "?", ":", ";", ")", "]")


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def read_jsonl(path: Path) -> Iterable[Tuple[int, Dict[str, Any]]]:
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if line.strip():
                yield line_no, json.loads(line)


def percentile(values: List[int], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = (len(ordered) - 1) * pct
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = index - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def split_text_with_flags(
    text: str,
    max_chars: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> Tuple[List[str], int]:
    """Use current splitter and count paragraph-sized hard cut risk."""
    chunks = split_text(text, max_chars, chunk_overlap)
    hard_cuts = sum(1 for paragraph in text.split("\n") if len(paragraph.strip()) > max_chars)
    return chunks, hard_cuts


def section_type_set(row: Dict[str, Any]) -> set[str]:
    found: set[str] = set()
    for section in row.get("sections") or []:
        found.update(str(item) for item in (section.get("types") or []))
    return found


def main() -> None:
    configure_stdout()

    if not INPUT_PATH.exists():
        raise SystemExit(f"Missing dataset: {INPUT_PATH}")

    doc_lengths: List[int] = []
    section_counts: List[int] = []
    short_docs: List[Tuple[int, str, int]] = []
    long_docs: List[Tuple[int, str, int]] = []
    missing_fields: Counter[str] = Counter()
    missing_examples: Dict[str, List[str]] = defaultdict(list)
    source_kind_counts: Counter[str] = Counter()
    section_type_doc_counts: Counter[str] = Counter()
    section_type_section_counts: Counter[str] = Counter()
    docs_without_sections: List[Tuple[int, str]] = []
    docs_without_medical_core: List[Tuple[int, str]] = []
    empty_or_short_sections = 0
    total_sections = 0

    total_chunks = 0
    risky_boundary_chunks = 0
    hard_cut_count = 0
    hard_cut_sections = 0
    risk_type_hard_cut_sections = 0
    chunk_counts_per_doc: List[int] = []
    risk_examples: List[str] = []

    for line_no, row in read_jsonl(INPUT_PATH):
        title = str(row.get("title") or row.get("slug") or f"line:{line_no}")
        text = str(row.get("text") or "")
        length = len(text)
        doc_lengths.append(length)
        section_count = len(row.get("sections") or [])
        section_counts.append(section_count)
        source_kind_counts[str(row.get("source_kind") or "missing")] += 1

        if length < SHORT_DOC_THRESHOLD:
            short_docs.append((line_no, title, length))
        if length > LONG_DOC_THRESHOLD:
            long_docs.append((line_no, title, length))

        for field in CORE_FIELDS:
            value = row.get(field)
            missing = value is None or value == "" or value == [] or value == {}
            if missing:
                missing_fields[field] += 1
                if len(missing_examples[field]) < 5:
                    missing_examples[field].append(f"line {line_no}: {title}")

        if should_skip_document(row):
            continue

        if not row.get("sections"):
            docs_without_sections.append((line_no, title))

        doc_types = section_type_set(row)
        for section_type in doc_types:
            section_type_doc_counts[section_type] += 1
        if not (doc_types & set(IMPORTANT_SECTION_TYPES)):
            docs_without_medical_core.append((line_no, title))

        doc_chunk_count = 0
        for section in row.get("sections") or []:
            total_sections += 1
            raw_section_text = section.get("text") or ""
            section_text = clean_ocr_text(raw_section_text)
            section_types = set(str(item) for item in (section.get("types") or []))
            for section_type in section_types:
                section_type_section_counts[section_type] += 1
            if len(section_text) < 80:
                empty_or_short_sections += 1
                continue

            overlap = (
                HIGH_RISK_CHUNK_OVERLAP
                if len(section_text) > CHUNK_SIZE and section_types & RISK_SECTION_TYPES
                else CHUNK_OVERLAP
            )
            chunks, section_hard_cuts = split_text_with_flags(section_text, CHUNK_SIZE, overlap)
            if section_hard_cuts:
                hard_cut_sections += 1
                hard_cut_count += section_hard_cuts
                if section_types & RISK_SECTION_TYPES:
                    risk_type_hard_cut_sections += 1
                    if len(risk_examples) < 5:
                        heading = section.get("heading") or "unknown section"
                        risk_examples.append(f"line {line_no}: {title} | {heading} | types={sorted(section_types)}")

            for chunk in chunks:
                stripped = chunk.strip()
                if stripped and not stripped.endswith(SENTENCE_ENDINGS):
                    risky_boundary_chunks += 1
            doc_chunk_count += len(chunks)

        total_chunks += doc_chunk_count
        chunk_counts_per_doc.append(doc_chunk_count)

    total_docs = len(doc_lengths)
    avg_len = statistics.mean(doc_lengths) if doc_lengths else 0
    min_len = min(doc_lengths) if doc_lengths else 0
    max_len = max(doc_lengths) if doc_lengths else 0
    median_len = statistics.median(doc_lengths) if doc_lengths else 0
    p95_len = percentile(doc_lengths, 0.95)
    p99_len = percentile(doc_lengths, 0.99)
    avg_sections = statistics.mean(section_counts) if section_counts else 0
    avg_chunks = statistics.mean(chunk_counts_per_doc) if chunk_counts_per_doc else 0
    boundary_risk_rate = (risky_boundary_chunks / total_chunks * 100) if total_chunks else 0
    hard_cut_rate = (hard_cut_sections / total_sections * 100) if total_sections else 0

    print("=" * 88)
    print("FULL DATASET EVALUATION REPORT - TRUNGTAMTHUOC DUOC THU")
    print("=" * 88)
    print(f"Input file: {INPUT_PATH}")
    print(
        "Chunking config: "
        f"chunk_size={CHUNK_SIZE}, default_overlap={CHUNK_OVERLAP}, "
        f"high_risk_overlap={HIGH_RISK_CHUNK_OVERLAP}"
    )
    print()

    print("1. DATA DISTRIBUTION")
    print(f"- Total documents/monographs: {total_docs:,}")
    print(f"- Character length avg: {avg_len:,.1f}")
    print(f"- Character length median: {median_len:,.1f}")
    print(f"- Character length min: {min_len:,}")
    print(f"- Character length max: {max_len:,}")
    print(f"- Character length p95: {p95_len:,.1f}")
    print(f"- Character length p99: {p99_len:,.1f}")
    print(f"- Average sections per document: {avg_sections:,.2f}")
    print(f"- Short documents < {SHORT_DOC_THRESHOLD} chars: {len(short_docs):,}")
    print(f"- Long documents > {LONG_DOC_THRESHOLD:,} chars: {len(long_docs):,}")
    if short_docs[:10]:
        print("  Short examples:")
        for line_no, title, length in short_docs[:10]:
            print(f"  - line {line_no}: {title} ({length} chars)")
    if long_docs[:10]:
        print("  Long examples:")
        for line_no, title, length in sorted(long_docs, key=lambda item: item[2], reverse=True)[:10]:
            print(f"  - line {line_no}: {title} ({length} chars)")
    print(f"- Source kind distribution: {dict(source_kind_counts)}")
    print()

    print("2. STRUCTURAL INTEGRITY")
    print("- Core field missing counts:")
    for field in CORE_FIELDS:
        count = missing_fields[field]
        print(f"  {field}: {count:,} missing ({(count / total_docs * 100 if total_docs else 0):.2f}%)")
        for example in missing_examples.get(field, []):
            print(f"    example: {example}")
    print(f"- Documents without sections: {len(docs_without_sections):,}")
    print(f"- Empty/short sections < 80 chars: {empty_or_short_sections:,} / {total_sections:,}")
    print("- Important section type coverage by document:")
    for section_type in IMPORTANT_SECTION_TYPES:
        count = section_type_doc_counts[section_type]
        print(f"  {section_type}: {count:,} docs ({(count / total_docs * 100 if total_docs else 0):.2f}%)")
    print("- Important section type coverage by section:")
    for section_type in IMPORTANT_SECTION_TYPES:
        print(f"  {section_type}: {section_type_section_counts[section_type]:,} sections")
    print(f"- Documents with no tagged important medical section: {len(docs_without_medical_core):,}")
    if docs_without_medical_core[:10]:
        print("  Examples:")
        for line_no, title in docs_without_medical_core[:10]:
            print(f"  - line {line_no}: {title}")
    print()

    print("3. CHUNKING STRATEGY AUDIT")
    print(f"- Total chunks reproduced after OCR cleaning: {total_chunks:,}")
    print(f"- Average chunks per document: {avg_chunks:,.2f}")
    print(f"- Chunks not ending with strong sentence punctuation: {risky_boundary_chunks:,} ({boundary_risk_rate:.2f}%)")
    print(f"- Sections requiring hard paragraph cuts: {hard_cut_sections:,} / {total_sections:,} ({hard_cut_rate:.2f}%)")
    print(f"- Total hard cuts inside long paragraphs: {hard_cut_count:,}")
    print(f"- Risk-type sections requiring hard cuts: {risk_type_hard_cut_sections:,}")
    if risk_examples:
        print("  Risk examples:")
        for example in risk_examples:
            print(f"  - {example}")
    print()

    print("4. RECOMMENDATION")
    if risk_type_hard_cut_sections or boundary_risk_rate > 20:
        print("- Recommendation: adjust chunking before full re-index.")
        print("- Keep field/section-based chunking as the primary strategy because headings/types are already structured.")
        print("- Add modest overlap only when a section must be split: 120-200 chars, especially for dosage, contraindication, interaction, adverse_effect, pregnancy_lactation, and overdose.")
        print("- Avoid one global overlap for every short section because it increases duplicate citations without improving recall much.")
    else:
        print("- Current field/section-based chunking is broadly safe.")
        print("- chunk_overlap=0 is acceptable for most sections because splitter keeps paragraph boundaries.")
        print("- Still consider 120-200 char overlap for rare long paragraphs in high-risk sections.")
    print("=" * 88)


if __name__ == "__main__":
    main()
