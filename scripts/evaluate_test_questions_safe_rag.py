"""Evaluate Safe RAG answers on the public-user test question JSON file."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def load_questions(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    groups = data.get("test_scenarios_phu_hop_nguoi_dung_pho_thong") or {}
    rows = []
    for group_name, items in groups.items():
        for item in items:
            rows.append(
                {
                    "id": item.get("id"),
                    "group": group_name,
                    "question": item.get("question") or "",
                }
            )
    rows.sort(key=lambda row: int(row["id"]))
    return rows


def source_summary(sources: Iterable[Any]) -> List[Dict[str, Any]]:
    rows = []
    for citation in sources:
        rows.append(
            {
                "id": citation.id,
                "source": citation.source,
                "title": citation.title,
                "url": citation.url,
                "section": citation.section,
                "similarity": citation.similarity,
            }
        )
    return rows


async def evaluate(
    rows: List[Dict[str, Any]],
    limit: int | None = None,
    use_chroma: bool = False,
) -> List[Dict[str, Any]]:
    from backend.services.safe_rag_service import SafeRagService

    kwargs = {}
    if not use_chroma:
        kwargs["chroma_dir"] = Path("__missing_chroma_for_batch_eval__")
    service = SafeRagService(**kwargs)
    results = []
    for index, row in enumerate(rows[:limit] if limit else rows, 1):
        response = await service.answer(row["question"], session_id=f"test-q-{row['id']}")
        metadata = response.metadata or {}
        graph_safety = metadata.get("graph_safety") or {}
        results.append(
            {
                **row,
                "agent_type": response.agent_type.value if hasattr(response.agent_type, "value") else str(response.agent_type),
                "confidence": response.confidence,
                "rag_action": metadata.get("rag_action"),
                "intent": metadata.get("intent"),
                "graph_should_warn": graph_safety.get("should_warn"),
                "graph_highest_risk": graph_safety.get("highest_risk"),
                "graph_findings_count": len(graph_safety.get("findings") or []),
                "llm_answer_enabled": metadata.get("llm_answer_enabled"),
                "llm_answer_used": metadata.get("llm_answer_used"),
                "source_count": len(response.sources or []),
                "sources": source_summary(response.sources or []),
                "warnings": response.warnings,
                "suggestions": response.suggestions,
                "answer": response.message,
                "answer_preview": response.message[:700],
            }
        )
        print(f"[{index}/{limit or len(rows)}] id={row['id']} action={metadata.get('rag_action')} graph={graph_safety.get('should_warn')}")
    return results


def summarize(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_group: Dict[str, Counter[str]] = defaultdict(Counter)
    for row in results:
        by_group[row["group"]][row["rag_action"] or "unknown"] += 1

    source_counter = Counter()
    for row in results:
        if row["sources"]:
            source_counter[row["sources"][0]["source"] or "unknown"] += 1
        else:
            source_counter["no_source"] += 1

    risky = [
        {
            "id": row["id"],
            "group": row["group"],
            "question": row["question"],
            "rag_action": row["rag_action"],
            "intent": row["intent"],
            "graph_highest_risk": row["graph_highest_risk"],
            "first_source": row["sources"][0]["source"] if row["sources"] else None,
            "answer_preview": row["answer_preview"],
        }
        for row in results
        if row["graph_should_warn"] or row["rag_action"] in {"handoff", "emergency", "insufficient_evidence"}
    ]

    return {
        "total": len(results),
        "rag_action_counts": dict(Counter(row["rag_action"] or "unknown" for row in results)),
        "intent_counts": dict(Counter(row["intent"] or "unknown" for row in results)),
        "graph_warning_count": sum(1 for row in results if row["graph_should_warn"]),
        "llm_answer_used_count": sum(1 for row in results if row["llm_answer_used"]),
        "no_source_count": sum(1 for row in results if not row["sources"]),
        "first_source_counts": dict(source_counter),
        "by_group_action_counts": {group: dict(counter) for group, counter in by_group.items()},
        "high_attention_cases": risky,
    }


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="test_q.json")
    parser.add_argument("--output", default="data/evaluation/test_q_safe_rag_results.json")
    parser.add_argument("--summary-output", default="data/evaluation/test_q_safe_rag_summary.json")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--use-llm", action="store_true")
    parser.add_argument("--use-chroma", action="store_true")
    args = parser.parse_args()

    if not args.use_llm:
        os.environ["USE_LLM_ANSWER"] = "False"

    rows = load_questions(Path(args.input))
    results = await evaluate(rows, args.limit, use_chroma=args.use_chroma)
    summary = summarize(results)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.summary_output).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
