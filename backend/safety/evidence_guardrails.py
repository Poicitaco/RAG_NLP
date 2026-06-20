"""Evidence-aware guardrails for pharmaceutical RAG answers.

These rules run after retrieval. They decide whether the retrieved evidence is
appropriate for the user's question, especially when the evidence is OCR-derived
or when the question asks about dosage, interactions, pregnancy, children,
overdose, recall, or counterfeit products.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterable, List
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
    "co giat",
    "ngat",
    "lo mo",
    "soc phan ve",
    "qua lieu",
    "uong nham",
}
HIGH_RISK_TERMS = {
    "mang thai",
    "co thai",
    "cho con bu",
    "tre em",
    "tre so sinh",
    "suy gan",
    "suy than",
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
}
INTERACTION_TERMS = {"tuong tac", "dung chung", "uong cung", "ket hop"}
COMMON_DRUG_TERMS = {
    "aspirin",
    "ibuprofen",
    "paracetamol",
    "acetaminophen",
    "cloramphenicol",
    "cefaclor",
    "aceclofenac",
}
RECALL_TERMS = {"thu hoi", "dinh chi", "khong dat tieu chuan"}
COUNTERFEIT_TERMS = {"gia mao", "thuoc gia", "khong ro nguon goc"}

SAFETY_SOURCES = {"dav_recall", "canhgiacduoc"}
REGISTRY_SOURCES = {"dav_all", "dav_otc"}
PDF_SOURCES = {"dav_pdf"}
OCR_SOURCES = {"dav_pdf_ocr"}
HIGH_RISK_INTENTS = {
    QuestionIntent.DOSAGE,
    QuestionIntent.INTERACTION,
    QuestionIntent.HIGH_RISK_CONTEXT,
    QuestionIntent.EMERGENCY,
}


def normalize_text(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", (text or "").lower())
    return " ".join(
        "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn").split()
    )


def contains_any(text: str, terms: Iterable[str]) -> bool:
    normalized = normalize_text(text)
    return any(term in normalized for term in terms)


def classify_question_intent(question: str) -> QuestionIntent:
    normalized = normalize_text(question)
    if contains_any(question, EMERGENCY_TERMS):
        return QuestionIntent.EMERGENCY
    if contains_any(question, COUNTERFEIT_TERMS):
        return QuestionIntent.COUNTERFEIT
    if contains_any(question, RECALL_TERMS):
        return QuestionIntent.RECALL
    if contains_any(question, HIGH_RISK_TERMS):
        return QuestionIntent.HIGH_RISK_CONTEXT
    drug_mentions = sum(1 for term in COMMON_DRUG_TERMS if term in normalized)
    if contains_any(question, INTERACTION_TERMS) or ("cung" in normalized and drug_mentions >= 2):
        return QuestionIntent.INTERACTION
    if contains_any(question, DOSAGE_TERMS):
        return QuestionIntent.DOSAGE
    if contains_any(question, {"canh bao", "tac dung phu", "nguy hiem", "di ung"}):
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


def evaluate_evidence(question: str, results: List[Dict[str, Any]]) -> EvidenceDecision:
    intent = classify_question_intent(question)
    summary = evidence_summary(results)
    sources = list(dict.fromkeys(summary["sources"]))
    question_drugs = mentioned_common_drugs(question)
    warnings: List[str] = []

    if intent == QuestionIntent.EMERGENCY:
        return EvidenceDecision(
            action=EvidenceAction.EMERGENCY,
            intent=intent,
            should_answer=False,
            message=(
                "Co dau hieu cap cuu hoac nguy co qua lieu. Khong nen tra loi bang RAG; "
                "can huong dan nguoi dung goi 115 hoac den co so y te gan nhat."
            ),
            warnings=["Emergency/red-flag question must bypass RAG answer generation."],
            usable_sources=sources,
            metadata=summary,
        )

    if not results:
        return EvidenceDecision(
            action=EvidenceAction.INSUFFICIENT_EVIDENCE,
            intent=intent,
            should_answer=False,
            message="Khong co bang chung RAG du lien quan de tra loi an toan.",
            warnings=["No retrieved evidence."],
            metadata=summary,
        )

    if summary["has_ocr_source"]:
        warnings.append(
            "Co bang chung OCR chua xac minh; khong duoc dung de ket luan chac chan ve lieu, so lieu hoac tuong tac."
        )

    if intent in {QuestionIntent.RECALL, QuestionIntent.COUNTERFEIT, QuestionIntent.GENERAL_SAFETY}:
        if summary["has_safety_source"]:
            return EvidenceDecision(
                action=EvidenceAction.ALLOW_WITH_CAUTION if warnings else EvidenceAction.ALLOW,
                intent=intent,
                should_answer=True,
                message="Co bang chung safety/recall phu hop de tra loi kem citation.",
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
                "Cau hoi ve thu hoi/canh bao/thuoc gia can nguon DAV recall hoac CanhGiacDuoc. "
                "Bang chung hien tai chua du de ket luan."
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
                    "Cau hoi rui ro cao chua co bang chung dung loai nguon da xac minh. "
                    "Nen chuyen nguoi dung gap bac si/duoc si."
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
                "Co the tra loi muc thong tin chung kem citation, nhung khong dua ra lieu ca nhan hoa "
                "hoac thay doi toa thuoc."
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
                message="Co bang chung phu hop de tra loi thong tin dinh danh thuoc kem citation.",
                warnings=warnings,
                usable_sources=sources,
                metadata=summary,
            )

    return EvidenceDecision(
        action=EvidenceAction.INSUFFICIENT_EVIDENCE,
        intent=intent,
        should_answer=False,
        message="Bang chung hien tai chua du tin cay hoac chua dung loai nguon cho cau hoi.",
        warnings=warnings,
        usable_sources=sources,
        metadata=summary,
    )
