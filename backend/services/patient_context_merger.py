"""Merge keyword and LLM patient-context extraction results."""
from __future__ import annotations

import re
import unicodedata
from typing import Any, Dict, Iterable, List, Optional

from backend.services.patient_context_schema import CONDITION_CANONICAL, PATIENT_CONTEXT_FIELDS


SAFETY_VALUE_FIELDS = {
    "pregnant",
    "breastfeeding",
    "conditions",
    "allergies",
    "conditions_confirmed",
    "allergies_confirmed",
    "pregnancy_breastfeeding_confirmed",
}

NORMAL_FIELDS = {
    "age",
    "age_months",
    "weight_kg",
    "current_medications",
    "current_medications_confirmed",
    "pregnancy_month",
}

def merge_patient_context(keyword_result: Any, llm_result: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    keyword_context = _context_from_keyword(keyword_result)
    llm = dict(llm_result or {})
    merged = dict(keyword_context)
    uncertain = bool(llm.get("uncertain"))

    for field in NORMAL_FIELDS:
        value = llm.get(field)
        if _has_value(value):
            if field in {"current_medications"}:
                merged[field] = _merge_lists(merged.get(field), value)
            else:
                merged[field] = value

    for field in ("conditions", "allergies"):
        keyword_value = merged.get(field)
        llm_value = llm.get(field)
        if _has_value(keyword_value):
            if _has_value(llm_value):
                merged[field] = _merge_lists(keyword_value, llm_value)
        elif _has_value(llm_value):
            merged[field] = _as_list(llm_value)

    for field in ("pregnant", "breastfeeding"):
        keyword_value = keyword_context.get(field)
        llm_value = llm.get(field)
        if keyword_value is not None and llm_value is not None and keyword_value != llm_value:
            merged[field] = keyword_value
            uncertain = True
        elif keyword_value is None and llm_value is not None:
            merged[field] = llm_value
        else:
            merged[field] = keyword_value

    for field in ("conditions_confirmed", "allergies_confirmed", "pregnancy_breastfeeding_confirmed"):
        keyword_value = keyword_context.get(field)
        llm_value = llm.get(field)
        if keyword_value is not None and llm_value is not None and keyword_value != llm_value:
            merged[field] = keyword_value
            uncertain = True
        elif keyword_value is None and llm_value is not None:
            merged[field] = llm_value
        else:
            merged[field] = keyword_value

    current_confirmed = llm.get("current_medications_confirmed")
    if current_confirmed is not None:
        merged["current_medications_confirmed"] = current_confirmed

    missing_context = _merge_lists(
        getattr(keyword_result, "missing_context", []),
        llm.get("missing_context") or llm.get("missing_fields") or [],
    )
    risk_flags = list(getattr(keyword_result, "risk_flags", []) or [])
    for flag in llm.get("red_flags") or []:
        label = f"llm:{flag}"
        if label not in risk_flags:
            risk_flags.append(label)

    merged["conditions"] = _canonicalize_conditions(merged.get("conditions") or [])
    merged = {key: merged.get(key) for key in PATIENT_CONTEXT_FIELDS if key in merged}

    return {
        "patient_context": merged,
        "intent": llm.get("intent") or None,
        "risk_flags": risk_flags,
        "missing_context": missing_context,
        "uncertain": uncertain,
    }


def _context_from_keyword(keyword_result: Any) -> Dict[str, Any]:
    if hasattr(keyword_result, "patient_context"):
        return dict(keyword_result.patient_context or {})
    if isinstance(keyword_result, dict):
        return dict(keyword_result.get("patient_context") or keyword_result)
    return {}


def _has_value(value: Any) -> bool:
    if value is None:
        return False
    if value is False:
        return True
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    return True


def _as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, (tuple, set)):
        return list(value)
    return [value]


def _merge_lists(*values: Iterable[Any]) -> List[Any]:
    merged: List[Any] = []
    for value in values:
        for item in _as_list(value):
            if item not in merged:
                merged.append(item)
    return merged


def _canonicalize_conditions(conditions: Iterable[Any]) -> List[str]:
    canonical: List[str] = []
    for condition in _as_list(conditions):
        if condition is None:
            continue
        value = str(condition).strip()
        if not value:
            continue
        normalized = _normalize_text(value)
        canonical_key = _condition_to_key(normalized) or value
        if canonical_key not in canonical:
            canonical.append(canonical_key)
    return canonical


def _condition_to_key(normalized_condition: str) -> Optional[str]:
    for alias, canonical in CONDITION_CANONICAL.items():
        if normalized_condition == _normalize_text(alias) or normalized_condition == _normalize_text(canonical):
            return canonical
    return None


def _normalize_text(text: str) -> str:
    value = (text or "").replace("\u0110", "D").replace("\u0111", "d").lower()
    decomposed = unicodedata.normalize("NFD", value)
    stripped = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", stripped).strip()
