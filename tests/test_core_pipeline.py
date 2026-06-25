"""Tests cho core pipeline: PatientContextService, classify_question_intent, evaluate_evidence.

Chay bang: pytest tests/test_core_pipeline.py -v
"""
from __future__ import annotations

import pytest

from backend.services.patient_context_service import PatientContextService
from backend.safety.evidence_guardrails import (
    EvidenceAction,
    QuestionIntent,
    classify_question_intent,
    evaluate_evidence,
)


# ============================================================================
# Fixture
# ============================================================================

@pytest.fixture
def dich_vu_benh_nhan() -> PatientContextService:
    """Khoi tao PatientContextService khong co LLM extractor de test thuan."""
    return PatientContextService(llm_extractor=None)


def _tao_result(source: str, kieu: str = "", da_xac_minh: bool = True) -> dict:
    """Tao mot result dict gia lap de truyen vao evaluate_evidence."""
    return {
        "document_preview": f"Tai lieu tu {source} ve {kieu}",
        "metadata": {
            "source": source,
            "type": kieu,
            "trust_level": "official_registry" if da_xac_minh else "unverified_ocr",
        },
    }


# ============================================================================
# Nhom 1: PatientContextService.assess() -- 10 truong hop
# ============================================================================

class TestPatientContextService:
    """10 test case cho PatientContextService.assess()."""

    def test_tre_em_thieu_tuoi_va_can(self, dich_vu_benh_nhan: PatientContextService) -> None:
        """Case 1: Cau hoi ve tre em -- phai hoi tuoi + can nang."""
        ket_qua = dich_vu_benh_nhan.assess(
            message="Be nha toi bi sot, nen cho uong thuoc gi?",
            intent="otc_recommendation",
            context={},
        )
        assert ket_qua.should_ask is True, "Phai hoi khi chua co tuoi tre em"
        co_hoi_tuoi = (
            "age_or_age_months" in ket_qua.missing_context
            or "age" in ket_qua.missing_context
        )
        assert co_hoi_tuoi, f"Phai hoi tuoi, missing={ket_qua.missing_context}"
        assert "pediatric_or_age_sensitive" in ket_qua.risk_flags

    def test_tre_5_tuoi_thieu_can(self, dich_vu_benh_nhan: PatientContextService) -> None:
        """Case 2: Tre 5 tuoi -- phai extract age=5 va hoi can nang."""
        ket_qua = dich_vu_benh_nhan.assess(
            message="Con trai 5 tuoi uong Paracetamol lieu bao nhieu?",
            intent="dosage",
            context={},
        )
        assert ket_qua.patient_context.get("age") == 5, (
            f"Phai extract age=5, got {ket_qua.patient_context.get('age')}"
        )
        assert "weight_kg" in ket_qua.missing_context, (
            f"Phai hoi can nang cho tre em, missing={ket_qua.missing_context}"
        )
        assert "pediatric_or_age_sensitive" in ket_qua.risk_flags

    def test_mang_thai_thang_6(self, dich_vu_benh_nhan: PatientContextService) -> None:
        """Case 3: Phu nu mang thai thang 6 -- phai detect thai ky."""
        ket_qua = dich_vu_benh_nhan.assess(
            message="Toi dang mang thai thang thu 6, uong Panadol duoc khong?",
            intent="dosage",
            context={},
        )
        assert "pregnancy_or_breastfeeding" in ket_qua.risk_flags, (
            f"Phai co flag thai ky, flags={ket_qua.risk_flags}"
        )
        assert ket_qua.patient_context.get("pregnant") is True
        assert ket_qua.patient_context.get("pregnancy_month") == 6

    def test_mang_thai_cach_xa_tu_kieu_1(self, dich_vu_benh_nhan: PatientContextService) -> None:
        """Case 3b: Tu 'mang thai' va 'thang 6' cach xa nhau (kieu: thang truoc so)."""
        ket_qua = dich_vu_benh_nhan.assess(
            message="Toi dang mang thai, bay gio la thang 6 roi, co dung thuoc duoc khong?",
            intent="drug_info",
            context={},
        )
        assert ket_qua.patient_context.get("pregnant") is True
        assert ket_qua.patient_context.get("pregnancy_month") == 6

    def test_mang_thai_cach_xa_tu_kieu_2(self, dich_vu_benh_nhan: PatientContextService) -> None:
        """Case 3c: Tu 'mang thai' va '6 thang' cach xa nhau (kieu: so truoc thang)."""
        ket_qua = dich_vu_benh_nhan.assess(
            message="Toi mang thai tinh den nay da duoc 6 thang, mua thuoc gi uong cho an toan?",
            intent="otc_recommendation",
            context={},
        )
        assert ket_qua.patient_context.get("pregnant") is True
        assert ket_qua.patient_context.get("pregnancy_month") == 6

    def test_benh_nen_tieu_duong(self, dich_vu_benh_nhan: PatientContextService) -> None:
        """Case 4: Benh nen tieu duong ro rang -- phai detect chronic_condition."""
        ket_qua = dich_vu_benh_nhan.assess(
            message="Toi bi tieu duong, co the uong Aspirin khong?",
            intent="drug_info",
            context={},
        )
        assert "chronic_condition" in ket_qua.risk_flags, (
            f"Phai co chronic_condition, flags={ket_qua.risk_flags}"
        )
        assert "diabetes" in ket_qua.patient_context.get("conditions", []), (
            f"Phai detect diabetes, conditions={ket_qua.patient_context.get('conditions')}"
        )

    def test_phu_dinh_khong_benh_nen(self, dich_vu_benh_nhan: PatientContextService) -> None:
        """Case 5: Noi ro khong benh nen -- conditions_confirmed=True, khong hoi lai."""
        ket_qua = dich_vu_benh_nhan.assess(
            message="Toi khong co benh nen gi, uong Ibuprofen duoc khong?",
            intent="dosage",
            context={},
        )
        assert ket_qua.patient_context.get("conditions_confirmed") is True, (
            "Phu dinh benh nen phai set conditions_confirmed=True"
        )
        assert "conditions_confirmed" not in ket_qua.missing_context, (
            f"Khong duoc hoi lai conditions khi da phu dinh, missing={ket_qua.missing_context}"
        )

    def test_cau_thong_tin_thuan_tuy(self, dich_vu_benh_nhan: PatientContextService) -> None:
        """Case 6: Cau hoi thong tin chung -- khong trigger risk_flags nhi khoa hay thai ky."""
        ket_qua = dich_vu_benh_nhan.assess(
            message="Paracetamol co tac dung gi?",
            intent="drug_info",
            context={},
        )
        assert "pediatric_or_age_sensitive" not in ket_qua.risk_flags, (
            "Cau thong tin thuan tuy khong phai ve tre em"
        )
        assert "pregnancy_or_breastfeeding" not in ket_qua.risk_flags, (
            "Cau thong tin thuan tuy khong phai ve thai ky"
        )

    def test_co_context_tu_truoc(self, dich_vu_benh_nhan: PatientContextService) -> None:
        """Case 7: Da co patient context tu turn truoc -- khong hoi lai thong tin da co."""
        context_san_co = {
            "patient_context": {
                "age": 30,
                "conditions_confirmed": True,
                "allergies_confirmed": True,
                "current_medications_confirmed": True,
            }
        }
        ket_qua = dich_vu_benh_nhan.assess(
            message="Uong Paracetamol bao nhieu?",
            intent="dosage",
            context=context_san_co,
        )
        assert ket_qua.patient_context.get("age") == 30, (
            f"Phai giu lai age=30 tu context cu, got {ket_qua.patient_context.get('age')}"
        )
        assert "age" not in ket_qua.missing_context, (
            "Tuoi 30 da co roi, khong hoi lai"
        )

    def test_tuong_tac_thuoc(self, dich_vu_benh_nhan: PatientContextService) -> None:
        """Case 8: Cau hoi tuong tac -- phai flag possible_interaction."""
        ket_qua = dich_vu_benh_nhan.assess(
            message="Uong Aspirin cung voi Warfarin co an toan khong?",
            intent="interaction",
            context={},
        )
        assert "possible_interaction" in ket_qua.risk_flags, (
            f"Phai co possible_interaction, flags={ket_qua.risk_flags}"
        )

    def test_di_ung_thuoc_cu_the(self, dich_vu_benh_nhan: PatientContextService) -> None:
        """Case 9: Khai bao di ung Penicillin ro rang -- phai extract va confirm."""
        ket_qua = dich_vu_benh_nhan.assess(
            message="Toi di ung Penicillin, co thuoc thay the khong?",
            intent="drug_info",
            context={},
        )
        allergies = ket_qua.patient_context.get("allergies", [])
        assert any("penicillin" in str(a).lower() for a in allergies), (
            f"Phai extract di ung Penicillin, allergies={allergies}"
        )
        assert ket_qua.patient_context.get("allergies_confirmed") is True

    def test_message_rong_khong_can_hoi(self, dich_vu_benh_nhan: PatientContextService) -> None:
        """Case 10: Message rong -- should_ask=False, khong co risk_flags, khong thieu context."""
        ket_qua = dich_vu_benh_nhan.assess(
            message="",
            intent="drug_info",
            context={},
        )
        assert ket_qua.should_ask is False, "Message rong khong nen hoi gi"
        assert ket_qua.risk_flags == [], f"Khong co risk_flags, got {ket_qua.risk_flags}"
        assert ket_qua.missing_context == [], f"Khong thieu context, got {ket_qua.missing_context}"


