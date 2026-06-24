"""Semantic rule mapping for matrix-driven medication safety routing.

This module keeps symptom/OTC routing data-driven. New user phrasing should be
added to ``data/config/otc_safety_matrix.json`` instead of adding more if/else
branches in the backend.
"""
from __future__ import annotations

import json
import math
import os
import re
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_MATRIX_PATH = ROOT_DIR / "data" / "config" / "otc_safety_matrix.json"
DEFAULT_LOCAL_MODEL = "BAAI/bge-m3"
RULE_ANCHORS = {
    "di_ngoai_tieu_chay": [
        "tieu chay",
        "di ngoai",
        "ia chay",
        "tao thao",
        "dau bung di ngoai",
        "bun ia",
        "buon ia",
    ],
    "tieu_duong_cam_cum": [
        "cam",
        "cum",
        "cam cum",
        "thuoc cam",
        "ho",
        "nghet mui",
        "so mui",
        "tieu duong bi cam",
        "huyet ap mua thuoc cam",
    ],
    "kem_bo_sung": [
        "kem",
        "zinc",
        "bo sung kem",
        "vien kem",
    ],
}
RULE_NEGATIVES = {
    "di_ngoai_tieu_chay": [
        "khong di ngoai",
        "khong di duoc",
        "tao bon",
        "bon",
        "may ngay roi khong di ngoai",
    ],
    "tieu_duong_cam_cum": [
        "khang sinh",
        "bia",
        "ruou",
        "gout",
        "dau khop",
        "dau lung",
        "dau bao tu",
        "dau da day",
    ],
    "kem_bo_sung": [
        "khang sinh",
        "bia",
        "ruou",
        "dau dau",
        "dau khop",
        "dau lung",
        "gout",
        "huyet ap",
        "dau bao tu",
        "dau da day",
    ],
}


def normalize_text(text: str) -> str:
    value = (text or "").replace("Đ", "D").replace("đ", "d").lower()
    decomposed = unicodedata.normalize("NFD", value)
    stripped = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", stripped).strip()


