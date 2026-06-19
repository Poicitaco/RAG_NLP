"""Download DAV leaflet/label documents referenced by normalized drug rows."""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List
from urllib.parse import quote, urljoin, urlparse
from urllib.request import Request, urlopen


BASE_URL = "https://dichvucong.dav.gov.vn"


def read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def safe_name(value: Any) -> str:
    text = str(value or "unknown").strip()
    keep = []
    for char in text:
        keep.append(char if char.isalnum() or char in {"-", "_"} else "_")
    return "".join(keep).strip("_") or "unknown"


def parse_document_entries(value: Any) -> Iterable[str]:
    if not value:
        return []
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return [text]
    else:
        parsed = value

    if isinstance(parsed, dict):
        parsed = [parsed]
    if isinstance(parsed, list):
        paths = []
        for item in parsed:
            if isinstance(item, dict):
                path = item.get("duongDanTep") or item.get("url") or item.get("path")
                if path:
                    paths.append(str(path))
            elif item:
                paths.append(str(item))
        return paths
    return [str(parsed)]


def to_download_url(value: str) -> str:
    if value.startswith("http://") or value.startswith("https://"):
        return value
    return f"{BASE_URL}/File/GoToViewTaiLieu?url={quote(value)}"


def iter_urls(row: Dict[str, Any]) -> Iterable[tuple[str, str]]:
    for label, key in [
        ("leaflet", "leaflet_url"),
        ("label", "label_url"),
        ("label_leaflet", "label_leaflet_url"),
    ]:
        for index, value in enumerate(parse_document_entries(row.get(key)), 1):
            suffix = label if index == 1 else f"{label}_{index}"
            yield suffix, to_download_url(value)


def extension_from_url(url: str, content_type: str | None = None) -> str:
    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix:
        return suffix
    if content_type and "pdf" in content_type.lower():
        return ".pdf"
    return ".bin"


def download(url: str, target: Path, timeout: int = 90) -> None:
    request = Request(url, headers={"User-Agent": "RAG_BOT_NLP_Project/1.0"})
    with urlopen(request, timeout=timeout) as response:
        content = response.read()
        suffix = extension_from_url(url, response.headers.get("Content-Type"))
        if target.suffix != suffix:
            target = target.with_suffix(suffix)
        target.write_bytes(content)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/processed/dav_otc_drugs.jsonl")
    parser.add_argument("--output-dir", default="data/raw/documents/dav_otc")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--delay", type=float, default=0.4)
    parser.add_argument("--manifest", default="data/raw/documents/dav_otc_manifest.jsonl")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = Path(args.manifest)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with manifest_path.open("a", encoding="utf-8") as manifest:
        for row in read_jsonl(Path(args.input)):
            reg = safe_name(row.get("registration_number") or row.get("dav_id"))
            for label, url in iter_urls(row):
                if args.limit is not None and count >= args.limit:
                    print(f"downloaded {count} documents")
                    return

                target = output_dir / f"{reg}_{label}.pdf"
                status = "exists" if target.exists() else "downloaded"
                error = None
                if not target.exists():
                    try:
                        download(url, target)
                        time.sleep(args.delay)
                    except Exception as exc:
                        status = "error"
                        error = str(exc)

                record = {
                    "registration_number": row.get("registration_number"),
                    "drug_name": row.get("drug_name"),
                    "document_type": label,
                    "url": url,
                    "local_path": str(target),
                    "status": status,
                    "error": error,
                }
                manifest.write(json.dumps(record, ensure_ascii=False) + "\n")
                print(f"{status}: {reg} {label}")
                count += 1

    print(f"downloaded {count} documents")


if __name__ == "__main__":
    main()
