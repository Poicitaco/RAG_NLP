"""Collect Drug Dictionary / active ingredient pages from TrungTamThuoc.

The crawler is sitemap-driven and rate-limited. It stores processed text and
metadata for RAG/KG ingestion, not raw mirrored HTML.
"""
from __future__ import annotations

import argparse
import gzip
import html
import json
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


BASE_URL = "https://trungtamthuoc.com"
SITEMAP_HOATCHAT = f"{BASE_URL}/sitemap_hoatchat.xml"
HOME_HOATCHAT = f"{BASE_URL}/hoat-chat"
DEFAULT_OUTPUT = "data/processed/trungtamthuoc_duocthu_monographs.jsonl"
DEFAULT_MANIFEST = "data/processed/trungtamthuoc_duocthu_manifest.json"
USER_AGENT = "RAG_NLP_research_bot/0.1 (+https://github.com/Poicitaco/RAG_NLP)"


GENERAL_KEYWORDS = (
    "duoc-thu-quoc-gia-viet-nam",
    "chuyen-luan",
    "phu-luc",
)

SECTION_TYPE_TERMS = {
    "interaction": ["tương tác thuốc", "tuong tac thuoc"],
    "contraindication": ["chống chỉ định", "chong chi dinh"],
    "dosage": ["liều dùng", "cách dùng", "lieu dung", "cach dung"],
    "pregnancy_lactation": ["mang thai", "cho con bú", "cho con bu"],
    "adverse_effect": ["tác dụng không mong muốn", "tac dung khong mong muon"],
    "indication": ["chỉ định", "chi dinh"],
    "overdose": ["quá liều", "qua lieu"],
    "storage": ["bảo quản", "bao quan"],
}


def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()
    return value


def normalize_for_match(value: str) -> str:
    import unicodedata

    value = clean_text(value).lower()
    decomposed = unicodedata.normalize("NFD", value)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def fetch_text(url: str, timeout: int = 30, retries: int = 2) -> str:
    last_error: Optional[Exception] = None
    for attempt in range(retries + 1):
        try:
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept-Encoding": "gzip",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                },
            )
            with urllib.request.urlopen(request, timeout=timeout) as response:
                data = response.read()
            if data[:2] == b"\x1f\x8b":
                return gzip.decompress(data).decode("utf-8", "replace")
            return data.decode("utf-8", "replace")
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            time.sleep(1 + attempt)
    raise RuntimeError(f"Failed to fetch {url}: {last_error}")


def sitemap_urls() -> List[str]:
    xml = fetch_text(SITEMAP_HOATCHAT)
    return re.findall(r"<loc>(.*?)</loc>", xml)


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: List[tuple[str, str]] = []
        self._href = ""
        self._text: List[str] = []
        self._in_a = False

    def handle_starttag(self, tag: str, attrs: List[tuple[str, Optional[str]]]) -> None:
        if tag.lower() == "a":
            self._in_a = True
            self._href = dict(attrs).get("href") or ""
            self._text = []

    def handle_data(self, data: str) -> None:
        if self._in_a:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._in_a:
            self.links.append((self._href, clean_text(" ".join(self._text))))
            self._in_a = False


def general_duocthu_urls() -> List[str]:
    page = fetch_text(HOME_HOATCHAT)
    parser = LinkParser()
    parser.feed(page)
    urls: List[str] = []
    for href, _text in parser.links:
        if not href:
            continue
        if href.startswith("/"):
            href = BASE_URL + href
        if "/tin-hoat-chat/" not in href:
            continue
        if any(keyword in href for keyword in GENERAL_KEYWORDS):
            urls.append(href)
    return list(dict.fromkeys(urls))


class BlockParser(HTMLParser):
    BLOCK_TAGS = {"h1", "h2", "h3", "h4", "p", "li", "td", "th"}

    def __init__(self) -> None:
        super().__init__()
        self.blocks: List[tuple[str, str]] = []
        self._tag_stack: List[str] = []
        self._current_tag: Optional[str] = None
        self._text: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[tuple[str, Optional[str]]]) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg"}:
            self._tag_stack.append(tag)
            return
        if self._tag_stack:
            return
        if tag in self.BLOCK_TAGS:
            self._flush()
            self._current_tag = tag
            self._text = []
        elif tag == "br" and self._current_tag:
            self._text.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self._tag_stack and self._tag_stack[-1] == tag:
            self._tag_stack.pop()
            return
        if self._tag_stack:
            return
        if tag == self._current_tag:
            self._flush()

    def handle_data(self, data: str) -> None:
        if self._tag_stack:
            return
        if self._current_tag:
            self._text.append(data)

    def close(self) -> None:
        self._flush()
        super().close()

    def _flush(self) -> None:
        if not self._current_tag:
            return
        text = clean_text(" ".join(self._text))
        if text:
            self.blocks.append((self._current_tag, text))
        self._current_tag = None
        self._text = []


def extract_title(page: str) -> str:
    match = re.search(r"<h1[^>]*>(.*?)</h1>", page, flags=re.I | re.S)
    if match:
        return clean_text(re.sub(r"<[^>]+>", " ", match.group(1)))
    meta = re.search(r"<title[^>]*>(.*?)</title>", page, flags=re.I | re.S)
    if meta:
        return clean_text(re.sub(r"<[^>]+>", " ", meta.group(1)))
    return ""


