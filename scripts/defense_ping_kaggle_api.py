"""Ping the Kaggle embedding API used by the ingestion pipeline."""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def load_env() -> None:
    try:
        from dotenv import load_dotenv

        load_dotenv(ROOT_DIR / ".env")
    except Exception:
        pass


def masked_url(url: str) -> str:
    if not url:
        return ""
    clean = url.rstrip("/")
    if len(clean) <= 28:
        return "[set]"
    return f"{clean[:14]}...{clean[-10:]}"


def request_json(url: str, payload: Optional[Dict[str, Any]], timeout: int) -> Dict[str, Any]:
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="GET" if payload is None else "POST",
    )
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read().decode("utf-8")
    return {
        "ok": True,
        "latency_ms": round((time.perf_counter() - started) * 1000.0, 2),
        "status": getattr(response, "status", None),
        "body": json.loads(raw) if raw.strip().startswith(("{", "[")) else raw[:500],
    }


def ping_embed(base_url: str, timeout: int) -> Dict[str, Any]:
    endpoint = base_url.rstrip("/") + "/embed"
    payload = {"texts": ["Kiem tra API embedding Kaggle cho SafeRAG Pharma."]}
    try:
        result = request_json(endpoint, payload, timeout)
        body = result.get("body") if isinstance(result.get("body"), dict) else {}
        embeddings = body.get("embeddings") if isinstance(body, dict) else None
        first = embeddings[0] if isinstance(embeddings, list) and embeddings else []
        return {
            "endpoint": "/embed",
            "ok": True,
            "latency_ms": result["latency_ms"],
            "http_status": result.get("status"),
            "embedding_count": len(embeddings) if isinstance(embeddings, list) else 0,
            "embedding_dimension": len(first) if isinstance(first, list) else 0,
            "response_keys": sorted(body.keys()) if isinstance(body, dict) else [],
        }
    except urllib.error.HTTPError as exc:
        return {"endpoint": "/embed", "ok": False, "error": f"HTTP {exc.code}: {exc.reason}"}
    except Exception as exc:
        return {"endpoint": "/embed", "ok": False, "error": str(exc)}


def ping_health(base_url: str, timeout: int) -> Dict[str, Any]:
    for suffix in ("/health", "/"):
        try:
            result = request_json(base_url.rstrip("/") + suffix, None, timeout)
            return {
                "endpoint": suffix,
                "ok": True,
                "latency_ms": result["latency_ms"],
                "http_status": result.get("status"),
                "body_preview": str(result.get("body"))[:300],
            }
        except Exception as exc:
            last_error = str(exc)
    return {"endpoint": "/health or /", "ok": False, "error": last_error}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ping Kaggle embedding API")
    parser.add_argument("--output-dir", default="data/evaluation/defense")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--url", default=None, help="Override KAGGLE_API_URL")
    return parser.parse_args()


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    load_env()
    args = parse_args()
    base_url = (args.url or os.getenv("KAGGLE_API_URL") or "").strip().strip('"').rstrip("/")
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not base_url:
        result = {
            "ok": False,
            "error": "KAGGLE_API_URL is not configured",
            "masked_url": "",
        }
    else:
        embed = ping_embed(base_url, args.timeout)
        health = ping_health(base_url, min(args.timeout, 20))
        result = {
            "ok": bool(embed.get("ok")),
            "masked_url": masked_url(base_url),
            "embed": embed,
            "health": health,
            "checked_at_epoch": round(time.time(), 3),
        }

    (output_dir / "kaggle_api_ping.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
