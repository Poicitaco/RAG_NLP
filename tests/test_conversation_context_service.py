from __future__ import annotations

from backend.services.conversation_context_service import ConversationContextService


def test_build_context_merges_flat_and_nested_patient_context(tmp_path) -> None:
    service = ConversationContextService(state_file=tmp_path / "states.json")

    context = service.build_context(
        "session-a",
        "toi dau dau",
        {
            "age": 30,
            "patient_context": {
                "conditions": ["hypertension"],
            },
        },
    )

    assert context["patient_context"]["conditions"] == ["hypertension"]
    assert "age" not in context["patient_context"]

    context = service.build_context(
        "session-b",
        "toi dau dau",
        {
            "age": 30,
            "conditions": ["hypertension"],
        },
    )

    assert context["patient_context"]["age"] == 30
    assert context["patient_context"]["conditions"] == ["hypertension"]


def test_update_from_response_stores_pending_question_for_clarification(tmp_path) -> None:
    service = ConversationContextService(state_file=tmp_path / "states.json")

    service.update_from_response(
        "session-a",
        "Be nha toi bi sot",
        {
            "rag_action": "needs_clarification",
            "original_query": "Be nha toi bi sot",
            "reason": "missing_patient_context_for_safe_medication_advice",
            "patient_context": {"conditions": ["asthma"]},
        },
    )

    context = service.build_context("session-a", "Be 3 tuoi nang 14kg")

    assert context["resume_pending_question"] == "Be nha toi bi sot"
    assert context["resumed_from_user_message"] == "Be 3 tuoi nang 14kg"
    assert context["patient_context"]["age"] == 3
    assert context["patient_context"]["weight_kg"] == 14
    assert context["patient_context"]["conditions"] == ["asthma"]
    assert service.message_for_processing("session-a", "Be 3 tuoi nang 14kg", context) == "Be nha toi bi sot"


def test_update_from_response_clears_pending_after_resume(tmp_path) -> None:
    service = ConversationContextService(state_file=tmp_path / "states.json")

    service.update_from_response(
        "session-a",
        "Be nha toi bi sot",
        {
            "rag_action": "needs_clarification",
            "original_query": "Be nha toi bi sot",
        },
    )
    service.update_from_response(
        "session-a",
        "Be 3 tuoi nang 14kg",
        {
            "resumed_from_pending_question": True,
            "patient_context": {"age": 3, "weight_kg": 14},
        },
    )

    context = service.build_context("session-a", "Cam on")

    assert "resume_pending_question" not in context
    assert context["patient_context"]["age"] == 3
    assert context["patient_context"]["weight_kg"] == 14


def test_build_context_uses_last_question_for_context_like_follow_up(tmp_path) -> None:
    service = ConversationContextService(state_file=tmp_path / "states.json")

    service.update_from_response(
        "session-a",
        "Toi muon mua thuoc cam",
        {
            "original_query": "Toi muon mua thuoc cam",
        },
    )
    context = service.build_context("session-a", "Toi 25 tuoi khong co benh nen khong di ung")

    assert context["resume_last_question"] == "Toi muon mua thuoc cam"
    assert context["patient_context"]["age"] == 25
    assert context["patient_context"]["conditions_confirmed"] is True
    assert context["patient_context"]["allergies_confirmed"] is True
    assert service.message_for_processing("session-a", "Toi 25 tuoi", context) == "Toi muon mua thuoc cam"


def test_merge_patient_context_deduplicates_lists_and_ignores_empty_values(tmp_path) -> None:
    service = ConversationContextService(state_file=tmp_path / "states.json")

    service.update_from_response(
        "session-a",
        "Toi dau dau",
        {
            "patient_context": {
                "conditions": ["hypertension"],
                "allergies": ["ibuprofen"],
                "current_medications": ["warfarin"],
                "age": 40,
            }
        },
    )
    context = service.build_context(
        "session-a",
        "toi dang dung warfarin",
        {
            "patient_context": {
                "conditions": ["hypertension", "diabetes"],
                "allergies": [],
                "current_medications": ["warfarin", "aspirin"],
                "age": None,
            }
        },
    )

    assert context["patient_context"]["conditions"] == ["hypertension", "diabetes"]
    assert context["patient_context"]["allergies"] == ["ibuprofen"]
    assert context["patient_context"]["current_medications"] == ["warfarin", "aspirin"]
    assert context["patient_context"]["age"] == 40
