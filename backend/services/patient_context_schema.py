"""Shared patient-context schema and canonical mappings."""
from __future__ import annotations

PATIENT_CONTEXT_FIELDS = {
    "age",
    "age_months",
    "weight_kg",
    "pregnant",
    "pregnancy_month",
    "breastfeeding",
    "conditions",
    "allergies",
    "current_medications",
    "conditions_confirmed",
    "allergies_confirmed",
    "current_medications_confirmed",
    "pregnancy_breastfeeding_confirmed",
}

CONDITION_CANONICAL = {
    "huyết áp": "hypertension",
    "cao huyết áp": "hypertension",
    "tiểu đường": "diabetes",
    "đái tháo đường": "diabetes",
    "bệnh tim": "heart_disease",
    "tim mạch": "heart_disease",
    "suy gan": "liver_disease",
    "bệnh gan": "liver_disease",
    "suy thận": "kidney_disease",
    "bệnh thận": "kidney_disease",
    "dạ dày": "stomach_ulcer",
    "loét dạ dày": "stomach_ulcer",
    "hen": "asthma",
    "suyễn": "asthma",
}
