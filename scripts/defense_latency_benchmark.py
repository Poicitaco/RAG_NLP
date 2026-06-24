"""Defense-ready latency benchmark for SafeRAG Pharma.

This script measures end-to-end latency and pipeline-node latency for a small,
explainable benchmark set. It writes JSON and Markdown outputs that can be used
directly in the report or defense slides.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median, stdev
from typing import Any, Dict, Iterable, List


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


BENCHMARK_CASES: List[Dict[str, str]] = [
    {"id": "lat_001", "group": "drug_lookup", "question": "Paracetamol dung de lam gi?"},
    {"id": "lat_002", "group": "dosage", "question": "Nguoi lon uong paracetamol lieu bao nhieu?"},
    {"id": "lat_003", "group": "interaction", "question": "Aspirin va diclofenac uong chung co sao khong?"},
    {"id": "lat_004", "group": "condition_guardrail", "question": "Toi bi tang huyet ap, co dung pseudoephedrine duoc khong?"},
    {"id": "lat_005", "group": "pediatric", "question": "Tre 3 tuoi bi sot nen dung thuoc gi?"},
    {"id": "lat_006", "group": "emergency", "question": "Toi vua uong 20 vien paracetamol, phai lam gi?"},
    {"id": "lat_007", "group": "misspelling", "question": "Tetracylin co tuong tac voi kem khong?"},
    {"id": "lat_008", "group": "otc_advice", "question": "Bi cam cum nen mua thuoc gi khong can don?"},
]


def configure_runtime(use_llm: bool) -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not use_llm:
        os.environ["USE_LLM_ANSWER"] = "False"


def percentile(values: List[float], p: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = (len(ordered) - 1) * p / 100.0
    lower = int(rank)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = rank - lower
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction


def citation_count(sources: Iterable[Any]) -> int:
    return len(list(sources or []))


def extract_trace(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    pipeline = metadata.get("agent_pipeline") or {}
    return list(pipeline.get("trace") or [])


async def run_one(service: Any, case: Dict[str, str], repeat_index: int) -> Dict[str, Any]:
    started = time.perf_counter()
    response = await service.answer(
        case["question"],
        session_id=f"defense-latency-{case['id']}-{repeat_index}",
    )
    elapsed_ms = (time.perf_counter() - started) * 1000.0
    metadata = response.metadata or {}
    trace = extract_trace(metadata)
    node_durations = {
        str(step.get("node")): round(float(step.get("duration_ms") or step.get("elapsed_ms") or 0.0), 2)
        for step in trace
        if step.get("node")
    }
    return {
        "id": case["id"],
        "group": case["group"],
        "question": case["question"],
        "repeat_index": repeat_index,
        "latency_ms": round(elapsed_ms, 2),
        "rag_action": metadata.get("rag_action"),
        "intent": metadata.get("intent"),
        "agent_type": getattr(response.agent_type, "value", str(response.agent_type)),
        "confidence": response.confidence,
        "source_count": citation_count(response.sources),
        "has_citation": citation_count(response.sources) > 0,
        "warning_count": len(response.warnings or []),
        "pipeline_nodes": [step.get("node") for step in trace if step.get("node")],
        "node_durations_ms": node_durations,
        "answer_preview": (response.message or "")[:500],
    }


def summarize(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    latencies = [float(row["latency_ms"]) for row in rows]
    by_group: Dict[str, List[float]] = defaultdict(list)
    node_times: Dict[str, List[float]] = defaultdict(list)
    for row in rows:
        by_group[row["group"]].append(float(row["latency_ms"]))
        for node, value in (row.get("node_durations_ms") or {}).items():
            if value:
                node_times[node].append(float(value))
    return {
        "total_runs": len(rows),
        "mean_ms": round(mean(latencies), 2) if latencies else 0.0,
        "median_ms": round(median(latencies), 2) if latencies else 0.0,
        "p95_ms": round(percentile(latencies, 95), 2) if latencies else 0.0,
        "min_ms": round(min(latencies), 2) if latencies else 0.0,
        "max_ms": round(max(latencies), 2) if latencies else 0.0,
        "stdev_ms": round(stdev(latencies), 2) if len(latencies) > 1 else 0.0,
        "no_source_count": sum(1 for row in rows if not row["has_citation"]),
        "rag_action_counts": dict(Counter(row.get("rag_action") or "unknown" for row in rows)),
        "group_latency": {
            group: {
                "count": len(values),
                "mean_ms": round(mean(values), 2),
                "median_ms": round(median(values), 2),
                "p95_ms": round(percentile(values, 95), 2),
            }
            for group, values in sorted(by_group.items())
        },
        "pipeline_node_mean_ms": {
            node: round(mean(values), 2)
            for node, values in sorted(node_times.items(), key=lambda item: -mean(item[1]))
        },
    }


def write_markdown(path: Path, rows: List[Dict[str, Any]], summary: Dict[str, Any]) -> None:
    lines = [
        "# SafeRAG Latency Benchmark",
        "",
        f"- Total runs: {summary['total_runs']}",
        f"- Mean latency: {summary['mean_ms']} ms",
        f"- Median latency: {summary['median_ms']} ms",
        f"- P95 latency: {summary['p95_ms']} ms",
        f"- No-source responses: {summary['no_source_count']}",
        "",
        "## Per Case",
        "",
        "| ID | Group | Action | Sources | Latency ms |",
        "|---|---|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['id']} | {row['group']} | {row.get('rag_action') or 'n/a'} | "
            f"{row['source_count']} | {row['latency_ms']} |"
        )
    lines.extend(["", "## Pipeline Node Mean Latency", ""])
    if summary["pipeline_node_mean_ms"]:
        lines.extend(["| Node | Mean ms |", "|---|---:|"])
        for node, value in summary["pipeline_node_mean_ms"].items():
            lines.append(f"| {node} | {value} |")
    else:
        lines.append("Pipeline trace did not expose node-level durations for this run.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


async def main_async(args: argparse.Namespace) -> None:
    configure_runtime(args.use_llm)
    from backend.services.safe_rag_service import SafeRagService

    service_kwargs: Dict[str, Any] = {}
    if not args.use_chroma:
        service_kwargs["chroma_dir"] = Path("__missing_chroma_for_defense_latency__")
    service = SafeRagService(**service_kwargs)

    selected = BENCHMARK_CASES[: args.limit] if args.limit else BENCHMARK_CASES
    rows: List[Dict[str, Any]] = []
    for repeat_index in range(1, args.repeat + 1):
        for case in selected:
            print(f"[latency] repeat={repeat_index}/{args.repeat} case={case['id']} group={case['group']}")
            rows.append(await run_one(service, case, repeat_index))

    summary = summarize(rows)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "latency_benchmark_details.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "latency_benchmark_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_markdown(output_dir / "latency_benchmark_summary.md", rows, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Defense latency benchmark for SafeRAG Pharma")
    parser.add_argument("--output-dir", default="data/evaluation/defense")
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--use-chroma", action="store_true", help="Use real Chroma vector index")
    parser.add_argument("--use-llm", action="store_true", help="Allow final LLM rewrite if configured")
    return parser.parse_args()


if __name__ == "__main__":
    asyncio.run(main_async(parse_args()))
