"""Run the 100-question SafeRAG benchmark and save defense logs."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.evaluate_test_questions_safe_rag import evaluate, load_questions, summarize  # noqa: E402


def configure_runtime(use_llm: bool) -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not use_llm:
        os.environ["USE_LLM_ANSWER"] = "False"


def compact_log_row(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": row.get("id"),
        "group": row.get("group"),
        "question": row.get("question"),
        "rag_action": row.get("rag_action"),
        "intent": row.get("intent"),
        "agent_type": row.get("agent_type"),
        "confidence": row.get("confidence"),
        "source_count": row.get("source_count"),
        "first_source": (row.get("sources") or [{}])[0].get("source") if row.get("sources") else None,
        "graph_should_warn": row.get("graph_should_warn"),
        "graph_highest_risk": row.get("graph_highest_risk"),
        "selected_agents": row.get("selected_agents") or [],
        "pipeline_nodes": row.get("pipeline_nodes") or [],
        "answer_preview": row.get("answer_preview"),
    }


def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(compact_log_row(row), ensure_ascii=False) + "\n")


def write_markdown(path: Path, summary: Dict[str, Any], rows: List[Dict[str, Any]]) -> None:
    lines = [
        "# SafeRAG 100-Question Evaluation",
        "",
        f"- Total questions: {summary.get('total')}",
        f"- No-source responses: {summary.get('no_source_count')}",
        f"- Graph warning count: {summary.get('graph_warning_count')}",
        f"- Graph override count: {summary.get('graph_override_count')}",
        f"- Entity alignment used: {summary.get('alignment_used_count')}",
        f"- Response block schema count: {summary.get('response_block_schema_count')}",
        "",
        "## RAG Action Counts",
        "",
        "| Action | Count |",
        "|---|---:|",
    ]
    for action, count in sorted((summary.get("rag_action_counts") or {}).items()):
        lines.append(f"| {action} | {count} |")
    lines.extend(["", "## High-Attention Cases", "", "| ID | Group | Action | Risk | First source |", "|---|---|---|---|---|"])
    for case in summary.get("high_attention_cases") or []:
        lines.append(
            f"| {case.get('id')} | {case.get('group')} | {case.get('rag_action')} | "
            f"{case.get('graph_highest_risk') or ''} | {case.get('first_source') or ''} |"
        )
    lines.extend(["", "## Sample Rows", "", "| ID | Group | Action | Sources | Question |", "|---|---|---|---:|---|"])
    for row in rows[:10]:
        question = (row.get("question") or "").replace("|", "/")
        lines.append(
            f"| {row.get('id')} | {row.get('group')} | {row.get('rag_action')} | "
            f"{row.get('source_count')} | {question} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


async def main_async(args: argparse.Namespace) -> None:
    configure_runtime(args.use_llm)
    rows = load_questions(Path(args.input))
    selected_count = args.limit or len(rows)
    print(f"[100q] running {selected_count} question(s) from {args.input}")
    results = await evaluate(rows, limit=args.limit, use_chroma=args.use_chroma, quiet=args.quiet)
    summary = summarize(results)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.prefix
    (output_dir / f"{prefix}_details.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / f"{prefix}_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_jsonl(output_dir / f"{prefix}_compact_log.jsonl", results)
    write_markdown(output_dir / f"{prefix}_summary.md", summary, results)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run SafeRAG 100-question defense benchmark")
    parser.add_argument("--input", default="test_q.json")
    parser.add_argument("--output-dir", default="data/evaluation/defense")
    parser.add_argument("--prefix", default="safe_rag_100q")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--use-chroma", action="store_true")
    parser.add_argument("--use-llm", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    asyncio.run(main_async(parse_args()))
