"""Collect DAV recall article listings for safety metadata."""
from __future__ import annotations

import argparse
import json
import re
import time
from html import unescape
from pathlib import Path
from typing import Dict, List
from urllib.parse import urljoin
from urllib.request import Request, urlopen


BASE_URL = "https://dav.gov.vn"
FIRST_PAGE = f"{BASE_URL}/cong-van-thu-hoi-thuoc-cn89.html"
PAGE_URL = f"{BASE_URL}/cong-van-thu-hoi-thuoc-cn89-page{{page}}.html"


def fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": "RAG_BOT_NLP_Project/1.0"})
    with urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8", errors="replace")


def strip_tags(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def parse_listing(html: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    pattern = re.compile(
        r'<a class="item small" href="(?P<href>[^"]+)" title="(?P<title>[^"]+)">(?P<body>.*?)</a>',
        re.S,
    )
    for match in pattern.finditer(html):
        body = match.group("body")
        date_match = re.search(r"<time>\s*([^<]+)\s*</time>", body)
        rows.append(
            {
                "title": unescape(match.group("title")).strip(),
                "url": urljoin(BASE_URL, match.group("href")),
                "published_date": strip_tags(date_match.group(1)) if date_match else "",
                "source": "dav_recall_listing",
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=int, default=3)
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--output", default="data/processed/dav_recalls.jsonl")
    args = parser.parse_args()

    rows: List[Dict[str, str]] = []
    for page in range(1, args.pages + 1):
        url = FIRST_PAGE if page == 1 else PAGE_URL.format(page=page)
        html = fetch(url)
        page_rows = parse_listing(html)
        print(f"page={page} rows={len(page_rows)}")
        rows.extend(page_rows)
        time.sleep(args.delay)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"saved {len(rows)} recall rows to {output}")


if __name__ == "__main__":
    main()
