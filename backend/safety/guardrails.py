"""
Cac quy tac bao ve an toan dua tren rule cho OTC va ho tro don thuoc tai Viet Nam.

Cac quy tac nay khong chan doan benh. Chung quyet dinh RAG pipeline co the tra loi,
can hoi them ngu canh con thieu, hay phai huong dan nguoi dung gap bac si.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterable, List
import unicodedata

from backend.models import Citation


class SafetyLevel(str, Enum):
    LOW = "low"
    NEEDS_CONTEXT = "needs_context"
    HIGH = "high"
    EMERGENCY = "emergency"


@dataclass
class SafetyDecision:
    level: SafetyLevel
    should_answer: bool
    message: str = ""
    missing_questions: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


EMERGENCY_TERMS = {
    "kho tho": "Khó thở hoặc tức ngực có thể là dấu hiệu nguy hiểm.",
    "khó thở": "Khó thở hoặc tức ngực có thể là dấu hiệu nguy hiểm.",
    "dau nguc": "Đau ngực cần được đánh giá trực tiếp.",
    "đau ngực": "Đau ngực cần được đánh giá trực tiếp.",
    "co giat": "Co giật là tình huống cấp cứu.",
    "co giật": "Co giật là tình huống cấp cứu.",
    "ngat": "Ngất/lơ mơ cần được khám ngay.",
    "ngất": "Ngất/lơ mơ cần được khám ngay.",
    "lo mo": "Lơ mơ cần được khám ngay.",
    "lơ mơ": "Lơ mơ cần được khám ngay.",
    "qua lieu": "Nghi ngờ quá liều cần xử trí khẩn cấp.",
    "quá liều": "Nghi ngờ quá liều cần xử trí khẩn cấp.",
    "uống nhầm": "Uống nhầm thuốc cần liên hệ y tế ngay.",
    "soc phan ve": "Có thể là phản vệ, cần cấp cứu.",
    "sốc phản vệ": "Có thể là phản vệ, cần cấp cứu.",
    "phu moi": "Phù môi/mặt sau dùng thuốc có thể là phản ứng dị ứng nặng.",
    "phù môi": "Phù môi/mặt sau dùng thuốc có thể là phản ứng dị ứng nặng.",
}

HIGH_RISK_TERMS = {
    "mang thai": "Phụ nữ mang thai cần được bác sĩ/dược sĩ xác nhận trước khi dùng thuốc.",
    "có thai": "Phụ nữ mang thai cần được bác sĩ/dược sĩ xác nhận trước khi dùng thuốc.",
    "cho con bú": "Người đang cho con bú cần được tư vấn cá nhân hóa.",
    "trẻ sơ sinh": "Trẻ sơ sinh cần được nhân viên y tế đánh giá trực tiếp.",
    "suy gan": "Bệnh gan làm thay đổi độ an toàn của nhiều thuốc.",
    "suy thận": "Bệnh thận làm thay đổi liều và độ an toàn của nhiều thuốc.",
    "dị ứng": "Tiền sử dị ứng thuốc cần được kiểm tra kỹ.",
    "di ung": "Tiền sử dị ứng thuốc cần được kiểm tra kỹ.",
    "kháng sinh": "Kháng sinh là thuốc kê đơn, không nên tự dùng.",
    "khang sinh": "Kháng sinh là thuốc kê đơn, không nên tự dùng.",
}

MEDICAL_TERMS = {
    "thuốc",
    "uống",
    "liều",
    "toa",
    "đơn",
    "dược",
    "paracetamol",
    "ibuprofen",
    "aspirin",
    "vitamin",
    "tác dụng phụ",
    "tương tác",
}

MINIMUM_CONTEXT_QUESTIONS = [
    "Người dùng thuốc bao nhiêu tuổi?",
    "Có đang mang thai, cho con bú, dị ứng thuốc, bệnh gan/thận hoặc bệnh nền quan trọng không?",
    "Đang dùng thuốc nào khác hoặc có toa thuốc bác sĩ kê không?",
]


def _norm(text: str) -> str:
    value = (text or "").strip().lower()
    decomposed = unicodedata.normalize("NFD", value)
    without_accents = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    normalized = unicodedata.normalize("NFC", without_accents)
    return " ".join(normalized.split())


def _contains_any(text: str, terms: Iterable[str]) -> bool:
    return any(_norm(term) in text for term in terms)


def _unique_preserve_order(items: Iterable[str]) -> List[str]:
    seen = set()
    unique_items = []
    for item in items:
        if item not in seen:
            seen.add(item)
            unique_items.append(item)
    return unique_items


def evaluate_query_safety(message: str, context: Dict[str, Any] | None = None) -> SafetyDecision:
    text = _norm(message)
    context = context or {}

    emergency_hits = _unique_preserve_order(reason for term, reason in EMERGENCY_TERMS.items() if _norm(term) in text)
    if emergency_hits:
        return SafetyDecision(
            level=SafetyLevel.EMERGENCY,
            should_answer=False,
            message=(
                "Trường hợp này có dấu hiệu nguy hiểm. Vui lòng gọi cấp cứu 115 "
                "hoặc đến cơ sở y tế gần nhất ngay. Bot không nên tư vấn dùng thuốc chi tiết "
                "trong tình huống này."
            ),
            warnings=emergency_hits,
            tags=["red_flag", "urgent_handoff"],
        )

    high_risk_hits = _unique_preserve_order(reason for term, reason in HIGH_RISK_TERMS.items() if _norm(term) in text)
    if high_risk_hits:
        return SafetyDecision(
            level=SafetyLevel.HIGH,
            should_answer=False,
            message=(
                "Câu hỏi có yếu tố rủi ro cao. Tôi không nên tự đưa ra hướng dùng thuốc cụ thể. "
                "Bạn nên hỏi trực tiếp bác sĩ hoặc dược sĩ và cung cấp đầy đủ toa thuốc, tuổi, "
                "bệnh nền, dị ứng và các thuốc đang dùng."
            ),
            warnings=high_risk_hits,
            tags=["high_risk_handoff"],
        )

    is_medical = _contains_any(text, MEDICAL_TERMS)
    has_profile = bool(context.get("patient_profile") or context.get("user_profile"))
    has_prescription_context = "toa" in text or "don" in text or "bac si ke" in text

    if is_medical and not has_profile and not has_prescription_context:
        return SafetyDecision(
            level=SafetyLevel.NEEDS_CONTEXT,
            should_answer=False,
            message=(
                "Để tư vấn an toàn, tôi cần thêm vài thông tin trước khi trả lời về thuốc."
            ),
            missing_questions=MINIMUM_CONTEXT_QUESTIONS,
            warnings=[
                "Không tự ý dùng thuốc kê đơn, đổi liều hoặc ngưng thuốc bác sĩ đã kê.",
            ],
            tags=["needs_patient_context"],
        )

    return SafetyDecision(
        level=SafetyLevel.LOW,
        should_answer=True,
        warnings=[
            "Thông tin chỉ hỗ trợ tham khảo, không thay thế bác sĩ hoặc dược sĩ.",
            "Không tự ý thay đổi liều thuốc trong toa bác sĩ.",
        ],
        tags=["rag_allowed"],
    )


def build_citation_list(results: List[Dict[str, Any]]) -> List[Citation]:
    citations: List[Citation] = []
    for index, result in enumerate(results, 1):
        metadata = result.get("metadata") or {}
        citations.append(
            Citation(
                id=f"S{index}",
                source=str(metadata.get("source") or metadata.get("file") or "Unknown"),
                title=metadata.get("title") or metadata.get("drug_name"),
                url=metadata.get("url"),
                page=metadata.get("page"),
                section=metadata.get("section"),
                updated_at=metadata.get("updated_at") or metadata.get("date"),
                similarity=round(float(result.get("similarity", 0.0)), 3),
            )
        )
    return citations


def validate_rag_evidence(results: List[Dict[str, Any]], min_sources: int = 1) -> SafetyDecision:
    if len(results) < min_sources:
        return SafetyDecision(
            level=SafetyLevel.NEEDS_CONTEXT,
            should_answer=False,
            message=(
                "Tôi chưa tìm thấy nguồn dữ liệu đã kiểm chứng đủ liên quan để trả lời chắc chắn. "
                "Vui lòng hỏi dược sĩ/bác sĩ hoặc bổ sung tên thuốc, hoạt chất, hàm lượng và toa thuốc nếu có."
            ),
            warnings=["Không đủ bằng chứng RAG để trả lời an toàn."],
            tags=["insufficient_evidence"],
        )

    return SafetyDecision(level=SafetyLevel.LOW, should_answer=True)
