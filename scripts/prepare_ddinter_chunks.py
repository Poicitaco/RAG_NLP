"""Prepare DDInter public CSV downloads as RAG chunks and KG edge rows."""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Tuple


SOURCE_URL = "https://ddinter.scbdd.com/download/"
SOURCE_LICENSE = "CC-BY-NC-SA-4.0"
LEVEL_ORDER = {"Major": 3, "Moderate": 2, "Minor": 1, "Unknown": 0}
ALIASES = {
    "Acetylsalicylic acid": ["aspirin", "acid acetylsalicylic"],
    "Acetaminophen": ["paracetamol"],
}


def iter_csv_paths(input_dir: Path) -> Iterator[Path]:
    yield from sorted(input_dir.glob("ddinter_downloads_code_*.csv"))


def normalize_name(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip())


def edge_id(drug_a: str, drug_b: str) -> str:
    left, right = sorted([drug_a.lower(), drug_b.lower()])
    slug = re.sub(r"[^a-z0-9]+", "-", f"{left}-{right}").strip("-")
    return f"ddinter:{slug}"


def read_edges(input_dir: Path) -> Iterator[Dict[str, Any]]:
    seen: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for path in iter_csv_paths(input_dir):
        atc_group = path.stem.rsplit("_", 1)[-1]
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                drug_a = normalize_name(row.get("Drug_A") or "")
                drug_b = normalize_name(row.get("Drug_B") or "")
                if not drug_a or not drug_b:
                    continue
                left, right = sorted([drug_a, drug_b], key=str.lower)
                key = (left.lower(), right.lower())
                level = normalize_name(row.get("Level") or "Unknown").title()
                if level not in LEVEL_ORDER:
                    level = "Unknown"
                existing = seen.get(key)
                candidate = {
                    "id": edge_id(left, right),
                    "drug_a": left,
                    "drug_b": right,
                    "ddinter_id_a": row.get("DDInterID_A"),
                    "ddinter_id_b": row.get("DDInterID_B"),
                    "level": level,
                    "source_groups": [atc_group],
                    "source": "ddinter",
                    "source_url": SOURCE_URL,
                    "license": SOURCE_LICENSE,
                    "trust_level": "curated_interaction_database",
                    "requires_review": True,
                }
                if not existing:
                    seen[key] = candidate
                    continue
                existing["source_groups"].append(atc_group)
                if LEVEL_ORDER[level] > LEVEL_ORDER[str(existing["level"])]:
                    existing["level"] = level
    yield from seen.values()


def edge_to_chunk(edge: Dict[str, Any]) -> Dict[str, Any]:
    drug_a = edge["drug_a"]
    drug_b = edge["drug_b"]
    level = edge["level"]
    aliases = sorted(set(ALIASES.get(drug_a, []) + ALIASES.get(drug_b, [])))
    alias_text = f"\nTên thường gặp/alias: {', '.join(aliases)}." if aliases else ""
    document = (
        f"Tương tác thuốc DDInter\n"
        f"Cặp thuốc: {drug_a} và {drug_b}.\n"
        f"Mức độ: {level}.\n"
        f"{alias_text}\n"
        f"Ý nghĩa sử dụng: khi người dùng đang dùng một trong hai thuốc, cần kiểm tra trước khi dùng thuốc còn lại. "
        f"Nếu mức độ Major hoặc Moderate, bot phải cảnh báo và khuyến nghị hỏi bác sĩ/dược sĩ trước khi phối hợp."
    )
    return {
        "id": edge["id"],
        "document": document,
        "metadata": {
            "source": "ddinter",
            "source_url": SOURCE_URL,
            "title": f"{drug_a} - {drug_b}",
            "drug_a": drug_a,
            "drug_b": drug_b,
            "aliases": json.dumps(aliases, ensure_ascii=False),
            "interaction_level": level,
            "section": "drug_drug_interaction",
            "type": "interaction",
            "trust_level": "curated_interaction_database",
            "requires_review": True,
            "license": SOURCE_LICENSE,
        },
    }


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/raw/ddinter")
    parser.add_argument("--chunks-output", default="data/chunks/ddinter_interaction_chunks.jsonl")
    parser.add_argument("--edges-output", default="data/processed/ddinter_interaction_edges.jsonl")
    parser.add_argument("--manifest", default="data/processed/ddinter_manifest.json")
    args = parser.parse_args()

    edges = list(read_edges(Path(args.input_dir)))
    edge_count = write_jsonl(Path(args.edges_output), edges)
    chunk_count = write_jsonl(Path(args.chunks_output), (edge_to_chunk(edge) for edge in edges))

    level_counts = Counter(edge["level"] for edge in edges)
    manifest = {
        "source": SOURCE_URL,
        "license": SOURCE_LICENSE,
        "input_dir": args.input_dir,
        "edges_output": args.edges_output,
        "chunks_output": args.chunks_output,
        "edge_count": edge_count,
        "chunk_count": chunk_count,
        "level_counts": dict(level_counts),
        "trust_policy": "Use as curated drug-drug interaction evidence. Absence from DDInter does not prove no interaction exists.",
    }
    Path(args.manifest).write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