# ============================================================================
# Nhom 2: classify_question_intent() -- 5 truong hop
# ============================================================================

class TestClassifyQuestionIntent:
    """5 test case cho classify_question_intent()."""

    def test_intent_khan_cap_qua_lieu_paracetamol(self) -> None:
        """'qua lieu paracetamol + so luong vien lon' phai la EMERGENCY."""
        intent = classify_question_intent("Ba toi uong qua lieu Paracetamol, uong 20 vien")
        assert intent == QuestionIntent.EMERGENCY, (
            f"Qua lieu paracetamol phai la EMERGENCY, got {intent}"
        )

    def test_intent_lieu_dung(self) -> None:
        """Cau hoi ve so vien / so lan uong phai la DOSAGE."""
        intent = classify_question_intent("Uong Ibuprofen ngay may lan, moi lan may vien?")
        assert intent == QuestionIntent.DOSAGE, (
            f"Cau hoi lieu dung phai la DOSAGE, got {intent}"
        )

    def test_intent_tuong_tac_hai_thuoc(self) -> None:
        """Cau hoi tuong tac giua Aspirin va Warfarin phai la INTERACTION."""
        intent = classify_question_intent("Uong Aspirin cung Warfarin co tuong tac gi khong?")
        assert intent == QuestionIntent.INTERACTION, (
            f"Cau hoi tuong tac phai la INTERACTION, got {intent}"
        )

    def test_intent_mua_thuoc_otc(self) -> None:
        """'bi cam ho mua thuoc gi' phai la OTC_RECOMMENDATION."""
        intent = classify_question_intent("Bi cam ho thi mua thuoc gi?")
        assert intent == QuestionIntent.OTC_RECOMMENDATION, (
            f"'mua thuoc gi' phai la OTC_RECOMMENDATION, got {intent}"
        )

    def test_intent_thong_tin_thuoc_chung(self) -> None:
        """Cau hoi thong tin dinh danh thuoc don gian phai la DRUG_INFO."""
        intent = classify_question_intent("Paracetamol duoc dung de dieu tri benh gi?")
        assert intent == QuestionIntent.DRUG_INFO, (
            f"Cau hoi thong tin thuan tuy phai la DRUG_INFO, got {intent}"
        )


