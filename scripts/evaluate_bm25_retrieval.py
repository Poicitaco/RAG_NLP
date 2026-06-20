"""Evaluate the local BM25 index against a retrieval benchmark.

The benchmark is source-aware: a hit should match the question, the source type,
and the trust metadata that the answer guardrail will later consume.
"""
from __future__ import annotations

import argparse
import gzip
import json
import pickle
import statistics
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, Iterable, List

sys.path.append(str(Path(__file__).resolve().parent))
from smoke_search_bm25 import search  # noqa: E402


DEFAULT_BENCHMARK = "data/evaluation/bm25_retrieval_benchmark.jsonl"
DEFAULT_INDEX = "data/embeddings/bm25/rag_bm25.pkl.gz"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def normalize_text(text: str) -> str:
    text = (text or "").lower()
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc


def load_index(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(
            f"Missing BM25 index: {path}\n"
            "Build it first with: python scripts/build_bm25_index.py"
        )
    with gzip.open(path, "rb") as handle:
        return pickle.load(handle)


def metadata_source(metadata: Dict[str, Any]) -> str:
    return str(metadata.get("source") or metadata.get("source_dataset") or "")


def result_text(result: Dict[str, Any]) -> str:
    metadata = result.get("metadata") or {}
    fields = [
        result.get("document_preview") or "",
        metadata.get("drug_name") or "",
        metadata.get("active_ingredient") or "",
        metadata.get("registration_number") or "",
        metadata.get("title") or "",
        metadata.get("source_url") or "",
    ]
    return normalize_text(" ".join(str(field) for field in fields))


def matches_result(case: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, bool]:
    metadata = result.get("metadata") or {}
    source = metadata_source(metadata)
    doc_type = str(metadata.get("type") or "")
    trust_level = str(metadata.get("trust_level") or "official_registry")
    haystack = result_text(result)

    relevant_sources = set(case.get("relevant_sources") or [])
    relevant_types = set(case.get("relevant_types") or [])
    allowed_trust = set(case.get("allowed_trust_levels") or [])
    required_terms = [normalize_text(str(term)) for term in case.get("required_terms") or []]

    source_ok = not relevant_sources or source in relevant_sources
    type_ok = not relevant_types or doc_type in relevant_types
    trust_ok = not allowed_trust or trust_level in allowed_trust
    term_ok = not required_terms or any(term and term in haystack for term in required_terms)
    strict_term_ok = not required_terms or all(term and term in haystack for term in required_terms)

    return {
        "source_ok": source_ok,
        "type_ok": type_ok,
        "trust_ok": trust_ok,
        "term_ok": term_ok,
        "strict_term_ok": strict_term_ok,
        "relevant": source_ok and type_ok and trust_ok and term_ok,
        "strict_relevant": source_ok and type_ok and trust_ok and strict_term_ok,
    }


def evaluate_case(index: Dict[str, Any], case: Dict[str, Any], top_k: int) -> Dict[str, Any]:
    results = search(index, case["question"], top_k=top_k)
    first_relevant_rank = None
    first_strict_rank = None
    annotated_results = []

    for result in results:
        match = matches_result(case, result)
        if match["relevant"] and first_relevant_rank is None:
            first_relevant_rank = result["rank"]
        if match["strict_relevant"] and first_strict_rank is None:
            first_strict_rank = result["rank"]

        metadata = result.get("metadata") or {}
        annotated_results.append(
            {
                "rank": result["rank"],
                "score": result["score"],
                "id": result["id"],
                "source": metadata_source(metadata),
                "type": metadata.get("type"),
                "trust_level": metadata.get("trust_level") or "official_registry",
                "title_or_drug": metadata.get("title") or metadata.get("drug_name"),
                "match": match,
            }
        )

    return {
        "id": case["id"],
        "question": case["question"],
        "category": case.get("category"),
        "expected_behavior": case.get("expected_behavior"),
        "hit_at_k": first_relevant_rank is not None,
        "strict_hit_at_k": first_strict_rank is not None,
        "first_relevant_rank": first_relevant_rank,
        "first_strict_rank": first_strict_rank,
        "reciprocal_rank": 1 / first_relevant_rank if first_relevant_rank else 0.0,
        "strict_reciprocal_rank": 1 / first_strict_rank if first_strict_rank else 0.0,
        "top_result": annotated_results[0] if annotated_results else None,
        "results": annotated_results,
    }


def summarize(case_results: List[Dict[str, Any]], top_k: int) -> Dict[str, Any]:
    if not case_results:
        return {"case_count": 0}

    by_category: Dict[str, Dict[str, Any]] = {}
    for row in case_results:
        category = row.get("category") or "uncategorized"
        bucket = by_category.setdefault(
            category,
            {
                "case_count": 0,
                "hits": 0,
                "strict_hits": 0,
                "reciprocal_ranks": [],
                "strict_reciprocal_ranks": [],
            },
        )
        bucket["case_count"] += 1
        bucket["hits"] += 1 if row["hit_at_k"] else 0
        bucket["strict_hits"] += 1 if row["strict_hit_at_k"] else 0
        bucket["reciprocal_ranks"].append(row["reciprocal_rank"])
        bucket["strict_reciprocal_ranks"].append(row["strict_reciprocal_rank"])

    for bucket in by_category.values():
        count = bucket["case_count"]
        bucket["hit_at_k"] = round(bucket.pop("hits") / count, 4)
        bucket["strict_hit_at_k"] = round(bucket.pop("strict_hits") / count, 4)
        bucket["mrr"] = round(statistics.mean(bucket.pop("reciprocal_ranks")), 4)
        bucket["strict_mrr"] = round(statistics.mean(bucket.pop("strict_reciprocal_ranks")), 4)

    return {
        "case_count": len(case_results),
        "top_k": top_k,
        "hit_at_k": round(statistics.mean(1 if row["hit_at_k"] else 0 for row in case_results), 4),
        "strict_hit_at_k": round(
            statistics.mean(1 if row["strict_hit_at_k"] else 0 for row in case_results),
            4,
        ),
        "mrr": round(statistics.mean(row["reciprocal_rank"] for row in case_results), 4),
        "strict_mrr": round(
            statistics.mean(row["strict_reciprocal_rank"] for row in case_results),
            4,
        ),
        "by_category": by_category,
        "failures": [
            {
                "id": row["id"],
                "question": row["question"],
                "category": row.get("category"),
                "top_result": row.get("top_result"),
            }
            for row in case_results
            if not row["hit_at_k"]
        ],
        "strict_failures": [
            {
                "id": row["id"],
                "question": row["question"],
                "category": row.get("category"),
                "first_relevant_rank": row.get("first_relevant_rank"),
                "top_result": row.get("top_result"),
            }
            for row in case_results
            if not row["strict_hit_at_k"]
        ],
    }


def write_markdown_report(summary: Dict[str, Any], case_results: List[Dict[str, Any]], path: Path) -> None:
    lines = [
        "# BM25 Retrieval Evaluation",
        "",
        "This report evaluates the dependency-light BM25 retrieval baseline for the pharmaceutical RAG corpus.",
        "",
        "## Summary",
        "",
        f"- Cases: {summary['case_count']}",
        f"- Top K: {summary['top_k']}",
        f"- Hit@K: {summary['hit_at_k']}",
        f"- Strict Hit@K: {summary['strict_hit_at_k']}",
        f"- MRR: {summary['mrr']}",
        f"- Strict MRR: {summary['strict_mrr']}",
        "",
        "Strict matching requires the retrieved result to satisfy source/type/trust checks and contain all required terms.",
        "",
        "## By Category",
        "",
        "| Category | Cases | Hit@K | Strict Hit@K | MRR | Strict MRR |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for category, bucket in sorted(summary["by_category"].items()):
        lines.append(
            f"| {category} | {bucket['case_count']} | {bucket['hit_at_k']} | "
            f"{bucket['strict_hit_at_k']} | {bucket['mrr']} | {bucket['strict_mrr']} |"
        )

    lines.extend(["", "## Case Results", ""])
    for row in case_results:
        top = row.get("top_result") or {}
        lines.extend(
            [
                f"### {row['id']}",
                "",
                f"- Question: {row['question']}",
                f"- Category: {row.get('category')}",
                f"- Hit@K: {row['hit_at_k']} | Strict Hit@K: {row['strict_hit_at_k']}",
                f"- First relevant rank: {row.get('first_relevant_rank')}",
                f"- First strict rank: {row.get('first_strict_rank')}",
                f"- Top result: `{top.get('source')}` / `{top.get('type')}` / `{top.get('trust_level')}` / {top.get('title_or_drug')}",
                "",
            ]
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", default=DEFAULT_BENCHMARK)
    parser.add_argument("--index", default=DEFAULT_INDEX)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--json-output", default="data/evaluation/bm25_retrieval_results.json")
    parser.add_argument("--md-output", default="data/evaluation/bm25_retrieval_report.md")
    args = parser.parse_args()

    index = load_index(Path(args.index))
    cases = list(read_jsonl(Path(args.benchmark)))
    case_results = [evaluate_case(index, case, args.top_k) for case in cases]
    summary = summarize(case_results, args.top_k)
    payload = {"summary": summary, "cases": case_results}

    json_output = Path(args.json_output)
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown_report(summary, case_results, Path(args.md_output))

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
