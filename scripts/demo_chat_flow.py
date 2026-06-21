"""Run a small multi-turn API demo for the medication safety agent."""
from __future__ import annotations

import argparse
import json
import urllib.request
from typing import Any, Dict, List


DEMO_TURNS: List[Dict[str, str]] = [
    {
        "session_id": "demo-cold-diabetes",
        "message": "Tui b\u1ecb c\u1ea3m, mua thu\u1ed1c g\u00ec u\u1ed1ng cho nhanh kh\u1ecfi?",
    },
    {
        "session_id": "demo-cold-diabetes",
        "message": "T\u00f4i 45 tu\u1ed5i, b\u1ecb ti\u1ec3u \u0111\u01b0\u1eddng, kh\u00f4ng d\u1ecb \u1ee9ng, kh\u00f4ng \u0111ang d\u00f9ng thu\u1ed1c kh\u00e1c.",
    },
    {
        "session_id": "demo-interaction",
        "message": "T\u00f4i u\u1ed1ng aspirin c\u00f9ng ibuprofen \u0111\u01b0\u1ee3c kh\u00f4ng?",
    },
    {
        "session_id": "demo-emergency",
        "message": "T\u00f4i kh\u00f3 th\u1edf sau khi u\u1ed1ng thu\u1ed1c th\u00ec l\u00e0m sao?",
    },
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()

    for index, turn in enumerate(DEMO_TURNS, 1):
        data = post_json(
            f"{args.base_url}/api/v1/chat/",
            turn,
            timeout=args.timeout,
        )
        metadata = data.get("metadata") or {}
        preview = " | ".join((data.get("message") or "").splitlines()[:8])
        print(f"\nTURN {index}")
        print("USER:", turn["message"])
        print(
            "BOT:",
            metadata.get("rag_action"),
            metadata.get("intent"),
            "sources=",
            len(data.get("sources") or []),
        )
        print("TRACE:", " -> ".join(step.get("node", "?") for step in (metadata.get("agent_pipeline") or {}).get("trace", [])))
        print(preview)


if __name__ == "__main__":
    main()
