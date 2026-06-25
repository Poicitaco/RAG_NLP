"""Pipeline retrieval cho Safe RAG — BM25 + Chroma hybrid search.

Chua: ham retrieve(), cac ham filter/boost/rank ket qua retrieval.
Duoc tach ra tu safe_rag_service.py de de maintain va test rieng.
"""
from __future__ import annotations

import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional

from backend.safety.evidence_guardrails import (
    is_unverified_ocr,
    mentioned_common_drugs,
    normalize_text,
)

ROOT_DIR = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = ROOT_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from hybrid_search_rag import chroma_search, combine_results, load_bm25_index  # noqa: E402
from smoke_search_bm25 import search as bm25_search  # noqa: E402


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

INTERACTION_FAST_PATH_CUES = (
    "tuong tac", "tương tác", "tac",
    "uong chung", "uống chung", "dung chung", "dùng chung", "chung",
    "uong cung", "uống cùng", "dung cung", "dùng cùng", "cung",
    "phoi hop", "phối hợp", "phoi",
    "ket hop", "kết hợp", "ket",
    "co sao khong", "có sao không", "sao kh",
    "co duoc khong", "có được không",
)

SOURCE_PRIORITY = {
    "dav_recall": 0,
    "canhgiacduoc": 1,
    "dav_all": 2,
    "dav_otc": 2,
    "trungtamthuoc_duocthu": 3,
    "ddinter": 2,
    "otc_condition_guardrail": 0,
    "dav_pdf": 3,
    "dav_pdf_ocr": 5,
}

CARDIAC_SPECIALTY_TERMS = {
    "milrinone", "milrinon", "lidocain", "lidocaine", "digoxin",
    "amiodaron", "amiodarone", "dobutamin", "dobutamine",
    "dopamin", "dopamine", "norepinephrin", "norepinephrine",
    "epinephrin", "epinephrine", "procainamid", "procainamide",
    "disopyramid", "disopyramide", "mexiletin", "mexiletine",
    "propafenon", "propafenone", "flecainid", "flecainide",
    "verapamil", "ivabradin", "ivabradine",
}

CARDIAC_SECTION_TERMS = {
    "he tim mach", "thuoc dieu tri tim", "chong loan nhip",
    "kich thich tim", "gian mach dung trong benh tim", "thuoc tim mach",
}

OTC_CATEGORY_METADATA_FIELDS = ("target_group", "otc_category")

ENTITY_AWARE_CANONICAL_TERMS = {
    "alendronic": [
        "alendronic", "alendronate", "alendron",
        "acid alendronic", "alendronic acid", "bisphosphonate",
        "loang xuong", "loãng xương",
    ],
    "zinc_supplement": [
        "kem", "zinc", "zinc gluconate", "zinc sulfate",
        "zinc sulphate", "bo sung kem",
    ],
}

INDICATION_QUERY_TERMS = (
    "dung de lam gi", "dung lam gi", "cong dung", "chi dinh",
    "tri gi", "chua gi", "de lam gi", "tac dung gi",
)

INDICATION_TEXT_TERMS = (
    "chi dinh", "cong dung", "ha sot", "giam dau",
    "thuoc ha sot", "thuoc giam dau",
)

OTC_CONTEXT_QUERY_TERMS = (
    "mua thuoc", "thuoc cam", "thuoc cam cum", "thuoc ho",
    "nen tranh", "tranh loai nao", "loai nao", "nen mua", "tu van",
)

CHRONIC_CONTEXT_TERMS = (
    "tieu duong", "dai thao duong", "duong huyet",
    "huyet ap", "tang huyet ap", "cao huyet ap", "benh nen",
    "tim mach", "hen", "suy than", "suy gan",
)


# ---------------------------------------------------------------------------
# Text utility
# ---------------------------------------------------------------------------

def _lay_metadata(row: Dict[str, Any]) -> Dict[str, Any]:
    return row.get("metadata") or {}


def _lay_nguon(row: Dict[str, Any]) -> str:
    metadata = _lay_metadata(row)
    return str(metadata.get("source") or metadata.get("source_dataset") or row.get("source") or "")


def _gep_text_row(row: Dict[str, Any]) -> str:
    metadata = _lay_metadata(row)
    values = [
        row.get("document_preview"),
        row.get("document"),
        metadata.get("title"),
        metadata.get("drug_name"),
        metadata.get("active_ingredients"),
        metadata.get("main_ingredient"),
    ]
    return normalize_text(" ".join(str(v) for v in values if v))


def _gep_full_text_row(row: Dict[str, Any]) -> str:
    metadata = _lay_metadata(row)
    return " ".join(
        str(v)
        for v in [
            row.get("document_preview"),
            row.get("document"),
            metadata.get("title"),
            metadata.get("drug_name"),
            metadata.get("active_ingredient"),
            metadata.get("active_ingredients"),
            metadata.get("main_ingredient"),
            metadata.get("section"),
            metadata.get("section_title"),
            metadata.get("slug"),
        ]
        if v
    )


