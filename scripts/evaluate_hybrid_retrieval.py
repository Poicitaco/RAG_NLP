"""Evaluate hybrid BM25 + Chroma retrieval against the RAG benchmark."""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path
from typing import Any, Dict, List

from evaluate_bm25_retrieval import matches_result, read_jsonl
from hybrid_search_rag import chroma_search, combine_results, load_bm25_index
from smoke_search_bm25 import search as bm25_search


DEFAULT_BENCHMARK = "data/evaluation/bm25_retrieval_benchmark.jsonl"
DEFAULT_BM25_INDEX = "data/embeddings/bm25/rag_bm25.pkl.gz"
DEFAULT_CHROMA_DIR = "data/embeddings/chroma_smoke"
DEFAULT_COLLECTION = "pharmaceutical_smoke"
DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def evaluate_case(
    bm25_index: Dict[str, Any],
    case: Dict[str, Any],
    bm25_k: int,
    vector_k: int,
    top_k: int,
    chroma_dir: str,
    collection: str,
    provider: str,
    model: str,
    bm25_weight: float,
    vector_weight: float,
) -> Dict[str, Any]:
    bm25_results = bm25_search(bm25_index, case["question"], bm25_k)
    chroma_results = chroma_search(case["question"], chroma_dir, collection, provider, model, vector_k)
    results = combine_results(
        case["question"],
        bm25_results,
        chroma_results,
        bm25_weight,
        vector_weight,
        top_k,
    )

    first_relevant_rank = None
    first_strict_rank = None
    annotated = []
    for result in results:
        match = matches_result(case, result)
        if match["relevant"] and first_relevant_rank is None:
            first_relevant_rank = result["rank"]
        if match["strict_relevant"] and first_strict_rank is None:
            first_strict_rank = result["rank"]
        annotated.append(
            {
                "rank": result["rank"],
                "id": result["id"],
                "hybrid_score": result["hybrid_score"],
                "source": result.get("source"),
                "type": result.get("type"),
                "trust_level": result.get("trust_level"),
                "title_or_drug": result.get("title_or_drug"),
                "retrievers": result.get("sources"),
                "match": match,
            }
        )

    return {
        "id": case["id"],
        "question": case["question"],
        "category": case.get("category"),
        "hit_at_k": first_relevant_rank is not None,
        "strict_hit_at_k": first_strict_rank is not None,
        "first_relevant_rank": first_relevant_rank,
        "first_strict_rank": first_strict_rank,
        "reciprocal_rank": 1 / first_relevant_rank if first_relevant_rank else 0.0,
        "strict_reciprocal_rank": 1 / first_strict_rank if first_strict_rank else 0.0,
        "top_result": annotated[0] if annotated else None,
        "results": annotated,
    }


def summarize(rows: List[Dict[str, Any]], top_k: int) -> Dict[str, Any]:
    by_category: Dict[str, Dict[str, Any]] = {}
    for row in rows:
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
        "case_count": len(rows),
        "top_k": top_k,
        "hit_at_k": round(statistics.mean(1 if row["hit_at_k"] else 0 for row in rows), 4),
        "strict_hit_at_k": round(statistics.mean(1 if row["strict_hit_at_k"] else 0 for row in rows), 4),
        "mrr": round(statistics.mean(row["reciprocal_rank"] for row in rows), 4),
        "strict_mrr": round(statistics.mean(row["strict_reciprocal_rank"] for row in rows), 4),
        "by_category": by_category,
        "failures": [
            {
                "id": row["id"],
                "question": row["question"],
                "category": row.get("category"),
                "top_result": row.get("top_result"),
            }
            for row in rows
            if not row["hit_at_k"]
        ],
    }


def write_markdown(summary: Dict[str, Any], rows: List[Dict[str, Any]], path: Path) -> None:
    lines = [
        "# Hybrid Retrieval Evaluation",
        "",
        "This evaluates BM25 + Chroma retrieval with evidence-aware source adjustment.",
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

    lines.extend(["", "## Failures", ""])
    for failure in summary["failures"]:
        top = failure.get("top_result") or {}
        lines.append(f"- `{failure['id']}` {failure['question']} -> top `{top.get('source')}` / `{top.get('type')}`")
    if not summary["failures"]:
        lines.append("- None")

    lines.extend(["", "## Top Results", ""])
    for row in rows:
        top = row.get("top_result") or {}
        lines.append(
            f"- `{row['id']}` hit={row['hit_at_k']} strict={row['strict_hit_at_k']} "
            f"rank={row.get('first_relevant_rank')} top=`{top.get('source')}`/`{top.get('type')}` {top.get('title_or_drug')}"
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    configure_stdout()
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", default=DEFAULT_BENCHMARK)
    parser.add_argument("--bm25-index", default=DEFAULT_BM25_INDEX)
    parser.add_argument("--chroma-dir", default=DEFAULT_CHROMA_DIR)
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--provider", choices=["sentence-transformers", "openai"], default="sentence-transformers")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--bm25-k", type=int, default=500)
    parser.add_argument("--vector-k", type=int, default=10)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--bm25-weight", type=float, default=0.65)
    parser.add_argument("--vector-weight", type=float, default=0.35)
    parser.add_argument("--json-output", default="data/evaluation/hybrid_retrieval_results.json")
    parser.add_argument("--md-output", default="data/evaluation/hybrid_retrieval_report.md")
    args = parser.parse_args()

    bm25_index = load_bm25_index(Path(args.bm25_index))
    cases = list(read_jsonl(Path(args.benchmark)))
    rows = [
        evaluate_case(
            bm25_index,
            case,
            args.bm25_k,
            args.vector_k,
            args.top_k,
            args.chroma_dir,
            args.collection,
            args.provider,
            args.model,
            args.bm25_weight,
            args.vector_weight,
        )
        for case in cases
    ]
    summary = summarize(rows, args.top_k)
    payload = {"summary": summary, "cases": rows}
    Path(args.json_output).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(summary, rows, Path(args.md_output))
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