def token_set(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", normalize_text(text)))


def contains_phrase(text: str, phrase: str) -> bool:
    normalized_text = normalize_text(text)
    normalized_phrase = normalize_text(phrase)
    if not normalized_phrase:
        return False
    if " " in normalized_phrase:
        return re.search(r"\b" + re.escape(normalized_phrase) + r"\b", normalized_text) is not None
    return normalized_phrase in token_set(normalized_text)


def cosine(left: List[float], right: List[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def lexical_score(question: str, texts: Iterable[str]) -> float:
    query_tokens = token_set(question)
    if not query_tokens:
        return 0.0
    best = 0.0
    normalized_question = normalize_text(question)
    for text in texts:
        normalized_text = normalize_text(text)
        if normalized_text and normalized_text in normalized_question:
            best = max(best, 1.0)
            continue
        terms = token_set(text)
        if not terms:
            continue
        overlap = len(query_tokens & terms)
        best = max(best, overlap / max(len(terms), 1))
    return best


class EmbeddingClient:
    """Small local embedding wrapper for matrix rule matching."""

    def __init__(self) -> None:
        self.provider = os.getenv("RULE_EMBEDDING_PROVIDER", "local").strip().lower()
        self.local_model_name = os.getenv("RULE_LOCAL_EMBEDDING_MODEL", DEFAULT_LOCAL_MODEL).strip()

    def embed(self, texts: List[str]) -> Optional[List[List[float]]]:
        if not texts:
            return []
        return self._embed_local(texts)

    def _embed_local(self, texts: List[str]) -> Optional[List[List[float]]]:
        try:
            model = _load_local_model(self.local_model_name)
            vectors = model.encode(texts, batch_size=len(texts), normalize_embeddings=True, show_progress_bar=False)
            return [vector.tolist() for vector in vectors]
        except Exception:
            return None


@lru_cache(maxsize=2)
def _load_local_model(model_name: str):
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(model_name)


class SemanticRuleMapper:
    """Map a free-form user question to the closest clinical rule in JSON."""

    def __init__(self, matrix_path: Path = DEFAULT_MATRIX_PATH) -> None:
        self.matrix_path = matrix_path
        self.embedding_client = EmbeddingClient()
        self.threshold = float(os.getenv("RULE_MATCH_THRESHOLD", "0.48"))
        self._rules: Optional[List[Dict[str, Any]]] = None
        self._rule_vectors: Optional[List[List[float]]] = None

    def map(self, question: str) -> Dict[str, Any]:
        rules = self._load_rules()
        if not rules:
            return {"matched": False, "reason": "matrix_empty"}

        lexical_matches = [
            (lexical_score(question, self._rule_texts(rule)), rule)
            for rule in rules
            if self._rule_allowed(rule, question)
        ]
        lexical_matches.sort(key=lambda item: item[0], reverse=True)
        if lexical_matches and lexical_matches[0][0] >= 0.72:
            return self._context(lexical_matches[0][1], lexical_matches[0][0], "lexical")

        vectors = self.embedding_client.embed([question])
        rule_vectors = self._get_rule_vectors()
        if vectors and rule_vectors:
            scored = [
                (cosine(vectors[0], rule_vector), rule)
                for rule, rule_vector in zip(rules, rule_vectors)
                if self._rule_allowed(rule, question)
            ]
            scored.sort(key=lambda item: item[0], reverse=True)
            if scored and scored[0][0] >= self.threshold:
                return self._context(scored[0][1], scored[0][0], self.embedding_client.provider)

        if lexical_matches and lexical_matches[0][0] >= 0.25:
            return self._context(lexical_matches[0][1], lexical_matches[0][0], "lexical_fallback")
        return {
            "matched": False,
            "best_score": round(lexical_matches[0][0], 4) if lexical_matches else 0.0,
            "reason": "below_threshold",
        }

    def _load_rules(self) -> List[Dict[str, Any]]:
        if self._rules is not None:
            return self._rules
        if not self.matrix_path.exists():
            self._rules = []
            return self._rules
        with self.matrix_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        self._rules = list(payload.get("clinical_rules") or [])
        return self._rules

    def _get_rule_vectors(self) -> Optional[List[List[float]]]:
        if self._rule_vectors is not None:
            return self._rule_vectors
        texts = ["\n".join(self._rule_texts(rule)) for rule in self._load_rules()]
        self._rule_vectors = self.embedding_client.embed(texts)
        return self._rule_vectors

    def _rule_texts(self, rule: Dict[str, Any]) -> List[str]:
        values = [
            rule.get("primary_intent"),
            rule.get("target_otc_group"),
            rule.get("retrieval_query"),
        ]
        values.extend(rule.get("keywords_synonyms") or [])
        values.extend(rule.get("priority_otc_ingredients") or [])
        values.extend(rule.get("response_focus") or [])
        return [str(value) for value in values if value]

    def _rule_allowed(self, rule: Dict[str, Any], question: str) -> bool:
        rule_id = str(rule.get("id") or "")
        if any(contains_phrase(question, phrase) for phrase in RULE_NEGATIVES.get(rule_id, [])):
            return False
        anchors = RULE_ANCHORS.get(rule_id, [])
        if not anchors:
            return True
        return any(contains_phrase(question, phrase) for phrase in anchors)

    def _context(self, rule: Dict[str, Any], score: float, method: str) -> Dict[str, Any]:
        return {
            "matched": True,
            "method": method,
            "score": round(float(score), 4),
            "rule_id": rule.get("id"),
            "primary_intent": rule.get("primary_intent"),
            "target_otc_group": rule.get("target_otc_group"),
            "retrieval_query": rule.get("retrieval_query"),
            "keywords_synonyms": rule.get("keywords_synonyms") or [],
            "must_avoid_sections_in_rag": rule.get("must_avoid_sections_in_rag") or [],
            "priority_otc_ingredients": rule.get("priority_otc_ingredients") or [],
            "must_avoid_ingredients": rule.get("must_avoid_ingredients") or [],
            "emergency_flags": rule.get("emergency_flags") or [],
            "response_focus": rule.get("response_focus") or [],
            "citations": rule.get("citations") or [],
        }