def _gep_folded(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value or "")
    without_marks = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return without_marks.replace("đ", "d").replace("Đ", "d").lower()


def _chua_tu_khoa(value: str, terms: tuple) -> bool:
    candidates = (normalize_text(value), _gep_folded(value), (value or "").lower())
    return any(term in candidate for candidate in candidates for term in terms)


def _khop_normalized(text: str, terms: List[str]) -> bool:
    normalized = normalize_text(text)
    return any(normalize_text(term) in normalized for term in terms if term)


def _gep_metadata_text(metadata: Dict[str, Any], fields: List[str]) -> str:
    return " ".join(str(metadata.get(f) or "") for f in fields)


# ---------------------------------------------------------------------------
# Query classifiers
# ---------------------------------------------------------------------------

def la_query_otc_context(question: str) -> bool:
    return _chua_tu_khoa(question, OTC_CONTEXT_QUERY_TERMS) and _chua_tu_khoa(question, CHRONIC_CONTEXT_TERMS)


def la_query_chi_dinh(question: str) -> bool:
    return _chua_tu_khoa(question, INDICATION_QUERY_TERMS)


def la_row_chi_dinh(row: Dict[str, Any]) -> bool:
    metadata = _lay_metadata(row)
    section = normalize_text(str(metadata.get("section") or ""))
    row_type = normalize_text(str(metadata.get("type") or ""))
    text = f"{_gep_text_row(row)} {_gep_full_text_row(row)}"
    return (
        section == "indications"
        or row_type == "indication"
        or _chua_tu_khoa(text, INDICATION_TEXT_TERMS)
    )


def la_row_chi_registry(row: Dict[str, Any]) -> bool:
    metadata = _lay_metadata(row)
    if _lay_nguon(row) not in {"dav_all", "dav_otc"}:
        return False
    section = normalize_text(str(metadata.get("section") or ""))
    row_type = normalize_text(str(metadata.get("type") or ""))
    return section in {"identity", "registration", "manufacturer", "documents"} or row_type == "drug_info"


def co_finding_otc_benh_nen(graph_result: Dict[str, Any]) -> bool:
    return any(
        finding.get("type") == "condition_otc_caution"
        for finding in graph_result.get("findings") or []
    )


def la_interaction_fast_path(message: str, graph_safety: Any) -> bool:
    candidates = (normalize_text(message), (message or "").lower())
    if not any(cue in text for text in candidates for cue in INTERACTION_FAST_PATH_CUES):
        return False
    return len(graph_safety.detect_query_drugs(message)) >= 2


# ---------------------------------------------------------------------------
# Hard filter
# ---------------------------------------------------------------------------

def _ly_do_filter_rule(row: Dict[str, Any], rule_context: Optional[Dict[str, Any]]) -> Optional[str]:
    if not rule_context or not rule_context.get("matched"):
        return None

    metadata = _lay_metadata(row)
    section_text = _gep_metadata_text(metadata, ["section", "section_title", "type", "slug"])
    document_text = _gep_full_text_row(row)
    avoid_terms = list(rule_context.get("must_avoid_sections_in_rag") or [])
    if avoid_terms and _khop_normalized(section_text + " " + document_text, avoid_terms):
        return "rule_must_avoid_section"

    target_group = normalize_text(str(rule_context.get("target_otc_group") or ""))
    if target_group and _lay_nguon(row) == "otc_condition_guardrail":
        category_values = [
            normalize_text(str(metadata.get(f) or ""))
            for f in OTC_CATEGORY_METADATA_FIELDS
        ]
        if target_group not in category_values:
            return "wrong_otc_target_group"

    if target_group == "zinc_supplement":
        normalized_text = normalize_text(document_text)
        if any(term in normalized_text for term in CARDIAC_SPECIALTY_TERMS):
            return "zinc_query_cardiac_specialty_noise"
        if any(term in normalize_text(section_text) for term in CARDIAC_SECTION_TERMS):
            return "zinc_query_cardiac_section_noise"

    return None


def _lay_entity_filter_terms(question: str, rule_context: Optional[Dict[str, Any]]) -> List[str]:
    normalized_question = normalize_text(question)
    terms: List[str] = []
    target_group = normalize_text(str((rule_context or {}).get("target_otc_group") or ""))
    if target_group and target_group in ENTITY_AWARE_CANONICAL_TERMS:
        terms.extend(ENTITY_AWARE_CANONICAL_TERMS[target_group])
    if any(term in normalized_question for term in ("alendronic", "alendronate", "alendron", "loang xuong")):
        terms.extend(ENTITY_AWARE_CANONICAL_TERMS["alendronic"])
    if target_group and target_group not in ENTITY_AWARE_CANONICAL_TERMS:
        terms.append(target_group)
    return list(dict.fromkeys(normalize_text(term) for term in terms if str(term).strip()))


