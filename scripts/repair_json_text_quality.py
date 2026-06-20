"""Repair mojibake text in JSON/JSONL files.

This script is deliberately conservative: each string is repaired only when the
candidate has fewer mojibake markers and a better Vietnamese character score.
It preserves JSON structure and writes UTF-8 with `ensure_ascii=False`.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
import unicodedata
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List


MOJIBAKE_MARKERS = (
    "Ã",
    "Ä",
    "Æ",
    "Â",
    "áº",
    "á»",
    "â€",
    "â€“",
    "â€”",
    "â€™",
    "â€œ",
    "â€",
)
VI_CHARS = set(
    "ăâđêôơưĂÂĐÊÔƠƯ"
    "áàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩị"
    "óòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ"
    "ÁÀẢÃẠẤẦẨẪẬẮẰẲẴẶÉÈẺẼẸẾỀỂỄỆÍÌỈĨỊ"
    "ÓÒỎÕỌỐỒỔỖỘỚỜỞỠỢÚÙỦŨỤỨỪỬỮỰÝỲỶỸỴ"
)
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def marker_count(text: str) -> int:
    return sum(text.count(marker) for marker in MOJIBAKE_MARKERS)


def vietnamese_score(text: str) -> int:
    return sum(1 for char in text if char in VI_CHARS)


def normalized_quality(text: str) -> tuple[int, int, int]:
    replacement = text.count("\ufffd")
    return (-marker_count(text), vietnamese_score(text), -replacement)


def candidate_decodes(text: str) -> Iterator[str]:
    encodings = ("latin1", "cp1252")
    for encoding in encodings:
        try:
            yield text.encode(encoding).decode("utf-8")
        except UnicodeError:
            continue


def repair_text(text: str) -> str:
    if not any(marker in text for marker in MOJIBAKE_MARKERS) and "\ufffd" not in text:
        return CONTROL_RE.sub(" ", text)

    best = text
    best_quality = normalized_quality(text)
    for candidate in candidate_decodes(text):
        candidate = CONTROL_RE.sub(" ", candidate)
        quality = normalized_quality(candidate)
        if quality > best_quality:
            best = candidate
            best_quality = quality
    return best


def repair_value(value: Any) -> tuple[Any, int]:
    if isinstance(value, str):
        repaired = repair_text(value)
        return repaired, 1 if repaired != value else 0
    if isinstance(value, list):
        changed = 0
        repaired_items = []
        for item in value:
            repaired, item_changed = repair_value(item)
            repaired_items.append(repaired)
            changed += item_changed
        return repaired_items, changed
    if isinstance(value, dict):
        changed = 0
        repaired_dict: Dict[str, Any] = {}
        for key, item in value.items():
            repaired, item_changed = repair_value(item)
            repaired_dict[key] = repaired
            changed += item_changed
        return repaired_dict, changed
    return value, 0


def iter_paths(paths: List[str]) -> Iterator[Path]:
    for name in paths:
        path = Path(name)
        if path.is_dir():
            yield from sorted(path.rglob("*.json"))
            yield from sorted(path.rglob("*.jsonl"))
        elif path.exists():
            yield path


def repair_jsonl(path: Path, dry_run: bool) -> Dict[str, Any]:
    rows = 0
    changed_values = 0
    tmp_name = None
    tmp_handle = None
    if not dry_run:
        tmp_handle = tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            newline="\n",
            delete=False,
            dir=str(path.parent),
            prefix=f".{path.name}.",
            suffix=".tmp",
        )
        tmp_name = tmp_handle.name

    try:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                rows += 1
                repaired, changed = repair_value(json.loads(line))
                changed_values += changed
                if tmp_handle:
                    tmp_handle.write(json.dumps(repaired, ensure_ascii=False) + "\n")
    finally:
        if tmp_handle:
            tmp_handle.close()

    if tmp_name:
        Path(tmp_name).replace(path)

    return {"path": str(path), "rows": rows, "changed_values": changed_values}


def repair_json(path: Path, dry_run: bool) -> Dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    repaired, changed_values = repair_value(value)
    if not dry_run and changed_values:
        path.write_text(json.dumps(repaired, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"path": str(path), "rows": 1, "changed_values": changed_values}


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--summary-output", default="data/evaluation/json_text_quality_repair_summary.json")
    args = parser.parse_args()

    results = []
    for path in iter_paths(args.paths):
        if path.suffix.lower() == ".jsonl":
            result = repair_jsonl(path, args.dry_run)
        elif path.suffix.lower() == ".json":
            result = repair_json(path, args.dry_run)
        else:
            continue
        if result["changed_values"]:
            print(json.dumps(result, ensure_ascii=False))
        results.append(result)

    summary = {
        "dry_run": args.dry_run,
        "files": len(results),
        "rows": sum(item["rows"] for item in results),
        "changed_values": sum(item["changed_values"] for item in results),
        "results": results,
    }
    if not args.dry_run:
        output = Path(args.summary_output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: summary[key] for key in summary if key != "results"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
