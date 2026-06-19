"""Select a high-value DAV document download sample for OTC RAG.

The selector prioritizes common active ingredients and keeps only rows with at
least one available DAV document URL.
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List


def read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def normalize_key(value: str) -> str:
    text = unicodedata.normalize("NFD", value or "").lower()
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = re.sub(r"\b(bp|usp|ep|hydrochloride|hydroclorid|hydrochlorid)\b", " ", text)
    return " ".join(text.split())


def has_document(row: Dict[str, Any]) -> bool:
    return bool(row.get("leaflet_url") or row.get("label_url") or row.get("label_leaflet_url"))


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
    parser.add_argument("--input", default="data/processed/dav_otc_drugs.jsonl")
    parser.add_argument("--output", default="data/processed/dav_otc_document_priority.jsonl")
    parser.add_argument("--top-ingredients", type=int, default=20)
    parser.add_argument("--per-ingredient", type=int, default=2)
    args = parser.parse_args()

    rows = [row for row in read_jsonl(Path(args.input)) if has_document(row)]
    ingredient_counts = Counter(normalize_key(row.get("active_ingredient") or "") for row in rows)
    ingredient_counts.pop("", None)
    top_keys = {key for key, _ in ingredient_counts.most_common(args.top_ingredients)}

    selected: List[Dict[str, Any]] = []
    seen_regs = set()
    per_key = defaultdict(int)
    for row in rows:
        key = normalize_key(row.get("active_ingredient") or "")
        reg = row.get("registration_number")
        if key not in top_keys or not reg or reg in seen_regs:
            continue
        if per_key[key] >= args.per_ingredient:
            continue
        enriched = dict(row)
        enriched["normalized_active_ingredient"] = key
        enriched["selection_reason"] = "top_otc_active_ingredient_with_dav_document"
        selected.append(enriched)
        seen_regs.add(reg)
        per_key[key] += 1

    count = write_jsonl(Path(args.output), selected)
    print(f"selected {count} rows for priority document download -> {args.output}")
    for key, _ in ingredient_counts.most_common(args.top_ingredients):
        print(f"{key}: selected={per_key[key]} total_with_docs={ingredient_counts[key]}")


if __name__ == "__main__":
    main()
