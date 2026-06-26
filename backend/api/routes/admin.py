"""Admin API — đọc/ghi config runtime, ping Kaggle, health check."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional
import httpx
import os

router = APIRouter()

# Các key được phép đọc/ghi (whitelist — không expose secrets toàn bộ)
EDITABLE_KEYS = {
    "LLM_PROVIDER", "LLM_MODEL", "LLM_PLANNER_MODEL", "LLM_TEMPERATURE",
    "LLM_MAX_OUTPUT_TOKENS", "LLM_TIMEOUT_SECONDS",
    "USE_LLM_ANSWER", "USE_LLM_PLANNER", "USE_TIERED_CLARIFICATION",
    "KAGGLE_API_URL", "MIN_HYBRID_SCORE", "RULE_MATCH_THRESHOLD",
}

GROQ_MODELS = [
    "llama-3.3-70b-versatile", "llama-3.1-8b-instant",
    "llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768",
    "gemma2-9b-it",
]


class ConfigUpdate(BaseModel):
    key: str
    value: Any


@router.get("/config")
async def get_config():
    """Trả về config hiện tại (whitelist only)."""
    from backend.config.settings import settings
    result = {}
    for key in EDITABLE_KEYS:
        val = getattr(settings, key, None)
        if val is not None:
            # Ẩn API key, chỉ show có/không
            if "KEY" in key:
                result[key] = "***set***" if val else ""
            else:
                result[key] = val
    return {"config": result, "groq_models": GROQ_MODELS}


@router.post("/config")
async def update_config(body: ConfigUpdate):
    """Cập nhật 1 config key vào .env runtime."""
    if body.key not in EDITABLE_KEYS:
        raise HTTPException(400, f"Key '{body.key}' không được phép chỉnh sửa.")

    env_path = ".env"
    if not os.path.exists(env_path):
        raise HTTPException(500, ".env không tồn tại")

    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_line = f'{body.key}="{body.value}"\n'
    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"{body.key}="):
            lines[i] = new_line
            updated = True
            break
    if not updated:
        lines.append(new_line)

    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    # Apply vào settings runtime ngay
    os.environ[body.key] = str(body.value)
    try:
        from backend.config.settings import settings
        if hasattr(settings, body.key):
            field_type = type(getattr(settings, body.key))
            if field_type == bool:
                setattr(settings, body.key, str(body.value).lower() in ("true", "1", "yes"))
            else:
                setattr(settings, body.key, field_type(body.value))
    except Exception:
        pass  # settings immutable → .env đã được ghi, restart sẽ apply

    return {"success": True, "key": body.key, "note": "Đã ghi vào .env. Restart backend để áp dụng đầy đủ."}


@router.get("/ping-kaggle")
async def ping_kaggle():
    """Ping Kaggle embedding API."""
    from backend.config.settings import settings
    url = (settings.KAGGLE_API_URL or "").rstrip("/")
    if not url:
        return {"status": "not_configured", "message": "KAGGLE_API_URL chưa được cấu hình."}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"{url}/embed",
                json={"texts": ["test"]},
                headers={"Content-Type": "application/json"},
            )
        if resp.status_code == 200:
            return {"status": "ok", "latency_ms": int(resp.elapsed.total_seconds() * 1000), "url": url}
        return {"status": "error", "code": resp.status_code, "url": url}
    except Exception as e:
        return {"status": "unreachable", "error": str(e), "url": url}


@router.get("/health")
async def admin_health():
    """Health check chi tiết: BM25, ChromaDB, Groq."""
    from backend.config.settings import settings
    checks: Dict[str, Any] = {}

    # BM25
    bm25_path = "data/embeddings/bm25/rag_bm25.pkl.gz"
    checks["bm25_index"] = {"status": "ok" if os.path.exists(bm25_path) else "missing"}

    # ChromaDB
    chroma_path = "data/embeddings/chroma_priority/chroma.sqlite3"
    if os.path.exists(chroma_path):
        size_mb = round(os.path.getsize(chroma_path) / 1024 / 1024, 1)
        checks["chromadb"] = {"status": "ok", "size_mb": size_mb}
    else:
        checks["chromadb"] = {"status": "missing"}

    # Groq API
    if settings.GROQ_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(
                    "https://api.groq.com/openai/v1/models",
                    headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
                )
            checks["groq"] = {"status": "ok" if resp.status_code == 200 else "error", "code": resp.status_code}
        except Exception as e:
            checks["groq"] = {"status": "unreachable", "error": str(e)}
    else:
        checks["groq"] = {"status": "no_key"}

    overall = "ok" if all(v["status"] == "ok" for v in checks.values()) else "degraded"
    return {"overall": overall, "checks": checks}
