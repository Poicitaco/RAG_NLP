import asyncio
import pytest
from unittest.mock import patch, AsyncMock

from backend.services.patient_context_service import PatientContextService



CASES = [
    # dental
    {
        "group": "dental",
        "message": "Toi moi nho rang sau hom qua, dau qua nen uong gi?",
        "intent": "otc_recommendation",
        "llm": {"subject": "dental_pain_after_extraction", "conditions_confirmed": True, "conditions": [], "confidence": 0.9},
        "expect": {"conditions_confirmed": True},
        "missing_has": ["age", "current_medications_confirmed", "allergies_confirmed"],
    },
    {
        "group": "dental",
        "message": "Toi 21 tuoi moi nho rang sau, khong benh nen",
        "intent": "otc_recommendation",
        "llm": {"subject": "dental_pain_after_extraction", "age": 21, "conditions_confirmed": True, "conditions": []},
        "expect": {"age": 21, "conditions_confirmed": True},
        "missing_has": ["current_medications_confirmed", "allergies_confirmed"],
    },
    {
        "group": "dental",
        "message": "Dau rang va dang dung amoxicillin",
        "intent": "otc_recommendation",
        "llm": {"subject": "dental_pain", "current_medications": ["amoxicillin"], "current_medications_confirmed": True},
        "expect_list_contains": {"current_medications": "amoxicillin"},
        "missing_has": ["age", "conditions_confirmed", "allergies_confirmed"],
    },
    {
        "group": "dental",
        "message": "Nho rang xong bi chay mau nhieu",
        "intent": "otc_recommendation",
        "llm": {"subject": "dental_pain_after_extraction", "red_flags": ["post_extraction_bleeding"], "confidence": 0.8},
        "risk_has": ["llm:post_extraction_bleeding"],
        "missing_has": ["age"],
    },
    {
        "group": "dental",
        "message": "Dau rang, toi khong di ung thuoc",
        "intent": "otc_recommendation",
        "llm": {"subject": "dental_pain", "allergies": [], "allergies_confirmed": True},
        "expect": {"allergies_confirmed": True},
        "missing_has": ["age", "conditions_confirmed", "current_medications_confirmed"],
    },
    # pediatric
    {
        "group": "pediatric",
        "message": "Be 3 tuoi bi sot nen uong gi?",
        "intent": "pediatric_symptom",
        "llm": {"subject": "pediatric_fever", "age": 3},
        "expect": {"age": 3},
        "missing_has": ["weight_kg"],
    },
    {
        "group": "pediatric",
        "message": "Be 18 thang nang 11kg bi ho",
        "intent": "pediatric_symptom",
        "llm": {"subject": "cough", "age_months": 18, "weight_kg": 11},
        "expect": {"age_months": 18, "weight_kg": 11},
    },
    {
        "group": "pediatric",
        "message": "Con toi 5 tuoi nang 20kg khong benh nen",
        "intent": "pediatric_symptom",
        "llm": {"subject": "pediatric_fever", "age": 5, "weight_kg": 20, "conditions_confirmed": True, "conditions": []},
        "expect": {"age": 5, "weight_kg": 20, "conditions_confirmed": True},
    },
    {
        "group": "pediatric",
        "message": "Be 8 tuoi di ung ibuprofen",
        "intent": "pediatric_symptom",
        "llm": {"age": 8, "allergies": ["ibuprofen"], "allergies_confirmed": True},
        "expect_list_contains": {"allergies": "ibuprofen"},
        "missing_has": ["weight_kg"],
    },
    {
        "group": "pediatric",
        "message": "Tre so sinh bi sot",
        "intent": "pediatric_symptom",
        "llm": {"subject": "pediatric_fever", "red_flags": ["newborn_fever"], "is_pediatric": True},
        "risk_has": ["llm:newborn_fever"],
        "missing_has": ["age_or_age_months", "weight_kg"],
    },
    # pregnancy
    {
        "group": "pregnancy",
        "message": "Toi dang mang thai thang 4 bi cam",
        "intent": "otc_recommendation",
        "llm": {"subject": "pregnancy_medication", "pregnant": True, "pregnancy_month": 4},
        "expect": {"pregnant": True, "pregnancy_month": 4},
        "missing_has": ["conditions_confirmed"],
    },
    {
        "group": "pregnancy",
        "message": "Dang cho con bu bi dau dau",
        "intent": "otc_recommendation",
        "llm": {"subject": "pregnancy_medication", "breastfeeding": True},
        "expect": {"breastfeeding": True},
        "missing_has": ["age"],
    },
    {
        "group": "pregnancy",
        "message": "Em bau 7 thang khong di ung thuoc",
        "intent": "otc_recommendation",
        "llm": {"pregnant": True, "pregnancy_month": 7, "allergies_confirmed": True, "allergies": []},
        "expect": {"pregnant": True, "pregnancy_month": 7, "allergies_confirmed": True},
        "missing_has": ["conditions_confirmed"],
    },
    {
        "group": "pregnancy",
        "message": "Phu nu co thai bi ho dang dung vitamin tong hop",
        "intent": "otc_recommendation",
        "llm": {"pregnant": True, "current_medications": ["vitamin tong hop"], "current_medications_confirmed": True},
        "expect": {"pregnant": True, "current_medications_confirmed": True},
        "expect_list_contains": {"current_medications": "vitamin tong hop"},
    },
    {
        "group": "pregnancy",
        "message": "Toi khong mang thai khong cho con bu",
        "intent": "otc_recommendation",
        "llm": {"pregnant": False, "breastfeeding": False, "pregnancy_breastfeeding_confirmed": True},
        "expect": {"pregnant": False, "breastfeeding": False, "pregnancy_breastfeeding_confirmed": True},
    },
    # chronic condition
    {
        "group": "chronic",
        "message": "Toi bi tang huyet ap muon mua thuoc cam",
        "intent": "otc_recommendation",
        "llm": {"conditions": ["hypertension"], "conditions_confirmed": True},
        "expect_list_contains": {"conditions": "hypertension"},
        "missing_has": ["age"],
    },
    {
        "group": "chronic",
        "message": "Toi co dau da day uong ibuprofen duoc khong",
        "intent": "otc_recommendation",
        "llm": {"conditions": ["stomach_ulcer"], "conditions_confirmed": True},
        "expect_list_contains": {"conditions": "stomach_ulcer"},
    },
    {
        "group": "chronic",
        "message": "Me toi bi suy than dang dau dau",
        "intent": "otc_recommendation",
        "llm": {"conditions": ["kidney_disease"], "conditions_confirmed": True},
        "expect_list_contains": {"conditions": "kidney_disease"},
    },
    {
        "group": "chronic",
        "message": "Toi bi hen suyen muon uong aspirin",
        "intent": "otc_recommendation",
        "llm": {"conditions": ["asthma"], "conditions_confirmed": True},
        "expect_list_contains": {"conditions": "asthma"},
    },
    {
        "group": "chronic",
        "message": "Toi bi suy gan va khong di ung thuoc",
        "intent": "otc_recommendation",
        "llm": {"conditions": ["liver_disease"], "conditions_confirmed": True, "allergies_confirmed": True},
        "expect": {"conditions_confirmed": True, "allergies_confirmed": True},
        "expect_list_contains": {"conditions": "liver_disease"},
    },
    # negation
    {
        "group": "negation",
        "message": "Toi 21 tuoi khong co benh nen",
        "intent": "otc_recommendation",
        "llm": {"age": 21, "conditions": [], "conditions_confirmed": True},
        "expect": {"age": 21, "conditions_confirmed": True},
    },
    {
        "group": "negation",
        "message": "Khong dung thuoc nao khac",
        "intent": "high_risk_context",
        "llm": {"current_medications": [], "current_medications_confirmed": True},
        "expect": {"current_medications_confirmed": True},
    },
    {
        "group": "negation",
        "message": "Khong di ung thuoc",
        "intent": "high_risk_context",
        "llm": {"allergies": [], "allergies_confirmed": True},
        "expect": {"allergies_confirmed": True},
    },
    {
        "group": "negation",
        "message": "Khong co gi ca",
        "intent": "high_risk_context",
        "llm": {"conditions": [], "conditions_confirmed": True, "allergies": [], "allergies_confirmed": True, "current_medications": [], "current_medications_confirmed": True},
        "expect": {"conditions_confirmed": True, "allergies_confirmed": True, "current_medications_confirmed": True},
    },
    {
        "group": "negation",
        "message": "Toi khong ro co di ung thuoc khong",
        "intent": "high_risk_context",
        "llm": {"allergies": [], "allergies_confirmed": None, "missing_context": ["allergies_confirmed"], "uncertain": True},
        "missing_has": ["allergies_confirmed"],
    },
    # drug interaction
    {
        "group": "interaction",
        "message": "Aspirin uong chung diclofenac duoc khong",
        "intent": "interaction",
        "llm": {"intent": "interaction", "current_medications": ["aspirin", "diclofenac"], "current_medications_confirmed": True},
        "expect_list_contains": {"current_medications": "aspirin"},
    },
    {
        "group": "interaction",
        "message": "Toi dang dung warfarin co uong ibuprofen duoc khong",
        "intent": "interaction",
        "llm": {"intent": "interaction", "current_medications": ["warfarin", "ibuprofen"], "current_medications_confirmed": True},
        "expect_list_contains": {"current_medications": "warfarin"},
    },
    {
        "group": "interaction",
        "message": "Dang uong thuoc huyet ap co dung pseudoephedrine khong",
        "intent": "interaction",
        "llm": {"intent": "interaction", "conditions": ["hypertension"], "current_medications": ["thuoc huyet ap", "pseudoephedrine"], "conditions_confirmed": True, "current_medications_confirmed": True},
        "expect_list_contains": {"conditions": "hypertension"},
    },
    {
        "group": "interaction",
        "message": "Metronidazole voi ruou co sao khong",
        "intent": "interaction",
        "llm": {"intent": "interaction", "current_medications": ["metronidazole", "alcohol"], "current_medications_confirmed": True},
        "expect_list_contains": {"current_medications": "metronidazole"},
    },
    {
        "group": "interaction",
        "message": "Dang dung clarithromycin va atorvastatin",
        "intent": "interaction",
        "llm": {"intent": "interaction", "current_medications": ["clarithromycin", "atorvastatin"], "current_medications_confirmed": True},
        "expect_list_contains": {"current_medications": "clarithromycin"},
    },
]


