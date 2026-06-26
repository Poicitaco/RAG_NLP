"""Triage LLM — Groq quyết định có cần hỏi thêm không, thay thế rule-based slot check."""
from __future__ import annotations

import json
import re
from typing import Any, Dict, Optional

import httpx

from backend.config.settings import settings


class TriageLLMService:
    """Dùng Groq để quyết định: đủ context chưa? Nếu chưa, hỏi câu gì?"""

    SYSTEM_PROMPT = (
        "Bạn là triage agent cho chatbot dược phẩm. "
        "Đọc câu hỏi thuốc và thông tin bệnh nhân đã biết. "
        "Trả về JSON:\n"
        "- Nếu đủ thông tin: {\"ready\": true}\n"
        "- Nếu cần thêm: {\"ready\": false, \"ask\": \"<câu hỏi ngắn>\", \"options\": [\"lựa chọn 1\", \"lựa chọn 2\", ...]}\n"
        "options là 2-4 lựa chọn phổ biến phù hợp với câu hỏi (ví dụ: tuổi → [\"Dưới 12 tuổi\", \"12–60 tuổi\", \"Trên 60 tuổi\"]). "
        "KHÔNG hỏi nếu câu hỏi chỉ là tra cứu thông tin (tác dụng gì, cơ chế gì). "
        "Chỉ hỏi khi thật sự cần để đảm bảo an toàn. "
        "Chỉ trả về JSON thuần, không giải thích."
    )

    def __init__(self) -> None:
        self.enabled = bool(settings.USE_LLM_PLANNER) and settings.LLM_PROVIDER.lower() == "groq"

    async def should_clarify(
        self,
        question: str,
        patient_ctx: Dict[str, Any],
        already_asked: int = 0,
    ) -> Dict[str, Any]:
        """Trả về {"ready": bool, "ask": str|None}. Fallback nếu lỗi."""
        if not self.enabled or already_asked >= 2:
            return {"ready": True, "ask": None}

        payload = json.dumps({
            "question": question,
            "known_context": {k: v for k, v in patient_ctx.items() if v is not None and v != [] and v != {}},
            "turns_asked_so_far": already_asked,
        }, ensure_ascii=False)

        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
                    json={
                        "model": settings.LLM_PLANNER_MODEL or "llama-3.1-8b-instant",
                        "messages": [
                            {"role": "system", "content": self.SYSTEM_PROMPT},
                            {"role": "user", "content": payload},
                        ],
                        "temperature": 0,
                        "max_tokens": 80,
                    },
                )
            text = ((resp.json().get("choices") or [{}])[0].get("message") or {}).get("content") or ""
            match = re.search(r"\{.*\}", text, re.DOTALL)
            result = json.loads(match.group(0) if match else text)
            return {
                "ready": bool(result.get("ready", True)),
                "ask": str(result["ask"]) if not result.get("ready") and result.get("ask") else None,
                "options": result.get("options", []) if not result.get("ready") else [],
            }
        except Exception:
            return {"ready": True, "ask": None}  # fallback: cứ trả lời luôn


_triage: Optional[TriageLLMService] = None


def get_triage_service() -> TriageLLMService:
    global _triage
    if _triage is None:
        _triage = TriageLLMService()
    return _triage
