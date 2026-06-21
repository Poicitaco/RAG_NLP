"""Evidence-aware guardrails for pharmaceutical RAG answers.

These rules run before and after retrieval. They decide whether the system is
allowed to answer, especially when the question involves children, red flags,
dosage, interactions, pregnancy, chronic disease, or unverified OCR evidence.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterable, List
import re
import unicodedata


class EvidenceAction(str, Enum):
    ALLOW = "allow"
    ALLOW_WITH_CAUTION = "allow_with_caution"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    HANDOFF = "handoff"
    EMERGENCY = "emergency"


class QuestionIntent(str, Enum):
    DRUG_INFO = "drug_info"
    DOSAGE = "dosage"
    INTERACTION = "interaction"
    RECALL = "recall"
    COUNTERFEIT = "counterfeit"
    HIGH_RISK_CONTEXT = "high_risk_context"
    PEDIATRIC_SYMPTOM = "pediatric_symptom"
    EMERGENCY = "emergency"
    GENERAL_SAFETY = "general_safety"


@dataclass
class EvidenceDecision:
    action: EvidenceAction
    intent: QuestionIntent
    should_answer: bool
    message: str
    warnings: List[str] = field(default_factory=list)
    required_sources: List[str] = field(default_factory=list)
    usable_sources: List[str] = field(default_factory=list)
    blocked_sources: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


EMERGENCY_TERMS = {
    "kho tho",
    "dau nguc",
    "nguc trai",
    "co giat",
    "sot cao co giat",
    "ngat",
    "lo mo",
    "soc phan ve",
    "qua lieu",
    "uong nham",
    "te nua nguoi",
    "yeu nua nguoi",
    "nhin mo dot ngot",
    "mat tu dung nhin mo",
    "ho ra mau",
    "tia mau",
    "di tieu ra mau",
    "tieu ra mau",
    "dau dau nhu bua bo",
    "dau bung du doi",
    "dau bung duoi ben phai",
    "vang mat",
    "vang da",
    "vang khe",
    "tim dap thinh thich",
    "sot gan 40",
    "sot 40",
}
HIGH_RISK_TERMS = {
    "mang thai",
    "co thai",
    "bau",
    "cho con bu",
    "tre em",
    "tre so sinh",
    "so sinh",
    "be",
    "con tui",
    "con toi",
    "con nit",
    "tre",
    "3 tuoi",
    "6 tuoi",
    "1 tuoi",
    "6 thang",
    "suy gan",
    "benh gan",
    "suy than",
    "hong than",
    "tieu duong",
    "dai thao duong",
    "huyet ap",
    "nguoi gia",
    "75 tuoi",
    "mai khong khoi",
    "khong khoi",
}
PEDIATRIC_TERMS = {
    "be",
    "con tui",
    "con toi",
    "tre",
    "tre em",
    "tre so sinh",
    "so sinh",
    "con nit",
    "3 tuoi",
    "6 tuoi",
    "1 tuoi",
    "6 thang",
    "15kg",
}
SYMPTOM_TERMS = {
    "ho",
    "sot",
    "nghet mui",
    "so mui",
    "dau",
    "tieu chay",
    "di ngoai",
    "non",
    "mat do",
    "dau tai",
    "viem",
    "loet",
    "ngua",
}
DOSAGE_TERMS = {
    "lieu",
    "lieu dung",
    "cach dung",
    "cach su dung",
    "su dung nhu the nao",
    "dung nhu the nao",
    "dung the nao",
    "uong nhu the nao",
    "uong the nao",
    "uong may vien",
    "dung bao nhieu",
    "uong bao nhieu",
    "ngay may lan",
    "tan suat",
    "nang 15kg",
    "15kg",
    "tang lieu",
    "lieu khang sinh",
}
INTERACTION_TERMS = {"tuong tac", "dung chung", "uong cung", "ket hop", "kem", "them"}
COMMON_DRUG_TERMS = {
    "aspirin",
    "ibuprofen",
    "paracetamol",
    "acetaminophen",
    "panadol",
    "efferalgan",
    "diclofenac",
    "warfarin",
    "augmentin",
    "amoxicillin",
    "metronidazole",
    "levothyroxine",
    "omeprazole",
    "rosuvastatin",
    "ventolin",
    "flixonase",
    "rhinocort",
}
RECALL_TERMS = {"thu hoi", "dinh chi", "khong dat tieu chuan"}
COUNTERFEIT_TERMS = {"gia mao", "thuoc gia", "khong ro nguon goc", "tren mang"}

SAFETY_SOURCES = {"dav_recall", "canhgiacduoc", "otc_condition_guardrail", "ddinter"}
REGISTRY_SOURCES = {"dav_all", "dav_otc"}
PDF_SOURCES = {"dav_pdf"}
OCR_SOURCES = {"dav_pdf_ocr"}
HIGH_RISK_INTENTS = {
    QuestionIntent.DOSAGE,
    QuestionIntent.INTERACTION,
    QuestionIntent.HIGH_RISK_CONTEXT,
    QuestionIntent.PEDIATRIC_SYMPTOM,
    QuestionIntent.EMERGENCY,
}


def normalize_text(text: str) -> str:
    value = (text or "").replace("Đ", "D").replace("đ", "d").lower()
    decomposed = unicodedata.normalize("NFD", value)
    return " ".join(
        "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn").split()
    )


def contains_any(text: str, terms: Iterable[str]) -> bool:
    normalized = normalize_text(text)
    tokens = set(re.findall(r"[a-z0-9]+", normalized))
    for term in terms:
        normalized_term = normalize_text(term)
        if " " in normalized_term:
            if re.search(r"\b" + re.escape(normalized_term) + r"\b", normalized):
                return True
        elif normalized_term in tokens:
            return True
    return False


def classify_question_intent(question: str) -> QuestionIntent:
    normalized = normalize_text(question)
    if contains_any(question, EMERGENCY_TERMS):
        return QuestionIntent.EMERGENCY
    if contains_any(question, COUNTERFEIT_TERMS):
        return QuestionIntent.COUNTERFEIT
    if contains_any(question, RECALL_TERMS):
        return QuestionIntent.RECALL
    if contains_any(question, PEDIATRIC_TERMS) and contains_any(question, SYMPTOM_TERMS):
        return QuestionIntent.PEDIATRIC_SYMPTOM
    drug_mentions = sum(1 for term in COMMON_DRUG_TERMS if term in normalized)
    if contains_any(question, INTERACTION_TERMS) and drug_mentions >= 1:
        return QuestionIntent.INTERACTION
    if "cung" in normalized and drug_mentions >= 2:
        return QuestionIntent.INTERACTION
    if contains_any(question, DOSAGE_TERMS):
        return QuestionIntent.DOSAGE
    if contains_any(question, HIGH_RISK_TERMS):
        return QuestionIntent.HIGH_RISK_CONTEXT
    if contains_any(question, {"canh bao", "tac dung phu", "nguy hiem", "di ung", "dau bao tu"}):
        return QuestionIntent.GENERAL_SAFETY
    return QuestionIntent.DRUG_INFO


def metadata_source(metadata: Dict[str, Any]) -> str:
    return str(metadata.get("source") or metadata.get("source_dataset") or "")


def result_metadata(result: Dict[str, Any]) -> Dict[str, Any]:
    return result.get("metadata") or {}


def result_source(result: Dict[str, Any]) -> str:
    return metadata_source(result_metadata(result))


def result_type(result: Dict[str, Any]) -> str:
    return str(result_metadata(result).get("type") or "")


def result_text(result: Dict[str, Any]) -> str:
    metadata = result_metadata(result)
    fields = [
        result.get("document_preview"),
        result.get("document"),
        metadata.get("title"),
        metadata.get("drug_name"),
        metadata.get("active_ingredients"),
        metadata.get("main_ingredient"),
    ]
    return normalize_text(" ".join(str(value) for value in fields if value))


def mentioned_common_drugs(question: str) -> List[str]:
    normalized = normalize_text(question)
    return [term for term in COMMON_DRUG_TERMS if term in normalized]


def is_relevant_to_question_drugs(result: Dict[str, Any], question_drugs: List[str]) -> bool:
    if not question_drugs:
        return True
    text = result_text(result)
    return any(term in text for term in question_drugs)


def trust_level(result: Dict[str, Any]) -> str:
    return str(result_metadata(result).get("trust_level") or "official_registry")


def is_unverified_ocr(result: Dict[str, Any]) -> bool:
    metadata = result_metadata(result)
    return (
        result_source(result) in OCR_SOURCES
        or trust_level(result) == "unverified_ocr"
        or bool(metadata.get("requires_human_review"))
    )


def evidence_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    sources = [result_source(row) for row in results]
    types = [result_type(row) for row in results]
    return {
        "sources": sources,
        "types": types,
        "has_safety_source": any(source in SAFETY_SOURCES for source in sources),
        "has_registry_source": any(source in REGISTRY_SOURCES for source in sources),
        "has_pdf_source": any(source in PDF_SOURCES for source in sources),
        "has_ocr_source": any(source in OCR_SOURCES for source in sources),
        "has_verified_non_ocr": any(not is_unverified_ocr(row) for row in results),
        "has_verified_dosage": any(
            not is_unverified_ocr(row) and result_type(row) == "dosage" for row in results
        ),
        "has_verified_interaction": any(
            not is_unverified_ocr(row) and result_type(row) == "interaction" for row in results
        ),
        "has_verified_safety": any(
            not is_unverified_ocr(row)
            and (result_type(row) in {"safety", "safety_article", "safety_recall"} or result_source(row) in SAFETY_SOURCES)
            for row in results
        ),
        "ocr_count": sum(1 for row in results if is_unverified_ocr(row)),
    }


def _early_handoff(intent: QuestionIntent, summary: Dict[str, Any]) -> EvidenceDecision | None:
    if intent == QuestionIntent.EMERGENCY:
        return EvidenceDecision(
            action=EvidenceAction.EMERGENCY,
            intent=intent,
            should_answer=False,
            message=(
                "Có dấu hiệu cấp cứu hoặc nguy cơ nặng. Không nên trả lời bằng RAG; "
                "cần hướng dẫn người dùng gọi 115 hoặc đến cơ sở y tế gần nhất."
            ),
            warnings=["Emergency/red-flag question must bypass RAG answer generation."],
            metadata=summary,
        )
    if intent == QuestionIntent.PEDIATRIC_SYMPTOM:
        return EvidenceDecision(
            action=EvidenceAction.HANDOFF,
            intent=intent,
            should_answer=False,
            message=(
                "Câu hỏi liên quan trẻ nhỏ và triệu chứng bệnh. Không nên tự gợi ý thuốc "
                "khi chưa có tuổi/cân nặng/chẩn đoán và nguồn nhi khoa phù hợp."
            ),
            warnings=["Pediatric symptom question must be handed off unless a vetted pediatric protocol exists."],
            metadata=summary,
        )
    return None


def evaluate_evidence(question: str, results: List[Dict[str, Any]]) -> EvidenceDecision:
    intent = classify_question_intent(question)
    summary = evidence_summary(results)
    sources = list(dict.fromkeys(summary["sources"]))
    question_drugs = mentioned_common_drugs(question)
    warnings: List[str] = []

    early = _early_handoff(intent, summary)
    if early is not None:
        early.usable_sources = sources
        return early

    if not results:
        return EvidenceDecision(
            action=EvidenceAction.INSUFFICIENT_EVIDENCE,
            intent=intent,
            should_answer=False,
            message="Không có bằng chứng RAG đủ liên quan để trả lời an toàn.",
            warnings=["No retrieved evidence."],
            metadata=summary,
        )

    if summary["has_ocr_source"]:
        warnings.append(
            "Có bằng chứng OCR chưa xác minh; không được dùng để kết luận chắc chắn về liều, số liệu hoặc tương tác."
        )

    if intent in {QuestionIntent.RECALL, QuestionIntent.COUNTERFEIT, QuestionIntent.GENERAL_SAFETY}:
        if summary["has_safety_source"]:
            return EvidenceDecision(
                action=EvidenceAction.ALLOW_WITH_CAUTION if warnings else EvidenceAction.ALLOW,
                intent=intent,
                should_answer=True,
                message="Có bằng chứng safety/recall phù hợp để trả lời kèm citation.",
                warnings=warnings,
                required_sources=sorted(SAFETY_SOURCES),
                usable_sources=sources,
                metadata=summary,
            )
        return EvidenceDecision(
            action=EvidenceAction.INSUFFICIENT_EVIDENCE,
            intent=intent,
            should_answer=False,
            message=(
                "Câu hỏi an toàn/cảnh báo cần nguồn safety đáng tin cậy. "
                "Bằng chứng hiện tại chưa đủ để kết luận."
            ),
            warnings=warnings + ["Missing trusted safety source."],
            required_sources=sorted(SAFETY_SOURCES),
            usable_sources=sources,
            metadata=summary,
        )

    if intent in HIGH_RISK_INTENTS:
        verified_relevant = [
            row
            for row in results
            if not is_unverified_ocr(row) and is_relevant_to_question_drugs(row, question_drugs)
        ]
        if intent == QuestionIntent.DOSAGE:
            has_relevant_verified = any(
                result_type(row) in {"dosage", "safety", "safety_article", "safety_recall"}
                or result_source(row) in SAFETY_SOURCES
                for row in verified_relevant
            )
        elif intent == QuestionIntent.INTERACTION:
            has_relevant_verified = any(
                result_type(row) in {"interaction", "safety", "safety_article", "safety_recall"}
                or result_source(row) in SAFETY_SOURCES
                for row in verified_relevant
            )
        else:
            has_relevant_verified = any(
                result_type(row) in {"safety", "safety_article", "safety_recall"}
                or result_source(row) in SAFETY_SOURCES | PDF_SOURCES
                for row in verified_relevant
            )

        if not has_relevant_verified:
            return EvidenceDecision(
                action=EvidenceAction.HANDOFF,
                intent=intent,
                should_answer=False,
                message=(
                    "Câu hỏi rủi ro cao chưa có bằng chứng đúng loại nguồn đã xác minh. "
                    "Nên chuyển người dùng gặp bác sĩ/dược sĩ."
                ),
                warnings=warnings + ["High-risk question lacks verified relevant evidence."],
                blocked_sources=[source for source in sources if source in OCR_SOURCES],
                usable_sources=sources,
                metadata=summary,
            )
        return EvidenceDecision(
            action=EvidenceAction.ALLOW_WITH_CAUTION,
            intent=intent,
            should_answer=True,
            message=(
                "Có thể trả lời mức thông tin chung kèm citation, nhưng không đưa ra liều cá nhân hóa "
                "hoặc thay đổi toa thuốc."
            ),
            warnings=warnings
            + [
                "High-risk answer must include handoff language and avoid personalized dosing."
            ],
            usable_sources=sources,
            metadata=summary,
        )

    if intent == QuestionIntent.DRUG_INFO:
        if summary["has_registry_source"] or summary["has_verified_non_ocr"]:
            return EvidenceDecision(
                action=EvidenceAction.ALLOW_WITH_CAUTION if warnings else EvidenceAction.ALLOW,
                intent=intent,
                should_answer=True,
                message="Có bằng chứng phù hợp để trả lời thông tin định danh thuốc kèm citation.",
                warnings=warnings,
                usable_sources=sources,
                metadata=summary,
            )

    return EvidenceDecision(
        action=EvidenceAction.INSUFFICIENT_EVIDENCE,
        intent=intent,
        should_answer=False,
        message="Bằng chứng hiện tại chưa đủ tin cậy hoặc chưa đúng loại nguồn cho câu hỏi.",
        warnings=warnings,
        usable_sources=sources,
        metadata=summary,
    )
