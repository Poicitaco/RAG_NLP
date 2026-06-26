import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_llm_calls():
    async def fake_plan(*args, **kwargs): return {"intent": "otc_recommendation"}
    async def fake_assess(*args, **kwargs):
        from backend.services.query_ambiguity_service import AmbiguityAssessment
        return AmbiguityAssessment(False, "clear", [], "")
    async def fake_extract(*args, **kwargs): return {}
    async def fake_rewrite(*args, **kwargs):
        print("FAKE REWRITE CALLED!!!!")
        return "Mocked LLM answer"

    with patch("backend.services.llm_intent_planner_service.LLMIntentPlanner.plan", new=fake_plan), \
         patch("backend.services.query_ambiguity_service.QueryAmbiguityService.assess", new=fake_assess), \
         patch("backend.services.llm_patient_context_extractor.LLMPatientContextExtractor.extract", new=fake_extract), \
         patch("backend.services.llm_answer_service.LLMAnswerService.rewrite", new=fake_rewrite):
        yield

def post_chat(message: str, session_id: str = "pytest-chat-smoke") -> dict:
    response = client.post(
        "/api/v1/chat/",
        json={"message": message, "session_id": session_id},
    )
    assert response.status_code == 200
    return response.json()


def test_paracetamol_overdose_bypasses_rag_with_sources():
    payload = post_chat("Toi uong 10 vien Panadol cung luc co nguy hiem khong?")
    metadata = payload["metadata"]

    assert metadata["rag_action"] == "emergency"
    assert metadata["intent"] == "emergency"
    assert metadata["subtype"] == "paracetamol_overdose"
    assert metadata["retrieval_bypassed"] is True
    assert len(payload["sources"]) > 0


def test_interaction_question_uses_graph_fast_path_with_citation():
    payload = post_chat("Aspirin uong chung voi diclofenac co sao khong?")
    metadata = payload["metadata"]

    assert metadata["rag_action"] == "allow_with_caution"
    assert metadata["intent"] == "interaction"
    assert metadata["retriever"] == "graph_fast_path"
    assert len(payload["sources"]) > 0
    assert metadata["graph_safety"]["should_warn"] is True


def test_public_otc_free_text_requires_patient_context_before_advice():
    payload = post_chat("Toi bi cam muon mua thuoc uong cho nhanh khoi")
    metadata = payload["metadata"]

    assert metadata["rag_action"] == "needs_clarification"
    assert metadata["retrieval_bypassed"] is True
    assert metadata["missing_context"]
    assert metadata["clarification_questions"]
    assert len(payload["sources"]) > 0


def test_child_fever_from_parent_requires_weight_after_age():
    # Reset session để tránh state cũ từ persist file
    client.delete("/api/v1/chat/session/pytest-child-fever-context")
    session_id = "pytest-child-fever-context"
    first = post_chat(
        "Con trai toi dang bi sot mua thuoc ha sot nao",
        session_id=session_id,
    )
    first_metadata = first["metadata"]

    assert first_metadata["rag_action"] == "needs_clarification"
    assert first_metadata["intent"] == "pediatric_symptom"
    assert "age_or_age_months" in first_metadata["missing_context"]
    assert "weight_kg" in first_metadata["missing_context"]

    second = post_chat(
        "Nguoi dung thuoc 3 tuoi, khong co benh nen, khong dang dung thuoc khac, khong di ung thuoc.",
        session_id=session_id,
    )
    second_metadata = second["metadata"]

    assert second_metadata["rag_action"] == "needs_clarification"
    assert second_metadata["intent"] == "pediatric_symptom"
    assert second_metadata["missing_context"] == ["weight_kg"]
    assert any("Cân nặng" in question for question in second_metadata["clarification_questions"])
