"""Collect public safety articles from CanhGiacDuoc.

The output is metadata plus article text suitable for safety-oriented RAG. It
focuses on listing pages that publish domestic drug information and
pharmacovigilance safety updates.
"""
from __future__ import annotations

import argparse
import json
import re
import time
from html import unescape
from pathlib import Path
from typing import Dict, Iterable, List
from urllib.parse import urljoin
from urllib.request import Request, urlopen


BASE_URL = "https://canhgiacduoc.org.vn"
SOURCES = {
    "domestic": f"{BASE_URL}/Thongtinthuoc/ThongTinYDuoc.aspx",
    "foreign": f"{BASE_URL}/CanhGiacDuoc/DiemTinCGD.aspx",
}
ADR_PAGE = f"{BASE_URL}/CanhGiacDuoc/phanungcohai.aspx"


def fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": "RAG_BOT_NLP_Project/1.0"})
    with urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8", errors="replace")


def strip_tags(html: str) -> str:
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", html)
    text = unescape(text)
    return re.sub(r"[ \t\r\f\v]+", " ", text).strip()


def clean_text(text: str) -> str:
    lines = []
    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


def listing_url(source_url: str, page: int) -> str:
    return source_url if page == 1 else f"{source_url}?page={page}"


def parse_listing(html: str, source_type: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    seen = set()
    pattern = re.compile(
        r'<a\s+[^>]*href="(?P<href>[^"]+)"[^>]*>(?P<body>.*?)</a>',
        re.S | re.I,
    )
    for match in pattern.finditer(html):
        href = match.group("href")
        if not any(part in href for part in ["/TinYDuoc/", "/DiemTin/"]):
            continue
        title = strip_tags(match.group("body"))
        title = re.sub(r"^(xem tiếp|Xem tiếp)\s*>>\s*", "", title).strip()
        if not title or len(title) < 12:
            continue
        url = urljoin(BASE_URL, href)
        if url in seen:
            continue
        seen.add(url)
        rows.append(
            {
                "source": "canhgiacduoc",
                "source_type": source_type,
                "title": title,
                "url": url,
            }
        )
    return rows


def parse_detail(html: str, fallback_title: str) -> Dict[str, str]:
    text = clean_text(strip_tags(html))
    title = fallback_title
    title_match = re.search(r"\n\s*([^#\n]{20,180})\n\s*\d{2}/\d{2}/\d{4}", "\n" + text)
    if title_match:
        title = title_match.group(1).strip()
    date_match = re.search(r"(\d{2}/\d{2}/\d{4})(?:\s+\d{1,2}:\d{2}:\d{2}\s+[SA]M)?", text)
    published_date = date_match.group(1) if date_match else ""

    start = text.find(title)
    article_text = text[start:] if start >= 0 else text
    stop_markers = ["# Các tin liên quan", "Bản quyền thuộc Trung tâm", "Địa chỉ:"]
    for marker in stop_markers:
        marker_pos = article_text.find(marker)
        if marker_pos > 0:
            article_text = article_text[:marker_pos]
    article_text = clean_text(article_text)
    return {"title": title, "published_date": published_date, "article_text": article_text}


def iter_articles(pages: int, include_details: bool, delay: float) -> Iterable[Dict[str, str]]:
    seen = set()
    for source_type, source_url in SOURCES.items():
        for page in range(1, pages + 1):
            url = listing_url(source_url, page)
            html = fetch(url)
            rows = parse_listing(html, source_type)
            print(f"{source_type} page={page} rows={len(rows)}")
            for row in rows:
                if row["url"] in seen:
                    continue
                seen.add(row["url"])
                if include_details:
                    try:
                        detail = parse_detail(fetch(row["url"]), row["title"])
                        row.update(detail)
                    except Exception as exc:
                        row["error"] = str(exc)
                yield row
            time.sleep(delay)

    try:
        html = fetch(ADR_PAGE)
        detail = parse_detail(html, "Phản ứng có hại của thuốc")
        yield {
            "source": "canhgiacduoc",
            "source_type": "adr_knowledge",
            "title": "Phản ứng có hại của thuốc",
            "url": ADR_PAGE,
            "published_date": detail.get("published_date", ""),
            "article_text": detail.get("article_text", ""),
        }
    except Exception as exc:
        yield {
            "source": "canhgiacduoc",
            "source_type": "adr_knowledge",
            "title": "Phản ứng có hại của thuốc",
            "url": ADR_PAGE,
            "error": str(exc),
        }


def write_jsonl(path: Path, rows: Iterable[Dict[str, str]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=int, default=10)
    parser.add_argument("--delay", type=float, default=0.2)
    parser.add_argument("--no-details", action="store_true")
    parser.add_argument("--output", default="data/processed/canhgiacduoc_safety_articles.jsonl")
    args = parser.parse_args()

    rows = list(iter_articles(args.pages, not args.no_details, args.delay))
    count = write_jsonl(Path(args.output), rows)
    print(f"saved {count} articles to {args.output}")


if __name__ == "__main__":
    main()
