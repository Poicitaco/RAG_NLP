"""Constrained LLM answer rewriting for Safe RAG responses.

The LLM is optional and never acts as the source of medical truth. It only
rewrites approved graph findings and retrieved citations into clearer language.
"""
from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

import httpx

from backend.config.settings import settings
from backend.models import Citation

_logger = logging.getLogger(__name__)


class LLMAnswerService:
    """Optional Gemini-backed rewriter with deterministic fallback behavior."""

    def __init__(self) -> None:
        self.enabled = bool(settings.USE_LLM_ANSWER)
        self.provider = settings.LLM_PROVIDER.lower()
        self.model = settings.LLM_MODEL
        self.timeout = settings.LLM_TIMEOUT_SECONDS

    def is_available(self) -> bool:
        if not self.enabled:
            return False
        if self.provider == "gemini":
            return bool(settings.GEMINI_API_KEY)
        if self.provider == "groq":
            return bool(settings.GROQ_API_KEY)
        return False

    async def rewrite(
        self,
        question: str,
        deterministic_answer: str,
        graph_safety: Dict[str, Any],
        snippets: List[Dict[str, Any]],
        citations: List[Citation],
        patient_context: Optional[Dict[str, Any]] = None,
        subtype: str = "",
    ) -> Optional[str]:
        if not self.is_available():
            return None
        if self.provider not in ("gemini", "groq"):
            return None

        prompt_payload = self._build_prompt(
            question=question,
            deterministic_answer=deterministic_answer,
            graph_safety=graph_safety,
            snippets=snippets,
            citations=citations,
            patient_context=patient_context,
            subtype=subtype,
        )
        try:
            if self.provider == "groq":
                answer = await self._groq_generate(
                    system_prompt=prompt_payload["system_prompt"],
                    user_payload=prompt_payload["user_payload"],
                )
            else:
                answer = await self._gemini_generate(
                    system_prompt=prompt_payload["system_prompt"],
                    user_payload=prompt_payload["user_payload"],
                )
            if not self._is_valid_rewrite(answer, graph_safety, citations):
                _logger.warning(
                    "LLM rewrite bi tu choi boi _is_valid_rewrite - su dung deterministic fallback. "
                    "Co citations: %s | Co graph_safety warning: %s | Do dai tra loi: %s",
                    bool(citations),
                    graph_safety.get("should_warn"),
                    len(answer or ""),
                )
                return None
            return answer
        except Exception as loi_llm:
            _logger.warning(
                "LLM rewrite gap loi, su dung deterministic fallback: %s",
                loi_llm,
                exc_info=True,
            )
            return None

    def _build_prompt(
        self,
        question: str,
        deterministic_answer: str,
        graph_safety: Dict[str, Any],
        snippets: List[Dict[str, Any]],
        citations: List[Citation],
        patient_context: Optional[Dict[str, Any]] = None,
        subtype: str = "",
    ) -> Dict[str, str]:
        evidence = []
        for index, row in enumerate(snippets[:5], 1):
            metadata = row.get("metadata") or {}
            evidence.append(
                {
                    "id": f"S{index}",
                    "title": metadata.get("title")
                    or metadata.get("drug_name")
                    or row.get("title_or_drug"),
                    "source": metadata.get("source")
                    or metadata.get("source_dataset")
                    or row.get("source"),
                    "section": metadata.get("section") or metadata.get("type"),
                    "snippet": (row.get("document_preview") or row.get("document") or "")[:900],
                }
            )

        # Detect safety verdict — subtype takes priority over text scan
        _SUBTYPE_VERDICT = {
            "nsaid_gastric_risk": "NGUY_HIEM",
            "paracetamol_overdose": "NGUY_HIEM",
            "hypertensive_crisis": "NGUY_HIEM",
            "high_risk_context": "CAN_THAN",
        }
        _det_lower = deterministic_answer.lower()
        _action = (graph_safety or {}).get("action", "")
        if subtype and subtype in _SUBTYPE_VERDICT:
            _verdict = _SUBTYPE_VERDICT[subtype]
        elif "nguy hiểm" in _det_lower or "nguy hiem" in _det_lower or _action in ("handoff", "insufficient_evidence"):
            _verdict = "NGUY_HIEM"
        elif "an toàn" in _det_lower or "an toan" in _det_lower or _action == "allow":
            _verdict = "AN_TOAN"
        elif "chưa đủ dữ liệu" in _det_lower:
            _verdict = "CHUA_DU_DU_LIEU"
        else:
            _verdict = "CAN_THAN"

        payload = {
            "question": question,
            "patient_context": patient_context or {},
            "last_assistant_answer": (patient_context or {}).get("last_assistant_answer", ""),
            "deterministic_answer": deterministic_answer,
            "graph_safety": graph_safety,
            "evidence_snippets": evidence,
            "citations": [citation.model_dump() for citation in citations[:5]],
        }

        # Inject verdict vào system prompt — không để trong payload để Groq không tự giải thích
        _VERDICT_INSTRUCTION = {
            "NGUY_HIEM": "LỆNH BẮT BUỘC: Kết luận mục 1 PHẢI là ❌ NGUY HIỂM. Không được dùng ✅ hay ⚠️.",
            "CAN_THAN": "LỆNH BẮT BUỘC: Kết luận mục 1 PHẢI là ⚠️ CẦN THẬN. Không được dùng ✅.",
            "AN_TOAN": "LỆNH BẮT BUỘC: Kết luận mục 1 PHẢI là ✅ AN TOÀN.",
            "CHUA_DU_DU_LIEU": "LỆNH BẮT BUỘC: Nói 'Chưa đủ dữ liệu trong nguồn cho câu hỏi này'.",
        }
        verdict_line = _VERDICT_INSTRUCTION.get(_verdict, "")
        from backend.services.llm_system_prompt import SYSTEM_PROMPT
        system_prompt = SYSTEM_PROMPT + (f"\n\n{verdict_line}" if verdict_line else "")
        return {
            "system_prompt": system_prompt,
            "user_payload": "JSON payload:\n" + json.dumps(payload, ensure_ascii=False, indent=2),
        }

    def _is_valid_rewrite(
        self,
        answer: Optional[str],
        graph_safety: Dict[str, Any],
        citations: List[Citation],
    ) -> bool:
        if not answer:
            return False
        stripped = answer.strip()
        if len(stripped) < 80:
            return False
        # Chap nhan ca [S1] va [ S1] (LLM doi khi them khoang trang)
        import re as _re
        # Bỏ kiểm tra citation gắt gao để chấp nhận câu trả lời LLM tự nhiên hơn
        # if citations and not _re.search(r"\[\s*S\d+\s*\]", stripped):
        #     return False
        if graph_safety.get("should_warn"):
            lowered = stripped.lower()
            warning_terms = ("cảnh báo", "canh bao", "thận trọng", "than trong", "tránh", "tranh", "lưu ý")
            if not any(term in lowered for term in warning_terms):
                return False

        # Kiem tra cau truc 5 section bat buoc: can it nhat 3/5 heading co mat.
        # Normalize Unicode để match cả "Lưu Ý An Toàn" và "lưu ý an toàn"
        import unicodedata as _ud
        def _norm_check(s: str) -> str:
            return _ud.normalize("NFC", s).lower()

        ten_section_can_kiem_tra = [
            "lưu ý an toàn",
            "hướng dẫn nhanh",
            "giải thích",
            "giải pháp",
            "nguồn",
        ]
        # Thêm các biến thể viết hoa/thường phổ biến của Groq
        section_variants = {
            "lưu ý an toàn": ["luu y an toan", "lưu ý", "an toàn"],
            "hướng dẫn nhanh": ["huong dan nhanh", "hướng dẫn"],
            "giải thích": ["giai thich"],
            "giải pháp": ["giai phap", "giải pháp thay thế"],
            "nguồn": ["nguon", "nguồn tham khảo", "tai lieu"],
        }
        normalized_stripped = _norm_check(stripped)
        so_section_co_mat = 0
        for ten_section in ten_section_can_kiem_tra:
            found = _norm_check(ten_section) in normalized_stripped
            if not found:
                for variant in section_variants.get(ten_section, []):
                    if _norm_check(variant) in normalized_stripped:
                        found = True
                        break
            if found:
                so_section_co_mat += 1

        ngu_ong_toi_thieu_section = 3  # giảm từ 4 xuống 3 để dễ pass hơn
        if so_section_co_mat < ngu_ong_toi_thieu_section:
            _logger.warning(
                "LLM rewrite thieu section: chi tim thay %d/%d heading. Fallback.",
                so_section_co_mat, len(ten_section_can_kiem_tra),
            )
            return False

        return True

    async def _gemini_generate(self, system_prompt: str, user_payload: str) -> Optional[str]:
        url = (
            f"{settings.GEMINI_BASE_URL.rstrip('/')}/v1beta/models/"
            f"{self.model}:generateContent"
        )
        body = {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": user_payload}]}],
            "generationConfig": {
                "temperature": settings.LLM_TEMPERATURE,
                "maxOutputTokens": settings.LLM_MAX_OUTPUT_TOKENS,
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ]
        }
        headers = {
            "x-goog-api-key": settings.GEMINI_API_KEY,
            "Content-Type": "application/json",
        }
        
        # Thêm cơ chế tự động retry khi gặp lỗi 429 (Quá tải API miễn phí)
        import asyncio
        max_retries = 3
        data = {}
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(url, headers=headers, json=body)
                    response.raise_for_status()
                    data = response.json()
                    break # Thành công thì thoát vòng lặp
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429 and attempt < max_retries - 1:
                    _logger.warning(f"Gemini API 429 Too Many Requests. Đang đợi 3s để thử lại (Lần {attempt + 1}/{max_retries})...")
                    await asyncio.sleep(3)
                else:
                    raise # Hết lượt retry hoặc lỗi khác thì ném lỗi ra ngoài
                    
        candidates = data.get("candidates") or []
        if not candidates:
            _logger.error(f"Gemini trả về không có candidates. Data: {data}")
            return None
        finish_reason = candidates[0].get("finishReason")
        if finish_reason and finish_reason != "STOP":
            _logger.error(f"Gemini dừng vì finish_reason={finish_reason}. Data: {data}")
            return None
        parts = ((candidates[0].get("content") or {}).get("parts") or [])
        text = "\n".join(part.get("text") or "" for part in parts).strip()
        if not text:
            _logger.error(f"Gemini trả về chuỗi rỗng. Data: {data}")
        return text or None

    async def stream_rewrite(
        self,
        question: str,
        deterministic_answer: str,
        graph_safety: dict,
        snippets: list,
        citations: list,
        patient_context: dict = None,
    ):
        """Generator: yield từng text chunk từ Groq streaming API."""
        if not self.is_available() or self.provider != "groq":
            for word in deterministic_answer.split():
                yield word + " "
            return

        prompt_payload = self._build_prompt(
            question=question,
            deterministic_answer=deterministic_answer,
            graph_safety=graph_safety,
            snippets=snippets,
            citations=citations,
            patient_context=patient_context,
        )
        url = "https://api.groq.com/openai/v1/chat/completions"
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": prompt_payload["system_prompt"]},
                {"role": "user", "content": prompt_payload["user_payload"]},
            ],
            "temperature": settings.LLM_TEMPERATURE,
            "max_tokens": settings.LLM_MAX_OUTPUT_TOKENS,
            "stream": True,
        }
        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=60) as client:
            async with client.stream("POST", url, headers=headers, json=body) as resp:
                if resp.status_code != 200:
                    for word in deterministic_answer.split():
                        yield word + " "
                    return
                async for line in resp.aiter_lines():
                    if not line.startswith("data: "):
                        continue
                    data_str = line[6:]
                    if data_str == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                        delta = chunk["choices"][0]["delta"].get("content", "")
                        if delta:
                            yield delta
                    except Exception:
                        continue

    async def _groq_generate(self, system_prompt: str, user_payload: str) -> Optional[str]:
        url = "https://api.groq.com/openai/v1/chat/completions"
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_payload}
            ],
            "temperature": settings.LLM_TEMPERATURE,
            "max_tokens": settings.LLM_MAX_OUTPUT_TOKENS,
        }
        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        
        import asyncio
        max_retries = 3
        data = {}
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(url, headers=headers, json=body)
                    response.raise_for_status()
                    data = response.json()
                    break
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429 and attempt < max_retries - 1:
                    _logger.warning(f"Groq API 429 Too Many Requests. Đợi 3s... Lần {attempt + 1}/{max_retries}")
                    await asyncio.sleep(3)
                else:
                    raise
                    
        choices = data.get("choices") or []
        if not choices:
            _logger.error(f"Groq trả về không có choices. Data: {data}")
            return None
            
        message = choices[0].get("message") or {}
        text = (message.get("content") or "").strip()
        if not text:
            _logger.error(f"Groq trả về chuỗi rỗng. Data: {data}")
            
        return text or None
