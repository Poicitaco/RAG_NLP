from __future__ import annotations

from backend.services.patient_context_merger import merge_patient_context


def test_merge_patient_context_canonicalizes_condition_aliases() -> None:
    result = merge_patient_context(
        {"patient_context": {"conditions": ["cao huyet ap", "benh tim mach"]}},
        {
            "conditions": [
                "hypertension",
                "tang huyet ap",
                "suy tim",
                "dau bao tu",
                "hen suyen",
            ],
            "conditions_confirmed": True,
        },
    )

    assert result["patient_context"]["conditions"] == [
        "hypertension",
        "heart_disease",
        "stomach_ulcer",
        "asthma",
    ]
    assert result["patient_context"]["conditions_confirmed"] is True


def test_merge_patient_context_keeps_unknown_condition_labels() -> None:
    result = merge_patient_context(
        {"patient_context": {"conditions": ["benh la"]}},
        {"conditions": ["condition_from_llm"]},
    )

    assert result["patient_context"]["conditions"] == ["benh la", "condition_from_llm"]
