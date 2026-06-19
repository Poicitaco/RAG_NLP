"""OCR DAV PDF documents that do not have an extractable text layer.

The default OCR language is Vietnamese + English because DAV labels/leaflets are
mostly Vietnamese with English drug names, manufacturers, and active ingredients.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, List
from urllib.request import urlretrieve

from extract_dav_pdf_chunks import chunk_text, normalize_text, section_to_type, split_sections


TESSERACT_EXE_CANDIDATES = [
    "tesseract",
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
]
VIE_TRAINEDDATA_URL = "https://github.com/tesseract-ocr/tessdata_best/raw/main/vie.traineddata"


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


def find_executable(candidates: List[str], name: str) -> str:
    for candidate in candidates:
        resolved = shutil.which(candidate) if "\\" not in candidate else candidate
        if resolved and Path(resolved).exists():
            return resolved
    raise SystemExit(f"Missing executable: {name}. Install it before running OCR.")


def ensure_tessdata(tessdata_dir: Path) -> None:
    tessdata_dir.mkdir(parents=True, exist_ok=True)
    vie_path = tessdata_dir / "vie.traineddata"
    if not vie_path.exists():
        print(f"downloading Vietnamese OCR model -> {vie_path}")
        urlretrieve(VIE_TRAINEDDATA_URL, vie_path)

    eng_path = tessdata_dir / "eng.traineddata"
    if not eng_path.exists():
        for source in [
            Path(r"C:\Program Files\Tesseract-OCR\tessdata\eng.traineddata"),
            Path(r"C:\Program Files (x86)\Tesseract-OCR\tessdata\eng.traineddata"),
        ]:
            if source.exists():
                shutil.copyfile(source, eng_path)
                break


def select_records(text_rows_path: Path, max_files: int | None = None) -> List[Dict[str, Any]]:
    selected = []
    for row in read_jsonl(text_rows_path):
        if row.get("extraction_status") != "needs_ocr":
            continue
        local_path = Path(row.get("local_path", ""))
        if not local_path.exists():
            continue
        selected.append(row)
        if max_files is not None and len(selected) >= max_files:
            break
    return selected


def render_page(pdftoppm: str, pdf_path: Path, page: int, output_prefix: Path, dpi: int) -> Path:
    cmd = [
        pdftoppm,
        "-f",
        str(page),
        "-l",
        str(page),
        "-singlefile",
        "-png",
        "-r",
        str(dpi),
        str(pdf_path),
        str(output_prefix),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output_prefix.with_suffix(".png")


def ocr_image(tesseract: str, image_path: Path, tessdata_dir: Path, lang: str, psm: int) -> str:
    cmd = [
        tesseract,
        str(image_path),
        "stdout",
        "--tessdata-dir",
        str(tessdata_dir),
        "-l",
        lang,
        "--psm",
        str(psm),
    ]
    result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    return normalize_text(result.stdout.strip())


def ocr_pdf(record: Dict[str, Any], pdftoppm: str, tesseract: str, tessdata_dir: Path, lang: str, dpi: int, psm: int, max_pages: int | None) -> Dict[str, Any]:
    pdf_path = Path(record["local_path"])
    pages = record.get("pages") or []
    page_numbers = [page.get("page") for page in pages if page.get("page")]
    if max_pages is not None:
        page_numbers = page_numbers[:max_pages]

    ocr_pages = []
    with tempfile.TemporaryDirectory(prefix="dav_ocr_") as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        for page_number in page_numbers:
            prefix = tmpdir / f"{pdf_path.stem}_p{page_number}"
            image_path = render_page(pdftoppm, pdf_path, int(page_number), prefix, dpi)
            text = ocr_image(tesseract, image_path, tessdata_dir, lang, psm)
            ocr_pages.append({"page": int(page_number), "text": text})

    total_chars = sum(len(page["text"]) for page in ocr_pages)
    return {
        **{key: value for key, value in record.items() if key != "pages"},
        "pages": ocr_pages,
        "total_text_chars": total_chars,
        "empty_pages": sum(1 for page in ocr_pages if not page["text"].strip()),
        "extraction_status": "ocr_ok" if total_chars > 0 else "ocr_empty",
        "ocr_engine": "tesseract",
        "ocr_language": lang,
        "ocr_dpi": dpi,
    }


def make_chunk_id(record: Dict[str, Any], section: str, page: int, index: int) -> str:
    reg = record.get("registration_number") or Path(record.get("local_path", "doc")).stem
    doc_type = record.get("document_type") or "document"
    return f"{reg}:{doc_type}:ocr:p{page}:{section}:{index}"


def rows_to_chunks(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    chunks: List[Dict[str, Any]] = []
    for record in rows:
        local_path = record.get("local_path")
        for page in record.get("pages") or []:
            page_text = page.get("text") or ""
            if not page_text.strip():
                continue
            page_chunk_index = 0
            for section in split_sections(page_text):
                for index, chunk in enumerate(chunk_text(section["text"]), 1):
                    page_chunk_index += 1
                    chunks.append(
                        {
                            "id": make_chunk_id(record, section["section"], page["page"], page_chunk_index),
                            "document": chunk,
                            "metadata": {
                                "source": "dav_pdf_ocr",
                                "source_url": record.get("url"),
                                "local_path": local_path,
                                "page": page["page"],
                                "section": section["section"],
                                "type": section_to_type(section["section"]),
                                "document_type": record.get("document_type"),
                                "drug_name": record.get("drug_name"),
                                "registration_number": record.get("registration_number"),
                                "ocr_engine": record.get("ocr_engine"),
                                "ocr_language": record.get("ocr_language"),
                            },
                        }
                    )
    return chunks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/processed/dav_otc_pdf_text.jsonl")
    parser.add_argument("--output", default="data/processed/dav_otc_pdf_ocr_text.jsonl")
    parser.add_argument("--chunks-output", default="data/chunks/dav_otc_pdf_ocr_chunks.jsonl")
    parser.add_argument("--tessdata-dir", default="tools/tessdata")
    parser.add_argument("--lang", default="vie+eng")
    parser.add_argument("--dpi", type=int, default=220)
    parser.add_argument("--psm", type=int, default=3)
    parser.add_argument("--max-files", type=int, default=None)
    parser.add_argument("--max-pages", type=int, default=None)
    args = parser.parse_args()

    pdftoppm = find_executable(["pdftoppm"], "pdftoppm")
    tesseract = find_executable(TESSERACT_EXE_CANDIDATES, "tesseract")
    tessdata_dir = Path(args.tessdata_dir)
    ensure_tessdata(tessdata_dir)

    selected = select_records(Path(args.input), args.max_files)
    ocr_rows = []
    for index, record in enumerate(selected, 1):
        print(f"ocr {index}/{len(selected)}: {record.get('registration_number')} {record.get('document_type')}")
        ocr_rows.append(ocr_pdf(record, pdftoppm, tesseract, tessdata_dir, args.lang, args.dpi, args.psm, args.max_pages))

    chunks = rows_to_chunks(ocr_rows)
    text_count = write_jsonl(Path(args.output), ocr_rows)
    chunk_count = write_jsonl(Path(args.chunks_output), chunks)
    print(f"saved {text_count} OCR documents to {args.output}")
    print(f"saved {chunk_count} OCR chunks to {args.chunks_output}")


if __name__ == "__main__":
    main()
