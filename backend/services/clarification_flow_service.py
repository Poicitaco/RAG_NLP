"""Tiered Clarification Flow — hỏi từng câu một theo độ ưu tiên.

Flow: age → conditions → medications/allergies → answer
Mỗi turn chỉ hỏi 1 câu thay vì dump tất cả cùng lúc.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# Thứ tự ưu tiên: thiếu cái nào hỏi cái đó trước
SLOT_PRIORITY = ["age", "age_or_age_months", "conditions_confirmed",
                 "allergies_confirmed", "current_medications_confirmed",
                 "pregnancy_breastfeeding_confirmed"]

# weight_kg chỉ hỏi khi là trẻ em (xử lý riêng trong check_clarification)
MAX_CLARIFICATION_TURNS = 2  # Chỉ hỏi tối đa 2 câu rồi trả lời luôn

SLOT_QUESTIONS = {
    "age": "Bạn (hoặc người dùng thuốc) bao nhiêu tuổi?",
    "age_or_age_months": "Người dùng thuốc bao nhiêu tuổi? (Nếu là trẻ nhỏ, cho biết số tháng tuổi)",
    "weight_kg": "Cân nặng của bé là bao nhiêu kg?",
    "conditions_confirmed": "Bạn có bệnh nền nào không — ví dụ huyết áp, tiểu đường, dạ dày, gan/thận?",
    "allergies_confirmed": "Bạn có từng dị ứng với thuốc nào không?",
    "current_medications_confirmed": "Bạn đang dùng thuốc gì khác không?",
    "pregnancy_breastfeeding_confirmed": "Bạn có đang mang thai hoặc cho con bú không?",
}

SLOT_SUGGESTIONS = {
    "age": ["Dưới 12 tuổi", "12–60 tuổi", "Trên 60 tuổi"],
    "age_or_age_months": ["Dưới 1 tuổi", "1–5 tuổi", "6–12 tuổi", "Trên 12 tuổi"],
    "weight_kg": [],
    "conditions_confirmed": ["Không có bệnh nền", "Huyết áp", "Tiểu đường", "Đau dạ dày", "Bệnh gan/thận", "Hen suyễn"],
    "allergies_confirmed": ["Không có dị ứng", "Có dị ứng thuốc"],
    "current_medications_confirmed": ["Không đang dùng thuốc khác", "Có đang dùng thuốc khác"],
    "pregnancy_breastfeeding_confirmed": ["Không", "Đang mang thai", "Đang cho con bú"],
}


@dataclass
class ClarificationResult:
    should_ask: bool
    next_slot: str = ""
    question: str = ""
    suggestions: List[str] = field(default_factory=list)
    missing_slots: List[str] = field(default_factory=list)


def _is_missing(patient_ctx: Dict[str, Any], slot: str) -> bool:
    val = patient_ctx.get(slot)
    if slot == "age_or_age_months":
        return patient_ctx.get("age") is None and patient_ctx.get("age_months") is None
    if slot in ("conditions_confirmed", "allergies_confirmed",
                "current_medications_confirmed", "pregnancy_breastfeeding_confirmed"):
        return not bool(val)
    return val is None or val == []


def check_clarification(
    missing_slots: List[str],
    patient_ctx: Dict[str, Any],
    already_asked: List[str],
) -> ClarificationResult:
    """Trả về câu hỏi tiếp theo cần hỏi (1 câu), hoặc should_ask=False nếu đủ."""
    # Đã hỏi đủ số lượt tối đa → không hỏi thêm
    if len(already_asked) >= MAX_CLARIFICATION_TURNS:
        return ClarificationResult(should_ask=False)

    is_pediatric = (
        patient_ctx.get("age_months") is not None
        or (patient_ctx.get("age") is not None and int(patient_ctx.get("age", 99)) < 12)
        or "age_or_age_months" in missing_slots
    )

    # Lọc slots: weight_kg chỉ hỏi khi là trẻ em
    filtered_slots = [
        s for s in missing_slots
        if s not in already_asked
        and _is_missing(patient_ctx, s)
        and (s != "weight_kg" or is_pediatric)
        and s in SLOT_PRIORITY  # chỉ hỏi slots đã định nghĩa
    ]
    ordered = sorted(filtered_slots, key=lambda s: SLOT_PRIORITY.index(s) if s in SLOT_PRIORITY else 99)

    if not ordered:
        return ClarificationResult(should_ask=False)
    next_slot = ordered[0]
    return ClarificationResult(
        should_ask=True,
        next_slot=next_slot,
        question=SLOT_QUESTIONS.get(next_slot, "Bạn có thể cung cấp thêm thông tin không?"),
        suggestions=SLOT_SUGGESTIONS.get(next_slot, []),
        missing_slots=ordered,
    )
