"""Patient-context clarification before medication advice.

The service keeps the safety-first pipeline from answering too early when a
public-user question lacks context that materially changes medicine safety.
It is deterministic and session/context friendly: callers can pass known
patient fields in ``context["patient_context"]`` and the service will only ask
for the missing parts that matter for the current question.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


CONDITION_TERMS = {
    "diabetes": ["tieu duong", "dai thao duong", "duong huyet"],
    "hypertension": ["huyet ap", "cao huyet ap", "tang huyet ap"],
    "heart_disease": ["tim mach", "benh tim", "suy tim", "dau nguc"],
    "liver_disease": ["suy gan", "benh gan", "vang da", "vang mat"],
    "kidney_disease": ["suy than", "benh than", "hong than"],
    "stomach_ulcer": ["dau bao tu", "viem loet da day", "loet da day"],
    "asthma": ["hen", "suyen", "kho tho"],
}

PREGNANCY_TERMS = ["mang thai", "co thai", "bau", "cho con bu"]
ADVICE_TERMS = [
    "mua thuoc gi",
    "nen mua",
    "nen uong",
    "uong thuoc gi",
    "dung thuoc gi",
    "loai nao",
    "tu van",
    "ban cho",
    "chon thuoc",
]
SYMPTOM_TERMS = [
    "cam",
    "ho",
    "sot",
    "dau",
    "nghet mui",
    "so mui",
    "tieu chay",
    "di ngoai",
    "non",
    "ngua",
    "dau bung",
    "dau dau",
]
DOSAGE_TERMS = [
    "lieu",
    "uong bao nhieu",
    "dung bao nhieu",
    "may vien",
    "ngay may lan",
    "cach dung",
    "dung the nao",
    "uong the nao",
]
INTERACTION_TERMS = [
    "tuong tac",
    "dung chung",
    "uong chung",
    "uong cung",
    "ket hop",
    "them",
    "chung voi",
    "thuoc khac",
]
PEDIATRIC_TERMS = ["be", "tre", "con toi", "con tui", "con nit", "so sinh"]
COMMON_DRUG_TERMS = [
    "aspirin",
    "diclofenac",
    "ibuprofen",
    "paracetamol",
    "acetaminophen",
    "panadol",
    "efferalgan",
    "warfarin",
    "atorvastatin",
    "clarithromycin",
    "amoxicillin",
    "metronidazole",
]


@dataclass
class ContextAssessment:
    should_ask: bool
    patient_context: Dict[str, Any]
    missing_context: List[str] = field(default_factory=list)
    questions: List[str] = field(default_factory=list)
    reason: str = ""
    risk_flags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "should_ask": self.should_ask,
            "patient_context": self.patient_context,
            "missing_context": self.missing_context,
            "clarification_questions": self.questions,
            "reason": self.reason,
            "risk_flags": self.risk_flags,
        }


def normalize_text(text: str) -> str:
    value = (text or "").replace("\u0110", "D").replace("\u0111", "d").lower()
    decomposed = unicodedata.normalize("NFD", value)
    stripped = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", stripped).strip()


def contains_any(normalized: str, terms: List[str]) -> bool:
    return any(term in normalized for term in terms)


class PatientContextService:
    """Ask for missing patient context when a medication answer is unsafe."""

    def assess(
        self,
        message: str,
        intent: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> ContextAssessment:
        normalized = normalize_text(message)
        provided = self._merge_context(context, normalized)
        risk_flags = self._risk_flags(normalized, intent)
        required = self._required_fields(normalized, intent, provided, risk_flags)
        missing = [field for field in required if self._field_missing(field, provided)]

        questions = self._questions_for_missing(missing, provided, risk_flags)
        should_ask = bool(questions)
        reason = ""
        if should_ask:
            reason = "missing_patient_context_for_safe_medication_advice"

        return ContextAssessment(
            should_ask=should_ask,
            patient_context=provided,
            missing_context=missing,
            questions=questions,
            reason=reason,
            risk_flags=risk_flags,
        )

    def _merge_context(self, context: Optional[Dict[str, Any]], normalized: str) -> Dict[str, Any]:
        source = dict((context or {}).get("patient_context") or {})
        conditions = set(source.get("conditions") or [])
        conditions.update(self._extract_conditions(normalized))

        patient_context = {
            "age": source.get("age"),
            "age_months": source.get("age_months"),
            "weight_kg": source.get("weight_kg"),
            "pregnant": source.get("pregnant"),
            "breastfeeding": source.get("breastfeeding"),
            "conditions": sorted(conditions),
            "allergies": source.get("allergies") or [],
            "current_medications": source.get("current_medications") or [],
            "conditions_confirmed": source.get("conditions_confirmed"),
            "allergies_confirmed": source.get("allergies_confirmed"),
            "current_medications_confirmed": source.get("current_medications_confirmed"),
            "pregnancy_breastfeeding_confirmed": source.get("pregnancy_breastfeeding_confirmed"),
        }

        age = self._extract_age(normalized)
        if age is not None:
            patient_context["age"] = age
        age_months = self._extract_age_months(normalized)
        if age_months is not None:
            patient_context["age_months"] = age_months
        weight = self._extract_weight(normalized)
        if weight is not None:
            patient_context["weight_kg"] = weight
        if contains_any(normalized, ["cho con bu"]):
            patient_context["breastfeeding"] = True
        if contains_any(normalized, ["mang thai", "co thai", "bau"]):
            patient_context["pregnant"] = True
        if conditions:
            patient_context["conditions_confirmed"] = True
        if (
            "khong co benh nen" in normalized
            or "khong benh nen" in normalized
            or "khong mac benh nen" in normalized
            or "khong co benh man tinh" in normalized
        ):
            patient_context["conditions_confirmed"] = True
        if "khong di ung" in normalized or "khong co di ung" in normalized:
            patient_context["allergies_confirmed"] = True
        if (
            "khong dang dung thuoc" in normalized
            or "khong dung thuoc" in normalized
            or "khong dung thuoc khac" in normalized
        ):
            patient_context["current_medications_confirmed"] = True

        return patient_context

    def _risk_flags(self, normalized: str, intent: str) -> List[str]:
        flags = []
        age = self._extract_age(normalized)
        age_months = self._extract_age_months(normalized)
        if contains_any(normalized, PEDIATRIC_TERMS) or age_months is not None or (age is not None and age < 16):
            flags.append("pediatric_or_age_sensitive")
        if contains_any(normalized, PREGNANCY_TERMS):
            flags.append("pregnancy_or_breastfeeding")
        if any(term in normalized for terms in CONDITION_TERMS.values() for term in terms):
            flags.append("chronic_condition")
        if contains_any(normalized, DOSAGE_TERMS) or intent == "dosage":
            flags.append("dosage_or_how_to_use")
        if contains_any(normalized, INTERACTION_TERMS) or intent == "interaction":
            flags.append("possible_interaction")
        if contains_any(normalized, ADVICE_TERMS) and contains_any(normalized, SYMPTOM_TERMS):
            flags.append("otc_recommendation")
        return list(dict.fromkeys(flags))

    def _required_fields(
        self,
        normalized: str,
        intent: str,
        patient_context: Dict[str, Any],
        risk_flags: List[str],
    ) -> List[str]:
        required: List[str] = []

        if "pediatric_or_age_sensitive" in risk_flags:
            required.extend(["age_or_age_months", "weight_kg"])
        elif intent in {"dosage", "high_risk_context"} or "otc_recommendation" in risk_flags:
            required.append("age")

        if "otc_recommendation" in risk_flags or intent in {"dosage", "high_risk_context"}:
            required.extend(["conditions_confirmed", "current_medications_confirmed", "allergies_confirmed"])

        drug_count = self._drug_mention_count(normalized)
        if "possible_interaction" in risk_flags and drug_count < 2 and not patient_context.get("current_medications"):
            required.append("current_medications_confirmed")

        if contains_any(normalized, ["phu nu", "chi em", "mang thai", "cho con bu"]):
            required.append("pregnancy_breastfeeding_confirmed")

        return list(dict.fromkeys(required))

    def _field_missing(self, field: str, patient_context: Dict[str, Any]) -> bool:
        if field == "age_or_age_months":
            return self._is_missing(patient_context.get("age")) and self._is_missing(patient_context.get("age_months"))
        if field == "conditions_confirmed":
            return not patient_context.get("conditions_confirmed")
        if field == "allergies_confirmed":
            return not patient_context.get("allergies_confirmed")
        if field == "current_medications_confirmed":
            return not patient_context.get("current_medications_confirmed") and self._is_missing(
                patient_context.get("current_medications")
            )
        if field == "pregnancy_breastfeeding_confirmed":
            return (
                patient_context.get("pregnant") is None
                and patient_context.get("breastfeeding") is None
                and not patient_context.get("pregnancy_breastfeeding_confirmed")
            )
        return self._is_missing(patient_context.get(field))

    def _is_missing(self, value: Any) -> bool:
        if value is None:
            return True
        if value is False:
            return False
        if isinstance(value, (list, tuple, set, dict)) and not value:
            return True
        return False

    def _questions_for_missing(
        self,
        missing: List[str],
        patient_context: Dict[str, Any],
        risk_flags: List[str],
    ) -> List[str]:
        questions = []
        if "age_or_age_months" in missing:
            questions.append("Người dùng thuốc bao nhiêu tuổi? Nếu là trẻ nhỏ, cho mình biết tuổi theo tháng/năm.")
        elif "age" in missing:
            questions.append("Bạn/người dùng thuốc bao nhiêu tuổi?")

        if "weight_kg" in missing:
            questions.append("Cân nặng khoảng bao nhiêu kg? Thông tin này rất quan trọng nếu là trẻ em hoặc hỏi liều.")

        missing_safety = [field for field in missing if field in {"conditions_confirmed", "current_medications_confirmed", "allergies_confirmed"}]
        if missing_safety:
            known_conditions = patient_context.get("conditions") or []
            if known_conditions:
                questions.append(
                    "Bạn xác nhận thêm giúp: ngoài "
                    + ", ".join(known_conditions)
                    + ", còn bệnh nền nào như gan/thận/tim mạch/huyết áp/dạ dày/hen không?"
                )
            else:
                questions.append("Bạn có bệnh nền nào như gan, thận, tim mạch, huyết áp, tiểu đường, dạ dày hoặc hen/suyễn không?")
            questions.append("Bạn đang dùng thuốc điều trị nào khác hoặc từng dị ứng thuốc nào không?")

        if "pregnancy_breastfeeding_confirmed" in missing:
            questions.append("Bạn có đang mang thai hoặc cho con bú không?")

        return questions[:3]

    def _extract_age(self, normalized: str) -> Optional[int]:
        match = re.search(r"\b(\d{1,3})\s*tuoi\b", normalized)
        if not match:
            return None
        age = int(match.group(1))
        if 0 <= age <= 120:
            return age
        return None

    def _extract_age_months(self, normalized: str) -> Optional[int]:
        match = re.search(r"\b(\d{1,2})\s*thang\b", normalized)
        if not match:
            return None
        months = int(match.group(1))
        if 0 <= months <= 36:
            return months
        return None

    def _extract_weight(self, normalized: str) -> Optional[float]:
        match = re.search(r"\b(\d{1,3}(?:[.,]\d{1,2})?)\s*kg\b", normalized)
        if not match:
            return None
        weight = float(match.group(1).replace(",", "."))
        if 0 < weight <= 300:
            return weight
        return None

    def _extract_conditions(self, normalized: str) -> List[str]:
        conditions = []
        for key, terms in CONDITION_TERMS.items():
            if contains_any(normalized, terms):
                conditions.append(key)
        return conditions

    def _drug_mention_count(self, normalized: str) -> int:
        return sum(1 for term in COMMON_DRUG_TERMS if term in normalized)
