"""Dynamic confidence scoring for SafeRagService responses."""
from __future__ import annotations

from typing import Any, Dict, List, Optional


def compute_confidence(
    action: str,
    intent: str,
    citations: List[Dict],
    graph_result: Dict,
    reranker_top_score: Optional[float] = None,
    planner_confidence: Optional[float] = None,
) -> float:
    """Compute a bounded response confidence score from evidence signals."""
    normalized_action = (action or "").lower()
    if normalized_action == "emergency":
        return 1.0

    base_scores = {
        "allow": 0.70,
        "allow_with_caution": 0.55,
        "handoff": 0.20,
        "insufficient_evidence": 0.20,
    }
    score = base_scores.get(normalized_action, 0.50)
    graph = graph_result or {}
    citation_count = len(citations or [])
    reranker_score = _to_float(reranker_top_score)
    planner_score = _to_float(planner_confidence)

    if citation_count >= 3:
        score += 0.10
    if citation_count >= 5:
        score += 0.05
    if graph.get("should_warn") is True:
        score -= 0.08
    if reranker_score is not None and reranker_score > 0.7:
        score += 0.07
    if planner_score is not None and planner_score > 0.8:
        score += 0.05

    if normalized_action == "allow_with_caution" and graph.get("highest_risk") == "high":
        score -= 0.10
    if citation_count == 0:
        score = min(score, 0.40)

    return round(max(0.0, min(1.0, score)), 2)


def _to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