# ============================================================================
# Nhom 3: evaluate_evidence() -- 5 truong hop
# ============================================================================

class TestEvaluateEvidence:
    """5 test case cho evaluate_evidence()."""

    def test_allow_drug_info_co_registry(self) -> None:
        """Drug info + nguon registry da xac minh -> ALLOW, should_answer=True."""
        results = [_tao_result("dav_all", "drug_info")]
        quyet_dinh = evaluate_evidence(
            question="Paracetamol co tac dung gi?",
            intent=QuestionIntent.DRUG_INFO,
            results=results,
        )
        assert quyet_dinh.action == EvidenceAction.ALLOW, (
            f"Drug info + dav_all phai ALLOW, got {quyet_dinh.action}"
        )
        assert quyet_dinh.should_answer is True
        assert "dav_all" in quyet_dinh.usable_sources

    def test_allow_with_caution_dosage_co_safety_source(self) -> None:
        """Dosage intent + safety source da xac minh -> ALLOW_WITH_CAUTION, co warnings."""
        results = [
            {
                "document_preview": "Ibuprofen lieu dung",
                "metadata": {
                    "source": "dav_recall",
                    "type": "dosage",
                    "drug_name": "ibuprofen",
                    "trust_level": "official_registry",
                },
            }
        ]
        quyet_dinh = evaluate_evidence(
            question="Uong Ibuprofen ngay may vien la du?",
            intent=QuestionIntent.DOSAGE,
            results=results,
        )
        assert quyet_dinh.action == EvidenceAction.ALLOW_WITH_CAUTION, (
            f"Dosage + safety source phai ALLOW_WITH_CAUTION, got {quyet_dinh.action}"
        )
        assert quyet_dinh.should_answer is True
        assert len(quyet_dinh.warnings) > 0, (
            "ALLOW_WITH_CAUTION phai co it nhat 1 warning ve rui ro"
        )

    def test_handoff_tuong_tac_chi_co_ocr(self) -> None:
        """Interaction intent + chi co OCR chua xac minh -> HANDOFF, should_answer=False."""
        results = [_tao_result("dav_pdf_ocr", "interaction", da_xac_minh=False)]
        quyet_dinh = evaluate_evidence(
            question="Warfarin uong cung Aspirin co sao khong?",
            intent=QuestionIntent.INTERACTION,
            results=results,
        )
        assert quyet_dinh.action == EvidenceAction.HANDOFF, (
            f"Interaction + chi OCR phai HANDOFF, got {quyet_dinh.action}"
        )
        assert quyet_dinh.should_answer is False

    def test_insufficient_evidence_khong_co_result(self) -> None:
        """Khong co result nao -> INSUFFICIENT_EVIDENCE, should_answer=False."""
        quyet_dinh = evaluate_evidence(
            question="Thuoc ABC XYZ dieu tri gi?",
            intent=QuestionIntent.DRUG_INFO,
            results=[],
        )
        assert quyet_dinh.action == EvidenceAction.INSUFFICIENT_EVIDENCE, (
            f"Khong co results phai INSUFFICIENT_EVIDENCE, got {quyet_dinh.action}"
        )
        assert quyet_dinh.should_answer is False
        assert "No retrieved evidence." in quyet_dinh.warnings

    def test_emergency_bo_qua_rag_du_co_result(self) -> None:
        """EMERGENCY intent -> luon tra ve EMERGENCY, du co nhieu results tot."""
        results = [
            _tao_result("dav_all", "dosage"),
            _tao_result("dav_recall", "safety"),
        ]
        quyet_dinh = evaluate_evidence(
            question="Ba toi uong qua lieu Paracetamol 20 vien",
            intent=QuestionIntent.EMERGENCY,
            results=results,
        )
        assert quyet_dinh.action == EvidenceAction.EMERGENCY, (
            f"EMERGENCY intent phai cho EMERGENCY action, got {quyet_dinh.action}"
        )
        assert quyet_dinh.should_answer is False, "EMERGENCY khong duoc phep tra loi bang RAG"
        assert len(quyet_dinh.warnings) > 0, "EMERGENCY phai co warning huong dan cap cuu"