@patch("backend.services.llm_patient_context_extractor.LLMPatientContextExtractor.extract", new_callable=AsyncMock)
@pytest.mark.parametrize("case", CASES, ids=[f"{item['group']}:{idx}" for idx, item in enumerate(CASES, 1)])
def test_hybrid_patient_context_extractor_cases(mock_extract, case):
    if isinstance(case.get("llm"), Exception):
        mock_extract.side_effect = case["llm"]
    else:
        mock_extract.return_value = case.get("llm")
        
    service = PatientContextService()
    result = asyncio.run(service.assess_hybrid(case["message"], case["intent"]))
    context = result.patient_context

    for key, value in case.get("expect", {}).items():
        assert context.get(key) == value

    for key, value in case.get("expect_list_contains", {}).items():
        assert value in (context.get(key) or [])

    for missing in case.get("missing_has", []):
        assert missing in result.missing_context

    for flag in case.get("risk_has", []):
        assert flag in result.risk_flags


@patch("backend.services.llm_patient_context_extractor.LLMPatientContextExtractor.extract", new_callable=AsyncMock)
def test_hybrid_patient_context_falls_back_when_llm_fails(mock_extract):
    mock_extract.side_effect = RuntimeError("llm down")
    message = "Toi 21 tuoi khong co benh nen"
    service = PatientContextService()
    result = asyncio.run(service.assess_hybrid(message, "otc_recommendation"))

    assert result.patient_context["age"] == 21
    assert result.patient_context["conditions_confirmed"] is True
