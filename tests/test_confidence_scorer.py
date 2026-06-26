from __future__ import annotations

from backend.services.confidence_scorer import compute_confidence


def _citations(count: int) -> list[dict[str, str]]:
    return [{"id": f"S{i}"} for i in range(1, count + 1)]


def test_emergency_confidence_is_always_maximum() -> None:
    assert compute_confidence(
        action="emergency",
        intent="overdose",
        citations=[],
        graph_result={},
        reranker_top_score=0.0,
        planner_confidence=0.0,
    ) == 1.0


def test_allow_confidence_combines_positive_evidence_signals() -> None:
    score = compute_confidence(
        action="allow",
        intent="otc_recommendation",
        citations=_citations(5),
        graph_result={"should_warn": True},
        reranker_top_score=0.8,
        planner_confidence=0.9,
    )

    # should_warn=True bây giờ GIẢM score (-0.08) thay vì tăng
    # 0.70 (allow) + 0.10 (>=3 cit) + 0.05 (>=5 cit) - 0.08 (warn) + 0.07 (reranker) + 0.05 (planner) = 0.89
    assert score == 0.89


def test_allow_with_caution_high_risk_penalty_is_applied() -> None:
    score = compute_confidence(
        action="allow_with_caution",
        intent="otc_recommendation",
        citations=_citations(3),
        graph_result={"highest_risk": "high"},
    )

    assert score == 0.55


def test_handoff_without_citations_stays_low_confidence() -> None:
    score = compute_confidence(
        action="handoff",
        intent="unknown",
        citations=[],
        graph_result={},
    )

    # handoff base=0.20, no citations: cap min(0.20, 0.40) = 0.20 (cap không áp dụng vì 0.20 < 0.40)
    assert score == 0.2


def test_unknown_action_uses_default_base_score() -> None:
    score = compute_confidence(
        action="needs_clarification",
        intent="missing_context",
        citations=_citations(3),
        graph_result={},
    )

    assert score == 0.6


def test_invalid_optional_scores_are_ignored() -> None:
    score = compute_confidence(
        action="allow",
        intent="otc_recommendation",
        citations=_citations(3),
        graph_result={},
        reranker_top_score="not-a-number",
        planner_confidence={"bad": "shape"},
    )

    assert score == 0.8
