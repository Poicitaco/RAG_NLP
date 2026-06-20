"""Smoke-test the running FastAPI safe RAG chat endpoint."""
from __future__ import annotations

import argparse
import json
import urllib.request
from typing import Any, Dict


QUESTIONS = [
    "Aceclofenac Stella 100mg thu hồi",
    "Paracetamol là thuốc gì?",
    "Paracetamol 500mg dùng thế nào?",
    "Tôi uống aspirin cùng ibuprofen được không?",
    "Tôi khó thở sau khi uống thuốc thì làm sao?",
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
