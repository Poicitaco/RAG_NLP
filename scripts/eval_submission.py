"""Submission-grade QA orchestrator for the medication safety RAG system."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT_DIR / "data" / "evaluation" / "submission_report.json"
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


TASKS = ("compile", "pytest", "frontend", "pipeline-smoke", "retrieval", "safe-rag", "api-smoke")


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def run_command(name: str, command: list[str]) -> dict[str, Any]:
    started = time.time()
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUTF8", "1")
    completed = subprocess.run(
        command,
        cwd=ROOT_DIR,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    duration = round(time.time() - started, 3)
    return {
        "name": name,
        "command": command,
        "returncode": completed.returncode,
        "duration_seconds": duration,
        "passed": completed.returncode == 0,
        "output_tail": completed.stdout[-4000:],
    }


def run_api_smoke() -> dict[str, Any]:
    started = time.time()
    try:
        from fastapi.testclient import TestClient

        from backend.main import app

        client = TestClient(app)
        response = client.post(
            "/api/v1/chat/",
            json={
                "message": (
                    "T\u00f4i u\u1ed1ng 10 vi\u00ean Panadol c\u00f9ng l\u00fac "
                    "c\u00f3 nguy hi\u1ec3m kh\u00f4ng?"
                ),
                "session_id": "submission-api-smoke",
            },
        )
        payload = response.json()
        metadata = payload.get("metadata") or {}
        passed = (
            response.status_code == 200
            and metadata.get("rag_action") == "emergency"
            and metadata.get("subtype") == "paracetamol_overdose"
            and len(payload.get("sources") or []) > 0
        )
        output = json.dumps(
            {
                "status_code": response.status_code,
                "rag_action": metadata.get("rag_action"),
                "intent": metadata.get("intent"),
                "subtype": metadata.get("subtype"),
                "source_count": len(payload.get("sources") or []),
                "message_preview": str(payload.get("message") or "")[:300],
            },
            ensure_ascii=False,
            indent=2,
        )
        return {
            "name": "api-smoke",
            "command": ["fastapi.testclient", "POST /api/v1/chat/"],
            "returncode": 0 if passed else 1,
            "duration_seconds": round(time.time() - started, 3),
            "passed": passed,
            "output_tail": output,
        }
    except Exception as exc:
        return {
            "name": "api-smoke",
            "command": ["fastapi.testclient", "POST /api/v1/chat/"],
            "returncode": 1,
            "duration_seconds": round(time.time() - started, 3),
            "passed": False,
            "output_tail": repr(exc),
        }


def run_pipeline_smoke() -> dict[str, Any]:
    started = time.time()
    try:
        import asyncio

        from backend.services.safe_rag_service import SafeRagService

        async def _run() -> list[dict[str, Any]]:
            service = SafeRagService()
            cases = [
                {
                    "id": "emergency_source",
                    "question": "Tôi uống 10 viên Panadol cùng lúc có nguy hiểm không?",
                    "expected_action": "emergency",
                    "expected_subtype": "paracetamol_overdose",
                },
                {
                    "id": "interaction_graph_fast_path",
                    "question": "Aspirin uống chung với diclofenac có sao không?",
                    "expected_action": "allow_with_caution",
                    "expected_retriever": "graph_fast_path",
                },
            ]
            rows = []
            for case in cases:
                case_started = time.time()
                response = await service.answer(case["question"], session_id=f"pipeline-smoke-{case['id']}")
                metadata = response.metadata or {}
                rows.append(
                    {
                        **case,
                        "actual_action": metadata.get("rag_action"),
                        "actual_subtype": metadata.get("subtype"),
                        "actual_retriever": metadata.get("retriever"),
                        "source_count": len(response.sources or []),
                        "latency_seconds": round(time.time() - case_started, 3),
                    }
                )
            return rows

        rows = asyncio.run(_run())
        passed = all(row["source_count"] > 0 for row in rows)
        for row in rows:
            if row.get("expected_action") and row["actual_action"] != row["expected_action"]:
                passed = False
            if row.get("expected_subtype") and row["actual_subtype"] != row["expected_subtype"]:
                passed = False
            if row.get("expected_retriever") and row["actual_retriever"] != row["expected_retriever"]:
                passed = False
        return {
            "name": "pipeline-smoke",
            "command": ["SafeRagService.answer", "emergency + interaction fast path"],
            "returncode": 0 if passed else 1,
            "duration_seconds": round(time.time() - started, 3),
            "passed": passed,
            "output_tail": json.dumps(rows, ensure_ascii=False, indent=2),
        }
    except Exception as exc:
        return {
            "name": "pipeline-smoke",
            "command": ["SafeRagService.answer", "emergency + interaction fast path"],
            "returncode": 1,
            "duration_seconds": round(time.time() - started, 3),
            "passed": False,
            "output_tail": repr(exc),
        }


def commands_for(task: str) -> list[dict[str, Any]]:
    python = sys.executable
    npm = "npm.cmd" if sys.platform.startswith("win") else "npm"
    if task == "compile":
        return [{"name": task, "command": [python, "-m", "compileall", "backend", "scripts"]}]
    if task == "frontend":
        frontend_dir = "frontend-next" if (ROOT_DIR / "frontend-next" / "package.json").exists() else "frontend"
        return [{"name": task, "command": [npm, "--prefix", frontend_dir, "run", "build"]}]
    if task == "pytest":
        return [{"name": task, "command": [python, "-m", "pytest", "tests", "-q"]}]
    if task == "retrieval":
        return [
            {
                "name": task,
                "command": [
                    python,
                    "scripts/evaluate_hybrid_retrieval.py",
                    "--chroma-dir",
                    "data/embeddings/chroma_priority",
                    "--collection",
                    "pharmaceutical_local_bge_1024",
                    "--provider",
                    "sentence-transformers",
                    "--model",
                    "BAAI/bge-m3",
                    "--json-output",
                    "data/evaluation/hybrid_bge_submission_results.json",
                    "--md-output",
                    "data/evaluation/hybrid_bge_submission_report.md",
                ],
            }
        ]
    if task == "safe-rag":
        return [
            {
                "name": task,
                "command": [
                    python,
                    "scripts/evaluate_test_questions_safe_rag.py",
                    "--use-chroma",
                    "--quiet",
                    "--output",
                    "data/evaluation/submission_safe_rag_full_results.json",
                    "--summary-output",
                    "data/evaluation/submission_safe_rag_full_summary.json",
                ],
            }
        ]
    if task == "api-smoke":
        return [{"name": task, "callable": run_api_smoke}]
    if task == "pipeline-smoke":
        return [{"name": task, "callable": run_pipeline_smoke}]
    raise ValueError(f"Unknown task: {task}")


def main() -> None:
    configure_stdout()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "tasks",
        nargs="+",
        choices=("all", *TASKS),
        help="QA tasks to run. Use 'all' for compile, pytest, frontend, retrieval, safe-rag, and api-smoke.",
    )
    args = parser.parse_args()

    selected = list(TASKS) if "all" in args.tasks else args.tasks
    results = []
    for task in selected:
        for item in commands_for(task):
            print(f"\n=== Running {item['name']} ===")
            if "callable" in item:
                result = item["callable"]()
            else:
                result = run_command(item["name"], item["command"])
            print(result["output_tail"])
            print(f"=== {item['name']} {'PASS' if result['passed'] else 'FAIL'} in {result['duration_seconds']}s ===")
            results.append(result)
            if not result["passed"]:
                break
        if results and not results[-1]["passed"]:
            break

    payload = {
        "generated_at_epoch": time.time(),
        "selected_tasks": selected,
        "passed": all(result["passed"] for result in results),
        "results": results,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nReport: {REPORT_PATH}")
    raise SystemExit(0 if payload["passed"] else 1)


if __name__ == "__main__":
    main()
