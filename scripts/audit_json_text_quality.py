"""Audit JSON/JSONL text quality for RAG data files.

The scanner focuses on issues that are dangerous for retrieval and citation:
mojibake Vietnamese text, replacement characters, control characters, and OCR
chunks that are already marked as requiring review.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Tuple


DEFAULT_ROOTS = ["data"]
DEFAULT_OUTPUT_JSON = "data/evaluation/json_text_quality_audit.json"
DEFAULT_OUTPUT_MD = "data/evaluation/json_text_quality_audit.md"

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
)
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
JSON_EXTENSIONS = {".json", ".jsonl"}
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__"}
SKIP_NAMES = {
    "json_text_quality_audit.json",
    "json_text_quality_repair_summary.json",
}


def normalize_text(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def marker_count(text: str) -> int:
    return sum(text.count(marker) for marker in MOJIBAKE_MARKERS)


def vietnamese_score(text: str) -> int:
    vi_chars = set(
        "ăâđêôơưĂÂĐÊÔƠƯ"
        "áàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩị"
        "óòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ"
        "ÁÀẢÃẠẤẦẨẪẬẮẰẲẴẶÉÈẺẼẸẾỀỂỄỆÍÌỈĨỊ"
        "ÓÒỎÕỌỐỒỔỖỘỚỜỞỠỢÚÙỦŨỤỨỪỬỮỰÝỲỶỸỴ"
    )
    return sum(1 for char in text if char in vi_chars)


def has_repairable_mojibake(text: str) -> bool:
    if not any(marker in text for marker in MOJIBAKE_MARKERS):
        return False
    original_markers = marker_count(text)
    original_score = vietnamese_score(text)
    for encoding in ("latin1", "cp1252"):
        try:
            repaired = text.encode(encoding).decode("utf-8")
        except UnicodeError:
            continue
        if marker_count(repaired) < original_markers and vietnamese_score(repaired) >= original_score:
            return True
    return False


def iter_json_paths(roots: List[str]) -> Iterator[Path]:
    for root_name in roots:
        root = Path(root_name)
        if root.is_file() and root.suffix.lower() in JSON_EXTENSIONS:
            yield root
            continue
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if path.name in SKIP_NAMES:
                continue
            if path.is_file() and path.suffix.lower() in JSON_EXTENSIONS:
                yield path


def read_json_records(path: Path, limit: int | None = None) -> Iterator[Tuple[int, Any]]:
    if path.suffix.lower() == ".jsonl":
        with path.open("r", encoding="utf-8") as handle:
            count = 0
            for line_number, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                yield line_number, json.loads(line)
                count += 1
                if limit is not None and count >= limit:
                    return
    else:
        yield 1, json.loads(path.read_text(encoding="utf-8"))


def walk_strings(value: Any, prefix: str = "$") -> Iterator[Tuple[str, str]]:
    if isinstance(value, str):
        yield prefix, value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from walk_strings(item, f"{prefix}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk_strings(item, f"{prefix}[{index}]")


def detect_issues(text: str) -> List[str]:
    issues: List[str] = []
    if has_repairable_mojibake(text):
        issues.append("mojibake_marker")
    if "\ufffd" in text:
        issues.append("replacement_char")
    if CONTROL_RE.search(text):
        issues.append("control_char")
    normalized = normalize_text(text)
    if "khong ro nguon goc" in normalized or "gia mao" in normalized:
        issues.append("safety_signal")
    return issues


def compact_sample(text: str, limit: int = 220) -> str:
    text = CONTROL_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def audit_file(path: Path, sample_limit: int, row_limit: int | None = None) -> Dict[str, Any]:
    issue_counts: Counter[str] = Counter()
    field_counts: Counter[str] = Counter()
    samples: List[Dict[str, Any]] = []
    rows = 0
    parse_errors: List[str] = []
    ocr_review_rows = 0

    try:
        for line_number, record in read_json_records(path, row_limit):
            rows += 1
            metadata = record.get("metadata") if isinstance(record, dict) else None
            if isinstance(metadata, dict) and metadata.get("requires_human_review"):
                ocr_review_rows += 1
            elif isinstance(record, dict) and record.get("requires_human_review"):
                ocr_review_rows += 1

            for field_path, text in walk_strings(record):
                issues = detect_issues(text)
                if not issues:
                    continue
                for issue in issues:
                    issue_counts[issue] += 1
                field_counts[field_path] += 1
                if len(samples) < sample_limit:
                    samples.append(
                        {
                            "line": line_number,
                            "field": field_path,
                            "issues": issues,
                            "sample": compact_sample(text),
                        }
                    )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        parse_errors.append(str(exc))

    return {
        "path": str(path),
        "rows_scanned": rows,
        "issue_counts": dict(issue_counts),
        "top_fields": field_counts.most_common(12),
        "ocr_review_rows": ocr_review_rows,
        "parse_errors": parse_errors,
        "samples": samples,
    }


def write_markdown(report: Dict[str, Any], path: Path) -> None:
    lines = [
        "# JSON Text Quality Audit",
        "",
        "This audit scans JSON/JSONL files for mojibake, replacement characters, control characters, safety signals, and OCR review flags.",
        "",
        "## Summary",
        "",
        f"- Files scanned: {report['files_scanned']}",
        f"- Rows scanned: {report['rows_scanned']}",
        f"- Files with parse errors: {len(report['files_with_parse_errors'])}",
        f"- Files with mojibake markers: {len(report['files_with_mojibake'])}",
        f"- OCR rows requiring human review: {report['ocr_review_rows']}",
        "",
        "## Issue Counts",
        "",
        "| Issue | Count |",
        "|---|---:|",
    ]
    for issue, count in sorted(report["issue_counts"].items()):
        lines.append(f"| {issue} | {count} |")

    lines.extend(["", "## Files With Most Issues", "", "| File | Rows | Issues | OCR review rows |", "|---|---:|---:|---:|"])
    for item in report["files"][:30]:
        total_issues = sum(item["issue_counts"].values())
        if total_issues == 0 and not item["parse_errors"] and item["ocr_review_rows"] == 0:
            continue
        lines.append(
            f"| `{item['path']}` | {item['rows_scanned']} | {total_issues} | {item['ocr_review_rows']} |"
        )

    lines.extend(["", "## Samples", ""])
    sample_count = 0
    for item in report["files"]:
        if not item["samples"]:
            continue
        lines.append(f"### {item['path']}")
        lines.append("")
        for sample in item["samples"][:5]:
            sample_count += 1
            lines.append(
                f"- line {sample['line']} `{sample['field']}` {sample['issues']}: {sample['sample']}"
            )
        lines.append("")
        if sample_count >= 80:
            break

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser()
    parser.add_argument("--roots", nargs="*", default=DEFAULT_ROOTS)
    parser.add_argument("--sample-limit", type=int, default=8)
    parser.add_argument("--row-limit", type=int, default=None)
    parser.add_argument("--json-output", default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--md-output", default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args()

    files = [audit_file(path, args.sample_limit, args.row_limit) for path in iter_json_paths(args.roots)]
    files.sort(key=lambda item: sum(item["issue_counts"].values()), reverse=True)

    issue_counts: Counter[str] = Counter()
    for item in files:
        issue_counts.update(item["issue_counts"])

    report = {
        "roots": args.roots,
        "files_scanned": len(files),
        "rows_scanned": sum(item["rows_scanned"] for item in files),
        "issue_counts": dict(issue_counts),
        "files_with_parse_errors": [item["path"] for item in files if item["parse_errors"]],
        "files_with_mojibake": [
            item["path"] for item in files if item["issue_counts"].get("mojibake_marker", 0) > 0
        ],
        "ocr_review_rows": sum(item["ocr_review_rows"] for item in files),
        "files": files,
    }

    json_output = Path(args.json_output)
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(report, Path(args.md_output))
    print(json.dumps({key: report[key] for key in report if key != "files"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