def _ly_do_entity_filter(row: Dict[str, Any], entity_terms: List[str]) -> Optional[str]:
    if not entity_terms:
        return None
    searchable = normalize_text(_gep_full_text_row(row))
    if any(term and term in searchable for term in entity_terms):
        return None
    return "entity_aware_keyword_mismatch"


def loc_cung_ket_qua(
    rows: List[Dict[str, Any]],
    rule_context: Optional[Dict[str, Any]],
    question: str = "",
) -> List[Dict[str, Any]]:
    """Loc bo cac row khong phu hop voi rule_context hoac entity terms."""
    entity_terms = _lay_entity_filter_terms(question, rule_context)
    if (not rule_context or not rule_context.get("matched")) and not entity_terms:
        return rows
    filtered = []
    for row in rows:
        reason = _ly_do_filter_rule(row, rule_context)
        if not reason:
            reason = _ly_do_entity_filter(row, entity_terms)
        if reason:
            continue
        filtered.append(row)
    return filtered


# ---------------------------------------------------------------------------
# Boost / rank policies
# ---------------------------------------------------------------------------

def ap_dung_chinh_sach_chi_dinh(question: str, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Boost rows chi dinh khi query hoi ve cong dung thuoc."""
    if not la_query_chi_dinh(question):
        return rows

    adjusted: List[Dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        boost = 0.0
        if la_row_chi_dinh(item):
            boost += 4.0
        if _lay_nguon(item) == "trungtamthuoc_duocthu" and la_row_chi_dinh(item):
            boost += 1.0
        if la_row_chi_registry(item):
            boost -= 1.5
        item["hybrid_score"] = round(float(item.get("hybrid_score") or item.get("score") or 0.0) + boost, 6)
        if boost:
            item["indication_policy_boost"] = round(boost, 4)
        adjusted.append(item)

    adjusted.sort(key=lambda r: r.get("hybrid_score") or 0.0, reverse=True)
    for rank, row in enumerate(adjusted, 1):
        row["rank"] = rank
    return adjusted


def ap_dung_chinh_sach_rule(
    rows: List[Dict[str, Any]],
    rule_context: Optional[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Boost rows phu hop voi rule OTC context (e.g. benh nen + thuoc cam)."""
    if not rule_context or not rule_context.get("matched"):
        return rows

    avoid_terms = list(rule_context.get("must_avoid_sections_in_rag") or [])
    priority_terms = list(rule_context.get("priority_otc_ingredients") or [])
    target_group = normalize_text(str(rule_context.get("target_otc_group") or ""))
    adjusted: List[Dict[str, Any]] = []

    for row in rows:
        if _ly_do_filter_rule(row, rule_context):
            continue
        metadata = _lay_metadata(row)
        section_text = " ".join(
            str(metadata.get(f) or "")
            for f in ("title", "section", "section_title", "type", "slug")
        )
        full_text = section_text + " " + str(row.get("document_preview") or row.get("document") or "")
        nguon = _lay_nguon(row)
        la_matrix_guardrail = nguon == "otc_condition_guardrail" and target_group in normalize_text(full_text)
        if avoid_terms and _khop_normalized(section_text, avoid_terms) and not la_matrix_guardrail:
            continue

        item = dict(row)
        boost = 0.0
        if la_matrix_guardrail:
            boost += 3.0
        if priority_terms and _khop_normalized(full_text, priority_terms):
            boost += 1.2
        if boost:
            item["hybrid_score"] = round(float(item.get("hybrid_score") or 0.0) + boost, 6)
            item["matrix_policy_boost"] = round(boost, 4)
        adjusted.append(item)

    adjusted.sort(key=lambda r: r.get("hybrid_score") or 0.0, reverse=True)
    for rank, row in enumerate(adjusted, 1):
        row["rank"] = rank
    return adjusted


def xep_hang_de_tra_loi(question: str, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sap xep ket qua retrieval de chon vao cau tra loi cuoi."""
    question_drugs = mentioned_common_drugs(question)
    indication_question = la_query_chi_dinh(question)

    def key(row: Dict[str, Any]) -> tuple:
        text = _gep_text_row(row)
        drug_match = 0 if not question_drugs or any(term in text for term in question_drugs) else 1
        indication_match = 0 if indication_question and la_row_chi_dinh(row) else 1
        registry_penalty = 1 if indication_question and la_row_chi_registry(row) else 0
        ocr_penalty = 1 if is_unverified_ocr(row) and not (indication_question and la_row_chi_dinh(row)) else 0
        return (
            drug_match,
            indication_match,
            registry_penalty,
            ocr_penalty,
            SOURCE_PRIORITY.get(_lay_nguon(row), 4),
            row.get("rank") or 999,
        )

    return sorted(results, key=key)


def chon_rows_cho_tra_loi(
    graph_result: Dict[str, Any],
    ranked: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Chon rows phu hop nhat dua tren graph findings."""
    findings = graph_result.get("findings") or []
    if not findings:
        return ranked

    preferred_sources = set()
    preferred_types = set()
    exact_interaction_pairs = []
    for finding in findings:
        if finding.get("type") == "condition_otc_caution":
            preferred_sources.add("otc_condition_guardrail")
            preferred_types.add("condition_guardrail")
        elif finding.get("type") == "drug_drug_interaction":
            preferred_sources.add("ddinter")
            preferred_types.add("interaction")
            left = normalize_text(str(finding.get("drug_a") or ""))
            right = normalize_text(str(finding.get("drug_b") or ""))
            if left and right:
                exact_interaction_pairs.append((left, right))

    exact_rows = []
    for row in ranked:
        if _lay_nguon(row) != "ddinter":
            continue
        text = _gep_text_row(row)
        for left, right in exact_interaction_pairs:
            if left in text and right in text:
                exact_rows.append(row)
                break
    if exact_rows:
        return exact_rows

    selected = [
        row
        for row in ranked
        if _lay_nguon(row) in preferred_sources or str(_lay_metadata(row).get("type") or "") in preferred_types
    ]
    return selected or ranked


def lay_preview(row: Dict[str, Any], max_len: int = 280) -> str:
    text = (row.get("document_preview") or row.get("document") or "").strip()
    if len(text) > max_len:
        return text[:max_len].rstrip() + "..."
    return text


def bo_sung_rule_context_vao_tin_nhan(message: str, rule_context: Dict[str, Any]) -> str:
    if not rule_context.get("matched"):
        return message
    parts = [message]
    if rule_context.get("primary_intent"):
        parts.append(f"primary_intent: {rule_context['primary_intent']}")
    if rule_context.get("target_otc_group"):
        parts.append(f"otc_category: {rule_context['target_otc_group']}")
    if rule_context.get("retrieval_query"):
        parts.append(str(rule_context["retrieval_query"]))
    return "\n".join(parts)


def xay_metadata_filter_tu_rule(rule_context: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not rule_context or not rule_context.get("matched"):
        return None

    must_avoid_sections = [
        str(s)
        for s in rule_context.get("must_avoid_sections_in_rag") or []
        if str(s).strip()
    ]
    target_group = str(rule_context.get("target_otc_group") or "").strip()
    conditions: List[Dict[str, Any]] = []
    if must_avoid_sections:
        conditions.append({"section": {"$nin": must_avoid_sections}})
    if target_group:
        conditions.append({"otc_category": {"$eq": target_group}})
    if not conditions:
        return None
    if len(conditions) == 1:
        return conditions[0]
    return {"$and": conditions}


def xay_metadata_filter_tu_patient_context(
    patient_context: Optional[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """Xay dung Chroma metadata filter dua tren thong tin benh nhan.

    Chi ap dung filter khi co du hieu ro rang ve nhom tuoi hoac thai ky.
    Cac truong hop con lai khong filter age_group de tranh bo sot tai lieu.

    Args:
        patient_context: Dict chua cac truong nhu age, age_months, pregnant.

    Returns:
        Chroma filter dict hoac None neu khong can filter.
    """
    if not patient_context:
        return None

    tuoi = patient_context.get("age")
    tuoi_thang = patient_context.get("age_months")
    dang_mang_thai = patient_context.get("pregnant")

    # Nhi khoa: co age_months hoac age < 16
    la_nhi_khoa = (tuoi_thang is not None) or (tuoi is not None and isinstance(tuoi, (int, float)) and tuoi < 16)

    if la_nhi_khoa:
        # Cho phep ca "pediatric" lan "general" de khong bo sot tai lieu chung
        return {"age_group": {"$in": ["pediatric", "general"]}}

    if dang_mang_thai is True:
        return {"age_group": {"$in": ["pregnancy", "general"]}}

    # Cac truong hop khac (nguoi lon binh thuong) khong can filter age_group
    return None


def hop_nhat_metadata_filter(
    filter_tu_rule: Optional[Dict[str, Any]],
    filter_tu_benh_nhan: Optional[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """Hop nhat hai filter theo AND logic neu ca hai cung ton tai."""
    if filter_tu_rule is None:
        return filter_tu_benh_nhan
    if filter_tu_benh_nhan is None:
        return filter_tu_rule
    # Ca hai deu co -> dung $and
    return {"$and": [filter_tu_rule, filter_tu_benh_nhan]}

