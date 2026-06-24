"""Optional cross-encoder reranking for retrieved RAG evidence."""
from __future__ import annotations

from typing import Any, Dict, List, Optional


RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class RerankerService:
    """Rerank retrieved rows with a sentence-transformers cross encoder.

    The service is intentionally optional: if sentence-transformers or the model
    cannot be loaded, callers receive the original results unchanged.
    """

    def __init__(self, model_name: str = RERANKER_MODEL) -> None:
        self.model_name = model_name
        self.model: Optional[Any] = None
        self.fallback_used = False
        self.last_reranked_count = 0
        self.last_top_score: Optional[float] = None
        self._load_model()

    def _load_model(self) -> None:
        try:
            from sentence_transformers import CrossEncoder

            self.model = CrossEncoder(self.model_name)
            self.fallback_used = False
        except Exception:
            self.model = None
            self.fallback_used = True

    def rerank(self, query: str, results: List[Dict]) -> List[Dict]:
        self.last_reranked_count = 0
        self.last_top_score = None

        if not results:
            self.fallback_used = self.model is None
            return results
        if self.model is None:
            self.fallback_used = True
            return results

        candidates = results[:20]
        pairs = [(query, self._row_text(row)) for row in candidates]
        try:
            scores = self.model.predict(pairs)
        except Exception:
            self.fallback_used = True
            return results

        reranked: List[Dict] = []
        for row, score in zip(candidates, scores):
            row_with_score = dict(row)
            row_with_score["rerank_score"] = float(score)
            reranked.append(row_with_score)

        reranked.sort(key=lambda row: row.get("rerank_score", float("-inf")), reverse=True)
        top_results = reranked[:10]
        self.fallback_used = False
        self.last_reranked_count = len(top_results)
        if top_results:
            self.last_top_score = float(top_results[0]["rerank_score"])
        return top_results

    @staticmethod
    def _row_text(row: Dict) -> str:
        metadata = row.get("metadata") or {}
        parts = [
            row.get("document_preview"),
            row.get("content"),
            row.get("text"),
            row.get("document"),
            metadata.get("title") if isinstance(metadata, dict) else None,
            metadata.get("drug_name") if isinstance(metadata, dict) else None,
            metadata.get("section") if isinstance(metadata, dict) else None,
        ]
        return " ".join(str(part) for part in parts if part)
