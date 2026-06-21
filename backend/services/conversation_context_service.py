"""In-memory session context for multi-turn medication safety flows."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from backend.services.patient_context_service import PatientContextService, normalize_text


@dataclass
class ConversationState:
    patient_context: Dict[str, Any] = field(default_factory=dict)
    pending_question: Optional[str] = None
    pending_reason: Optional[str] = None


class ConversationContextService:
    """Stores lightweight context per session for a local API/demo process."""

    def __init__(self) -> None:
        self._states: Dict[str, ConversationState] = {}
        self._patient_context = PatientContextService()

    def build_context(
        self,
        session_id: str,
        message: str,
        incoming_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        state = self._states.setdefault(session_id, ConversationState())
        merged = deepcopy(incoming_context or {})
        patient_context = self._merge_patient_context(
            state.patient_context,
            merged.get("patient_context") or {},
        )

        if state.pending_question and self._looks_like_context_answer(message):
            extracted = self._patient_context.assess(message, intent="high_risk_context").patient_context
            patient_context = self._merge_patient_context(patient_context, extracted)
            normalized = normalize_text(message)
            patient_context["conditions_confirmed"] = True
            if "di ung" in normalized or "khong di ung" in normalized:
                patient_context["allergies_confirmed"] = True
            if "dang dung" in normalized or "khong dung thuoc" in normalized or "thuoc khac" in normalized:
                patient_context["current_medications_confirmed"] = True
            if patient_context.get("pregnant") is not None or patient_context.get("breastfeeding") is not None:
                patient_context["pregnancy_breastfeeding_confirmed"] = True
            merged["resume_pending_question"] = state.pending_question
            merged["resumed_from_user_message"] = message

        merged["patient_context"] = patient_context
        return merged

    def message_for_processing(self, session_id: str, message: str, context: Dict[str, Any]) -> str:
        return str(context.get("resume_pending_question") or message)

    def update_from_response(self, session_id: str, user_message: str, response_metadata: Dict[str, Any]) -> None:
        state = self._states.setdefault(session_id, ConversationState())
        patient_context = response_metadata.get("patient_context") or {}
        if patient_context:
            state.patient_context = self._merge_patient_context(state.patient_context, patient_context)

        if response_metadata.get("rag_action") == "needs_clarification":
            state.pending_question = response_metadata.get("original_query") or user_message
            state.pending_reason = response_metadata.get("reason") or "needs_clarification"
        elif response_metadata.get("resumed_from_pending_question"):
            state.pending_question = None
            state.pending_reason = None

    def _merge_patient_context(self, base: Dict[str, Any], incoming: Dict[str, Any]) -> Dict[str, Any]:
        merged = deepcopy(base or {})
        for key, value in (incoming or {}).items():
            if key in {"conditions", "allergies", "current_medications"}:
                values = list(dict.fromkeys((merged.get(key) or []) + (value or [])))
                merged[key] = values
            elif value is not None and value != []:
                merged[key] = value
        return merged

    def _looks_like_context_answer(self, message: str) -> bool:
        normalized = normalize_text(message)
        markers = [
            "tuoi",
            "kg",
            "tieu duong",
            "huyet ap",
            "tim",
            "gan",
            "than",
            "da day",
            "hen",
            "di ung",
            "khong di ung",
            "dang dung",
            "khong dung thuoc",
            "khong co benh",
            "khong benh",
            "mang thai",
            "cho con bu",
        ]
        return any(marker in normalized for marker in markers)