def content_region(page: str) -> str:
    lower = page.lower()
    starts = [pos for pos in [lower.find("<article"), lower.find("<h1")] if pos >= 0]
    start = min(starts) if starts else 0
    end_candidates = [
        lower.find("các sản phẩm có chứa hoạt chất", start),
        lower.find("so sánh sản phẩm", start),
        lower.find("<footer", start),
    ]
    end_candidates = [pos for pos in end_candidates if pos > start]
    end = min(end_candidates) if end_candidates else len(page)
    return page[start:end]


def split_sections(blocks: List[tuple[str, str]]) -> List[Dict[str, Any]]:
    sections: List[Dict[str, Any]] = []
    current: Optional[Dict[str, Any]] = None
    for tag, text in blocks:
        if tag in {"h1", "h2", "h3", "h4"}:
            if current and current["text"].strip():
                sections.append(current)
            current = {"heading": text, "level": tag, "text": ""}
        else:
            if current is None:
                current = {"heading": "", "level": "", "text": ""}
            current["text"] += ("\n" if current["text"] else "") + text
    if current and current["text"].strip():
        sections.append(current)
    return sections


def section_types(heading: str, text: str) -> List[str]:
    haystack = normalize_for_match(f"{heading} {text[:300]}")
    found = []
    for section_type, terms in SECTION_TYPE_TERMS.items():
        if any(normalize_for_match(term) in haystack for term in terms):
            found.append(section_type)
    return found


def parse_page(url: str, page: str, source_kind: str) -> Dict[str, Any]:
    title = extract_title(page)
    parser = BlockParser()
    parser.feed(content_region(page))
    parser.close()
    blocks = parser.blocks
    sections = split_sections(blocks)
    normalized_title = normalize_for_match(title)
    matching_heading_indexes = [
        index
        for index, section in enumerate(sections)
        if normalized_title and normalize_for_match(section.get("heading", "")) == normalized_title
    ]
    if len(matching_heading_indexes) >= 2:
        sections = sections[matching_heading_indexes[-1] :]
    elif sections and normalize_for_match(sections[0].get("text", "")).startswith("trang chu hoat chat"):
        sections = sections[1:]
    for section in sections:
        section["types"] = section_types(section["heading"], section["text"])
    full_text = "\n\n".join(
        f"{section['heading']}\n{section['text']}".strip() for section in sections
    )
    slug = url.rstrip("/").split("/")[-1]
    all_types = sorted({item for section in sections for item in section.get("types", [])})
    return {
        "source": "trungtamthuoc_duocthu",
        "source_kind": source_kind,
        "source_url": url,
        "slug": slug,
        "title": title,
        "section_count": len(sections),
        "sections": sections,
        "text": full_text,
        "text_length": len(full_text),
        "detected_section_types": all_types,
        "trust_level": "secondary_duocthu_reference",
        "requires_review": True,
        "notes": (
            "Collected from TrungTamThuoc online Dược thư pages. Use as secondary "
            "reference and cite source URL; verify critical dosing/interaction claims."
        ),
    }


@dataclass
class CollectStats:
    attempted: int = 0
    succeeded: int = 0
    failed: int = 0


def collect(urls: Iterable[str], output: Path, delay: float, timeout: int) -> CollectStats:
    output.parent.mkdir(parents=True, exist_ok=True)
    stats = CollectStats()
    with output.open("w", encoding="utf-8", newline="\n") as handle:
        for url in urls:
            stats.attempted += 1
            source_kind = "active_ingredient" if "/hoat-chat/" in url else "general_monograph"
            try:
                page = fetch_text(url, timeout=timeout)
                row = parse_page(url, page, source_kind)
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
                stats.succeeded += 1
                print(f"[ok] {stats.succeeded}/{stats.attempted} {row['title'][:80]}")
            except Exception as exc:
                stats.failed += 1
                print(f"[fail] {url} {exc}")
            if delay:
                time.sleep(delay)
    return stats


def write_manifest(output: Path, manifest: Path, urls: List[str], stats: CollectStats) -> None:
    rows = []
    if output.exists():
        with output.open("r", encoding="utf-8") as handle:
            rows = [json.loads(line) for line in handle if line.strip()]
    source_kind_counts: Dict[str, int] = {}
    detected_counts: Dict[str, int] = {}
    for row in rows:
        source_kind_counts[row["source_kind"]] = source_kind_counts.get(row["source_kind"], 0) + 1
        for section_type in row.get("detected_section_types") or []:
            detected_counts[section_type] = detected_counts.get(section_type, 0) + 1
    payload = {
        "source": "https://trungtamthuoc.com/hoat-chat",
        "robots_txt": "https://trungtamthuoc.com/robots.txt allows / and lists sitemap_hoatchat.xml",
        "sitemap": SITEMAP_HOATCHAT,
        "available_url_count": len(urls),
        "attempted": stats.attempted,
        "succeeded": stats.succeeded,
        "failed": stats.failed,
        "output": str(output),
        "source_kind_counts": source_kind_counts,
        "detected_section_type_counts": dict(sorted(detected_counts.items())),
        "trust_policy": (
            "Use as secondary Dược thư reference for RAG/KG enrichment. For high-risk "
            "dosage, interaction, pregnancy, liver/kidney, and pediatric claims, require "
            "citation and preferably cross-check with official/curated sources."
        ),
    }
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--delay", type=float, default=0.2)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--include-general", action="store_true")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    args = parser.parse_args()

    urls = sitemap_urls()
    if args.include_general:
        urls = general_duocthu_urls() + urls
    urls = list(dict.fromkeys(urls))
    if args.limit:
        urls = urls[: args.limit]

    output = Path(args.output)
    stats = collect(urls, output, delay=args.delay, timeout=args.timeout)
    write_manifest(output, Path(args.manifest), urls, stats)
    print(Path(args.manifest).read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
