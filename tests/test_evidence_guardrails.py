import pytest
from backend.safety.evidence_guardrails import (
    classify_question_intent,
    evaluate_evidence,
    detect_clinical_subtype,
    contains_any,
    evidence_summary,
    QuestionIntent,
    EvidenceAction,
    SUBTYPE_PARACETAMOL_OVERDOSE,
)

# --- Tests for classify_question_intent (5 cases) ---

def test_classify_intent_emergency_paracetamol():
    question = "Tôi lỡ uống 10 viên paracetamol cùng lúc"
    assert classify_question_intent(question) == QuestionIntent.EMERGENCY

def test_classify_intent_pediatric_symptom():
    question = "Bé nhà tôi 3 tuổi bị ho và sốt"
    assert classify_question_intent(question) == QuestionIntent.PEDIATRIC_SYMPTOM

def test_classify_intent_interaction():
    question = "Dùng chung aspirin và ibuprofen có sao không"
    assert classify_question_intent(question) == QuestionIntent.INTERACTION

def test_classify_intent_dosage():
    question = "Liều dùng của panadol cho trẻ 15kg là bao nhiêu"
    assert classify_question_intent(question) == QuestionIntent.DOSAGE

def test_classify_intent_drug_info():
    question = "Cho tôi hỏi công dụng của thuốc metformin"
    assert classify_question_intent(question) == QuestionIntent.DRUG_INFO

# --- Tests for evaluate_evidence (5 cases) ---

def test_evaluate_evidence_emergency():
    # Emergency intent -> early handoff
    question = "Sốt cao 40 độ co giật"
    decision = evaluate_evidence(question, QuestionIntent.EMERGENCY, [])
    assert decision.action == EvidenceAction.EMERGENCY
    assert not decision.should_answer

def test_evaluate_evidence_pediatric_handoff():
    # Pediatric symptom intent -> early handoff
    question = "Bé nhà tôi 3 tuổi bị ho và sốt"
    decision = evaluate_evidence(question, QuestionIntent.PEDIATRIC_SYMPTOM, [])
    assert decision.action == EvidenceAction.HANDOFF
    assert not decision.should_answer

def test_evaluate_evidence_insufficient_evidence():
    # No results
    question = "Thuốc metformin có tác dụng phụ gì"
    decision = evaluate_evidence(question, QuestionIntent.DRUG_INFO, [])
    assert decision.action == EvidenceAction.INSUFFICIENT_EVIDENCE
    assert not decision.should_answer

def test_evaluate_evidence_interaction_allow_with_caution():
    # High risk (interaction) with verified safety source
    question = "Dùng chung aspirin và ibuprofen"
    results = [
        {"metadata": {"source": "dav_recall", "type": "interaction", "drug_name": "aspirin"}}
    ]
    decision = evaluate_evidence(question, QuestionIntent.INTERACTION, results)
    assert decision.action == EvidenceAction.ALLOW_WITH_CAUTION
    assert decision.should_answer

def test_evaluate_evidence_interaction_handoff_no_verified():
    # High risk (interaction) without verified source (e.g. OCR source)
    question = "Dùng chung aspirin và ibuprofen"
    results = [
        {"metadata": {"source": "dav_pdf_ocr", "type": "interaction"}}
    ]
    decision = evaluate_evidence(question, QuestionIntent.INTERACTION, results)
    assert decision.action == EvidenceAction.HANDOFF
    assert not decision.should_answer

# --- Tests for helper functions (3 cases) ---

def test_detect_clinical_subtype():
    assert detect_clinical_subtype("Tôi lỡ uống 15 viên paracetamol") == SUBTYPE_PARACETAMOL_OVERDOSE
    assert detect_clinical_subtype("Uống 1 viên panadol") == ""

def test_contains_any():
    assert contains_any("bị đau đầu", {"dau dau", "sot"}) is True
    assert contains_any("bị ho", {"dau dau", "sot"}) is False

def test_evidence_summary():
    results = [
        {"metadata": {"source": "dav_recall", "type": "interaction", "drug_name": "aspirin"}},
        {"metadata": {"source": "dav_pdf_ocr", "type": "dosage"}}
    ]
    summary = evidence_summary(results)
    assert summary["has_safety_source"] is True
    assert summary["has_ocr_source"] is True
    assert summary["ocr_count"] == 1
    assert summary["has_verified_interaction"] is True

