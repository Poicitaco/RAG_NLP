"""Smoke-test the running FastAPI safe RAG chat endpoint."""
from __future__ import annotations

import argparse
import json
import urllib.request
from typing import Any, Dict


QUESTIONS = [
    "Aceclofenac Stella 100mg thu h\u1ed3i",
    "Paracetamol l\u00e0 thu\u1ed1c g\u00ec?",
    "Tui b\u1ecb c\u1ea3m, mua thu\u1ed1c g\u00ec u\u1ed1ng cho nhanh kh\u1ecfi?",
    "T\u00f4i u\u1ed1ng aspirin c\u00f9ng ibuprofen \u0111\u01b0\u1ee3c kh\u00f4ng?",
    "T\u00f4i kh\u00f3 th\u1edf sau khi u\u1ed1ng thu\u1ed1c th\u00ec l\u00e0m sao?",
]


def post_json(url: str, payload: Dict[str, Any], timeout: int) -> Dict[str, Any]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def get_text(url: str, timeout: int) -> str:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return response.read().decode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()

    print(get_text(f"{args.base_url}/health", timeout=10))
    for question in QUESTIONS:
        data = post_json(
            f"{args.base_url}/api/v1/chat/",
            {"message": question, "session_id": "api-smoke"},
            timeout=args.timeout,
        )
        metadata = data.get("metadata") or {}
        first_line = (data.get("message") or "").splitlines()[0]
        print(question)
        print(
            metadata.get("rag_action"),
            metadata.get("intent"),
            len(data.get("sources") or []),
            first_line,
        )


if __name__ == "__main__":
    main()
