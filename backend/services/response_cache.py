"""Simple in-memory TTL cache for RAG responses."""
from __future__ import annotations
import hashlib
import time
from typing import Any, Dict, Optional


class ResponseCache:
    """TTL dict cache. Key = hash(question + patient_context_fingerprint)."""

    def __init__(self, ttl_seconds: int = 300, max_size: int = 500) -> None:
        self._cache: Dict[str, tuple[float, Any]] = {}
        self.ttl = ttl_seconds
        self.max_size = max_size

    def _make_key(self, question: str, patient_context: Optional[Dict] = None) -> str:
        fingerprint = question.strip().lower()
        if patient_context:
            # Chỉ hash các fields ảnh hưởng đến câu trả lời
            relevant = {k: patient_context.get(k) for k in
                       ("age", "conditions", "allergies", "current_medications") if patient_context.get(k)}
            fingerprint += str(sorted(relevant.items()))
        return hashlib.md5(fingerprint.encode()).hexdigest()

    def get(self, question: str, patient_context: Optional[Dict] = None) -> Optional[Any]:
        key = self._make_key(question, patient_context)
        entry = self._cache.get(key)
        if entry is None:
            return None
        ts, value = entry
        if time.time() - ts > self.ttl:
            del self._cache[key]
            return None
        return value

    def set(self, question: str, value: Any, patient_context: Optional[Dict] = None) -> None:
        if len(self._cache) >= self.max_size:
            # Evict oldest entry
            oldest = min(self._cache, key=lambda k: self._cache[k][0])
            del self._cache[oldest]
        key = self._make_key(question, patient_context)
        self._cache[key] = (time.time(), value)

    def clear(self) -> None:
        self._cache.clear()


_cache = ResponseCache()


def get_response_cache() -> ResponseCache:
    return _cache
