"""Evaluate evidence guardrails on retrieval evaluation results."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

sys.path.append(str(Path(__file__).resolve().parents[1]))
from backend.safety.evidence_guardrails import evaluate_evidence


DEFAULT_INPUT = "data/evaluation/hybrid_priority_retrieval_results.json"


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def convert_result(row: Dict[str, Any]) -> Dict[str, Any]:
    metadata = {
        "source": row.get("source"),
        "type": row.get("type"),
        "trust_level": row.get("trust_level"),
        "title": row.get("title_or_drug"),
    }
    return {
        "id": row.get("id"),
        "metadata": metadata,
        "document": row.get("document_preview") or "",
        "hybrid_score": row.get("hybrid_score"),
    }


def evaluate_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    cases = []
    actions: Counter[str] = Counter()
    intents: Counter[str] = Counter()

    for case in payload.get("cases", []):
        evidence_rows = [convert_result(row) for row in case.get("results", [])]
        decision = evaluate_evidence(case.get("question", ""), evidence_rows)
        actions[decision.action.value] += 1
        intents[decision.intent.value] += 1
        cases.append(
            {
                "id": case.get("id"),
                "question": case.get("question"),
                "category": case.get("category"),
                "retrieval_hit": case.get("hit_at_k"),
                "decision": {
                    "action": decision.action.value,
                    "intent": decision.intent.value,
                    "should_answer": decision.should_answer,
                    "message": decision.message,
                    "warnings": decision.warnings,
                    "usable_sources": decision.usable_sources,
                    "blocked_sources": decision.blocked_sources,
                    "metadata": decision.metadata,
                },
            }
        )

    return {
        "summary": {
            "case_count": len(cases),
            "action_counts": dict(actions),
            "intent_counts": dict(intents),
        },
        "cases": cases,
    }


def write_markdown(report: Dict[str, Any], path: Path) -> None:
    lines = [
        "# Evidence Guardrail Evaluation",
        "",
        "This evaluates whether retrieved evidence is safe enough to use for answer generation.",
        "",
        "## Summary",
        "",
        f"- Cases: {report['summary']['case_count']}",
        "",
        "### Actions",
        "",
        "| Action | Count |",
        "|---|---:|",
    ]
    for action, count in sorted(report["summary"]["action_counts"].items()):
        lines.append(f"| {action} | {count} |")

    lines.extend(["", "### Cases", ""])
    for case in report["cases"]:
        decision = case["decision"]
        lines.append(
            f"- `{case['id']}` intent=`{decision['intent']}` action=`{decision['action']}` "
            f"should_answer={decision['should_answer']} sources={decision['usable_sources']}"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    configure_stdout()
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--json-output", default="data/evaluation/evidence_guardrail_results.json")
    parser.add_argument("--md-output", default="data/evaluation/evidence_guardrail_report.md")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    report = evaluate_payload(payload)
    Path(args.json_output).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(report, Path(args.md_output))
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
