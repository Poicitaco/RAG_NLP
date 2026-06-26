"""In-memory session context for multi-turn medication safety flows."""
from __future__ import annotations

import json
import threading
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

from backend.services.patient_context_service import PatientContextService, normalize_text

STATE_FILE = Path(__file__).resolve().parents[2] / "data" / "conversation_states.json"


@dataclass
class ConversationState:
    patient_context: Dict[str, Any] = field(default_factory=dict)
    pending_question: Optional[str] = None
    pending_reason: Optional[str] = None
    last_question: Optional[str] = None
    last_answer: Optional[str] = None
    asked_slots: list = field(default_factory=list)  # tiered clarification tracking


class ConversationContextService:
    """Stores lightweight context per session, persisted to file across restarts."""

    def __init__(self, state_file: Optional[Path] = None) -> None:
        self._states: Dict[str, ConversationState] = {}
        self._lock = threading.Lock()
        self._state_file = state_file or STATE_FILE
        self._patient_context = PatientContextService()
        self._load_states()

    def _load_states(self) -> None:
        if not self._state_file.exists():
            return
        try:
            with self._state_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
            for sid, d in data.items():
                self._states[sid] = ConversationState(
                    patient_context=d.get("patient_context", {}),
                    pending_question=d.get("pending_question"),
                    pending_reason=d.get("pending_reason"),
                    last_question=d.get("last_question"),
                    last_answer=d.get("last_answer"),
                    asked_slots=d.get("asked_slots", []),
                )
        except Exception:
            pass  # corrupt file → start fresh

    def _save_states(self) -> None:
        self._state_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            sid: {
                "patient_context": state.patient_context,
                "pending_question": state.pending_question,
                "pending_reason": state.pending_reason,
                "last_question": state.last_question,
                "last_answer": state.last_answer,
                "asked_slots": state.asked_slots,
            }
            for sid, state in self._states.items()
        }
        try:
            with self._state_file.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def build_context(
        self,
        session_id: str,
        message: str,
        incoming_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        with self._lock:
            state = self._states.setdefault(session_id, ConversationState())
        merged = deepcopy(incoming_context or {})
        
        # Hỗ trợ cả trường hợp API gửi flat dict (chứa age, weight_kg...) và trường hợp lồng trong key 'patient_context'
        incoming_patient_context = merged.get("patient_context") or {}
        if not incoming_patient_context and any(k in merged for k in ["age", "age_months", "weight_kg", "conditions", "allergies", "pregnant", "breastfeeding"]):
            incoming_patient_context = {k: merged[k] for k in ["age", "age_months", "weight_kg", "conditions", "allergies", "current_medications", "pregnant", "pregnancy_month", "breastfeeding"] if k in merged}

        patient_context = self._merge_patient_context(
            state.patient_context,
            incoming_patient_context,
        )

        if (state.pending_question or state.last_question) and self._looks_like_context_answer(message):
            extracted = self._patient_context.assess(message, intent="high_risk_context").patient_context
            patient_context = self._merge_patient_context(patient_context, extracted)
            normalized = normalize_text(message)
            negative_none = any(
                marker in normalized
                for marker in [
                    "khong co",
                    "khong co gi",
                    "khong bi gi",
                    "khong dung gi",
                    "khong su dung gi",
                ]
            )
            patient_context["conditions_confirmed"] = True
            if negative_none or "di ung" in normalized or "khong di ung" in normalized:
                patient_context["allergies_confirmed"] = True
            if (
                negative_none
                or "dang dung" in normalized
                or "khong dung thuoc" in normalized
                or "thuoc khac" in normalized
            ):
                patient_context["current_medications_confirmed"] = True
            if patient_context.get("pregnant") is not None or patient_context.get("breastfeeding") is not None:
                patient_context["pregnancy_breastfeeding_confirmed"] = True
            resume_question = state.pending_question or state.last_question
            if state.pending_question:
                merged["resume_pending_question"] = resume_question
            else:
                merged["resume_last_question"] = resume_question
            merged["resumed_from_user_message"] = message

        merged["patient_context"] = patient_context
        if state.last_answer:
            merged["last_assistant_answer"] = state.last_answer
        if state.asked_slots:
            merged["_asked_slots"] = list(state.asked_slots)
        return merged

    def message_for_processing(self, session_id: str, message: str, context: Dict[str, Any]) -> str:
        return str(context.get("resume_pending_question") or context.get("resume_last_question") or message)

    def update_from_response(self, session_id: str, user_message: str, response_metadata: Dict[str, Any]) -> None:
        with self._lock:
            state = self._states.setdefault(session_id, ConversationState())
            patient_context = response_metadata.get("patient_context") or {}
            if patient_context:
                state.patient_context = self._merge_patient_context(state.patient_context, patient_context)

            # Lưu câu trả lời cuối vào state để inject vào context sau
            response_message = response_metadata.get("message") or response_metadata.get("answer") or ""
            if response_message:
                state.last_answer = str(response_message)[:500]  # cap 500 chars

            if response_metadata.get("rag_action") == "needs_clarification":
                state.pending_question = response_metadata.get("original_query") or user_message
                state.pending_reason = response_metadata.get("reason") or "needs_clarification"
                # Persist tiered clarification progress
                new_asked = response_metadata.get("_asked_slots")
                if new_asked:
                    state.asked_slots = list(new_asked)
            elif response_metadata.get("resumed_from_pending_question") or response_metadata.get("resumed_from_previous_question"):
                state.pending_question = None
                state.pending_reason = None
                state.asked_slots = []  # reset khi câu hỏi được resume
            elif response_metadata.get("original_query"):
                state.last_question = response_metadata.get("original_query")
            elif user_message:
                state.last_question = user_message
            self._save_states()

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
            "khong co",
            "khong co gi",
            "khong bi gi",
            "dang dung",
            "khong dung gi",
            "khong dung thuoc",
            "khong co benh",
            "khong benh",
            "mang thai",
            "cho con bu",
        ]
        return any(marker in normalized for marker in markers)
