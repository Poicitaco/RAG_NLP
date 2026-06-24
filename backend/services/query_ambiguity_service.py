"""Ambiguity detection for medication queries before retrieval."""
from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from backend.safety.evidence_guardrails import normalize_text


AMBIGUITY_QUESTIONS = {
    "no_drug_found": [
        "Bạn có thể cho mình biết tên thuốc ghi trên hộp hoặc vỉ thuốc không?",
        "Thuốc này dùng để trị bệnh gì vậy bạn?",
    ],
    "incomplete": [
        "Bạn có thể gõ đầy đủ câu hỏi hơn không?",
        "Ví dụ: 'paracetamol uống mấy viên' hoặc 'ibuprofen có tác dụng phụ gì'",
    ],
    "vague_ref": [
        "Bạn đang hỏi về thuốc nào vậy? Cho mình biết tên thuốc nhé.",
        "Tên thuốc thường ghi trên hộp hoặc vỉ thuốc bạn đang cầm.",
    ],
    "clear": [],
}
ALLOWED_AMBIGUITY_TYPES = {"no_drug_found", "incomplete", "vague_ref", "clear"}

OTC_ADVICE_TERMS = (
    "mua thuoc",
    "thuoc cam",
    "thuoc cam cum",
    "thuoc ho",
    "nen tranh",
    "tranh loai nao",
    "loai nao",
    "nen mua",
    "tu van",
)

OTC_CONTEXT_TERMS = (
    "tieu duong",
    "dai thao duong",
    "duong huyet",
    "huyet ap",
    "tang huyet ap",
    "cao huyet ap",
    "benh nen",
    "tim mach",
    "hen",
    "suy than",
    "suy gan",
)


@dataclass
class AmbiguityAssessment:
    is_ambiguous: bool
    ambiguity_type: str
    questions: List[str]
    original_message: str


class QueryAmbiguityService:
    """Detect vague or incomplete medication queries without owning dependencies."""

    def __init__(self, intent_planner: Optional[Any] = None, query_expander: Optional[Any] = None) -> None:
        self.intent_planner = intent_planner
        self.query_expander = query_expander

    async def assess(self, message: str) -> AmbiguityAssessment:
        try:
            llm_assessment = await self._assess_with_llm(message)
            if llm_assessment is not None:
                return llm_assessment
            return self._fallback_assess(message)
        except Exception:
            return self._assessment(False, "clear", message)

    async def _assess_with_llm(self, message: str) -> Optional[AmbiguityAssessment]:
        planner = self.intent_planner
        if planner is None or not getattr(planner, "enabled", False):
            return None
        is_available = getattr(planner, "is_available", None)
        if not callable(is_available) or not is_available():
            return None
        generate = getattr(planner, "_gemini_generate", None)
        if not callable(generate):
            return None

        prompt = f"""
Bạn là hệ thống phân tích câu hỏi thuốc. Phân tích câu hỏi sau và trả về JSON.

Câu hỏi: "{message}"

Trả về JSON với format:
{{
  "is_ambiguous": true/false,
  "ambiguity_type": "no_drug_found" | "incomplete" | "vague_ref" | "clear",
  "reason": "giải thích ngắn"
}}

Quy tắc:
- "no_drug_found": người dùng mô tả triệu chứng/màu sắc/hình dạng mà không có tên thuốc
- "incomplete": câu quá ngắn hoặc thiếu thông tin để hiểu
- "vague_ref": dùng "thuốc này/đó/kia" mà không nêu tên
- "clear": có tên thuốc hoặc hoạt chất cụ thể

Chỉ trả về JSON, không giải thích thêm.
""".strip()
        try:
            text = await generate(prompt, json.dumps({"message": message}, ensure_ascii=False))
            if not text:
                return None
            match = re.search(r"\{.*\}", text, re.DOTALL)
            data = json.loads(match.group(0) if match else text)
            ambiguity_type = str(data.get("ambiguity_type") or "clear")
            if ambiguity_type not in ALLOWED_AMBIGUITY_TYPES:
                return None
            is_ambiguous = bool(data.get("is_ambiguous")) and ambiguity_type != "clear"
            return self._assessment(is_ambiguous, ambiguity_type, message)
        except Exception:
            return None

    def _fallback_assess(self, message: str) -> AmbiguityAssessment:
        normalized = normalize_text(message or "")
        folded = self._fold_vietnamese(message or "")
        if self._looks_like_otc_advice(normalized, folded):
            return self._assessment(False, "clear", message)
        has_drug_term = self._has_drug_term(normalized)
        word_count = len(normalized.split())
        is_incomplete = word_count <= 2
        vague_terms = ["nay", "kia", "do", "vay", "cai do", "cai nay"]
        is_vague_ref = any(term in normalized for term in vague_terms) and not has_drug_term

        if is_incomplete and not has_drug_term:
            ambiguity_type = "incomplete"
        elif is_vague_ref:
            ambiguity_type = "vague_ref"
        elif not has_drug_term and len((message or "").strip()) > 10:
            ambiguity_type = "no_drug_found"
        else:
            ambiguity_type = "clear"
        return self._assessment(ambiguity_type != "clear", ambiguity_type, message)

    def _has_drug_term(self, normalized_message: str) -> bool:
        try:
            expansion_map = getattr(self.query_expander, "expansion_map", None)
            if not expansion_map:
                return False
            return any(term in normalized_message for term in expansion_map.keys())
        except Exception:
            return False

    @staticmethod
    def _assessment(is_ambiguous: bool, ambiguity_type: str, message: str) -> AmbiguityAssessment:
        if ambiguity_type not in ALLOWED_AMBIGUITY_TYPES:
            ambiguity_type = "clear"
            is_ambiguous = False
        return AmbiguityAssessment(
            is_ambiguous=is_ambiguous,
            ambiguity_type=ambiguity_type,
            questions=AMBIGUITY_QUESTIONS.get(ambiguity_type, []),
            original_message=message,
        )

    @staticmethod
    def _fold_vietnamese(text: str) -> str:
        normalized = unicodedata.normalize("NFKD", text or "")
        without_marks = "".join(char for char in normalized if not unicodedata.combining(char))
        return without_marks.replace("đ", "d").replace("Đ", "d").lower()

    @staticmethod
    def _looks_like_otc_advice(normalized: str, folded: str) -> bool:
        has_advice = any(term in normalized or term in folded for term in OTC_ADVICE_TERMS)
        has_context = any(term in normalized or term in folded for term in OTC_CONTEXT_TERMS)
        return has_advice and has_context
