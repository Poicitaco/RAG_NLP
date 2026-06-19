"""Extract downloaded DAV PDF documents into section-aware RAG chunks."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


VI_CHARS = (
    "\u0103\u00e2\u0111\u00ea\u00f4\u01a1\u01b0"
    "\u0102\u00c2\u0110\u00ca\u00d4\u01a0\u01af"
    "\u00e1\u00e0\u1ea3\u00e3\u1ea1\u1ea5\u1ea7\u1ea9\u1eab\u1ead"
    "\u1eaf\u1eb1\u1eb3\u1eb5\u1eb7\u00e9\u00e8\u1ebb\u1ebd\u1eb9"
    "\u1ebf\u1ec1\u1ec3\u1ec5\u1ec7\u00ed\u00ec\u1ec9\u0129\u1ecb"
    "\u00f3\u00f2\u1ecf\u00f5\u1ecd\u1ed1\u1ed3\u1ed5\u1ed7\u1ed9"
    "\u1edb\u1edd\u1edf\u1ee1\u1ee3\u00fa\u00f9\u1ee7\u0169\u1ee5"
    "\u1ee9\u1eeb\u1eed\u1eef\u1ef1\u00fd\u1ef3\u1ef7\u1ef9\u1ef5"
)


SECTION_PATTERNS: List[Tuple[str, re.Pattern[str]]] = [
    ("composition", re.compile(r"^(th\u00e0nh ph\u1ea7n|thanh phan|ho\u1ea1t ch\u1ea5t|hoat chat)", re.I)),
    ("indications", re.compile(r"^(ch\u1ec9 \u0111\u1ecbnh|chi dinh|c\u00f4ng d\u1ee5ng|cong dung)", re.I)),
    ("dosage_administration", re.compile(r"^(li\u1ec1u d\u00f9ng|lieu dung|c\u00e1ch d\u00f9ng|cach dung|\u0111\u01b0\u1eddng d\u00f9ng|duong dung)", re.I)),
    ("contraindications", re.compile(r"^(ch\u1ed1ng ch\u1ec9 \u0111\u1ecbnh|chong chi dinh)", re.I)),
    ("warnings_precautions", re.compile(r"^(c\u1ea3nh b\u00e1o|canh bao|th\u1eadn tr\u1ecdng|than trong|l\u01b0u \u00fd|luu y)", re.I)),
    ("side_effects", re.compile(r"^(t\u00e1c d\u1ee5ng kh\u00f4ng mong mu\u1ed1n|tac dung khong mong muon|t\u00e1c d\u1ee5ng ph\u1ee5|tac dung phu)", re.I)),
    ("interactions", re.compile(r"^(t\u01b0\u01a1ng t\u00e1c thu\u1ed1c|tuong tac thuoc|t\u01b0\u01a1ng t\u00e1c|tuong tac)", re.I)),
    ("overdose", re.compile(r"^(qu\u00e1 li\u1ec1u|qua lieu|x\u1eed tr\u00ed qu\u00e1 li\u1ec1u|xu tri qua lieu)", re.I)),
    ("storage", re.compile(r"^(b\u1ea3o qu\u1ea3n|bao quan)", re.I)),
    ("manufacturer", re.compile(r"^(nh\u00e0 s\u1ea3n xu\u1ea5t|nha san xuat|c\u01a1 s\u1edf s\u1ea3n xu\u1ea5t|co so san xuat)", re.I)),
]


def import_pdf_reader():
    try:
        from pypdf import PdfReader
    except ModuleNotFoundError as exc:
        raise SystemExit("Missing dependency: install pypdf or run `pip install -r requirements.txt`.") from exc
    return PdfReader


def read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def vietnamese_score(text: str) -> int:
    return sum(1 for char in text if char in VI_CHARS)


def repair_mojibake(text: str) -> str:
    if not any(marker in text for marker in ("\u00c3", "\u00c4", "\u00c6", "\u00a1", "\u00bb")):
        return text
    try:
        repaired = text.encode("latin1").decode("utf-8")
    except UnicodeError:
        return text
    return repaired if vietnamese_score(repaired) >= vietnamese_score(text) else text


def normalize_text(text: str) -> str:
    text = repair_mojibake(text)
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf_pages(path: Path) -> List[Dict[str, Any]]:
    PdfReader = import_pdf_reader()
    reader = PdfReader(str(path))
    pages = []
    for index, page in enumerate(reader.pages, 1):
        try:
            text = normalize_text(page.extract_text() or "")
        except Exception:
            text = ""
        pages.append({"page": index, "text": text})
    return pages


def detect_section(line: str) -> str | None:
    candidate = line.strip(" :-\u2013\u2014\t").lower()
    if not candidate or len(candidate) > 120:
        return None
    for section, pattern in SECTION_PATTERNS:
        if pattern.search(candidate):
            return section
    return None


def split_sections(text: str) -> List[Dict[str, str]]:
    current_section = "general"
    current_lines: List[str] = []
    sections: List[Dict[str, str]] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            if current_lines and current_lines[-1] != "":
                current_lines.append("")
            continue

        detected = detect_section(line)
        if detected and current_lines:
            body = normalize_text("\n".join(current_lines))
            if body:
                sections.append({"section": current_section, "text": body})
            current_section = detected
            current_lines = [line]
        elif detected:
            current_section = detected
            current_lines = [line]
        else:
            current_lines.append(line)

    body = normalize_text("\n".join(current_lines))
    if body:
        sections.append({"section": current_section, "text": body})

    return sections or [{"section": "general", "text": normalize_text(text)}]


def chunk_text(text: str, max_chars: int = 1800, overlap: int = 200) -> List[str]:
    text = normalize_text(text)
    if len(text) <= max_chars:
        return [text] if text else []

    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        window = text[start:end]
        cut = max(window.rfind("\n\n"), window.rfind(". "), window.rfind("; "))
        if cut > max_chars * 0.5:
            end = start + cut + 1
            window = text[start:end]
        chunks.append(window.strip())
        if end >= len(text):
            break
        start = max(0, end - overlap)
    return [chunk for chunk in chunks if chunk]


def section_to_type(section: str) -> str:
    if section == "dosage_administration":
        return "dosage"
    if section == "interactions":
        return "interaction"
    if section in {"contraindications", "warnings_precautions", "side_effects", "overdose"}:
        return "safety"
    return "drug_info"


def make_chunk_id(record: Dict[str, Any], section: str, page: int, index: int) -> str:
    reg = record.get("registration_number") or Path(record.get("local_path", "doc")).stem
    doc_type = record.get("document_type") or "document"
    return f"{reg}:{doc_type}:p{page}:{section}:{index}"


def process_manifest(manifest_path: Path, max_files: int | None = None) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    extracted_rows: List[Dict[str, Any]] = []
    chunks: List[Dict[str, Any]] = []
    processed = 0

    for record in read_jsonl(manifest_path):
        if record.get("status") not in {"downloaded", "exists"}:
            continue
        local_path = Path(record.get("local_path", ""))
        if not local_path.exists():
            continue
        if max_files is not None and processed >= max_files:
            break

        pages = extract_pdf_pages(local_path)
        total_chars = sum(len(page.get("text") or "") for page in pages)
        extracted_rows.append(
            {
                **record,
                "pages": pages,
                "total_text_chars": total_chars,
                "empty_pages": sum(1 for page in pages if not (page.get("text") or "").strip()),
                "extraction_status": "ok" if total_chars > 0 else "needs_ocr",
            }
        )
        for page in pages:
            page_text = page.get("text") or ""
            if not page_text:
                continue
            for section in split_sections(page_text):
                for index, chunk in enumerate(chunk_text(section["text"]), 1):
                    chunks.append(
                        {
                            "id": make_chunk_id(record, section["section"], page["page"], index),
                            "document": chunk,
                            "metadata": {
                                "source": "dav_pdf",
                                "source_url": record.get("url"),
                                "local_path": str(local_path),
                                "page": page["page"],
                                "section": section["section"],
                                "type": section_to_type(section["section"]),
                                "document_type": record.get("document_type"),
                                "drug_name": record.get("drug_name"),
                                "registration_number": record.get("registration_number"),
                            },
                        }
                    )
        processed += 1
        status = "ok" if total_chars > 0 else "needs_ocr"
        print(f"processed {local_path} pages={len(pages)} chars={total_chars} status={status}")

    return extracted_rows, chunks


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
    parser.add_argument("--manifest", default="data/raw/documents/dav_otc_manifest.jsonl")
    parser.add_argument("--text-output", default="data/processed/dav_otc_pdf_text.jsonl")
    parser.add_argument("--chunks-output", default="data/chunks/dav_otc_pdf_chunks.jsonl")
    parser.add_argument("--max-files", type=int, default=None)
    args = parser.parse_args()

    extracted_rows, chunks = process_manifest(Path(args.manifest), args.max_files)
    text_count = write_jsonl(Path(args.text_output), extracted_rows)
    chunk_count = write_jsonl(Path(args.chunks_output), chunks)
    print(f"saved {text_count} extracted documents to {args.text_output}")
    print(f"saved {chunk_count} pdf chunks to {args.chunks_output}")


if __name__ == "__main__":
    main()
