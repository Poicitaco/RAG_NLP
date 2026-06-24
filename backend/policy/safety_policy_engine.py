"""Bo may chinh sach an toan lam sang dua tren cau hinh.

Muc tieu la giu cac quyet dinh dinh tuyen lam sang trong data/config/clinical_policy.json
thay vi them mot nhanh Python moi cho moi truong hop kiem thu.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
import json
import re
from pathlib import Path
from typing import Any, Iterable
import unicodedata


ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_POLICY_PATH = ROOT_DIR / "data" / "config" / "clinical_policy.json"


@dataclass(frozen=True)
class PolicyDecision:
    matched: bool
    rule_id: str = ""
    intent: str = ""
    action: str = ""
    subtype: str = ""
    reason: str = ""
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


def normalize_text(text: str) -> str:
    value = (text or "").lower().replace("\u0111", "d")
    decomposed = unicodedata.normalize("NFD", value)
    return " ".join(
        "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn").split()
    )


def _term_present(normalized_text: str, term: str) -> bool:
    normalized_term = normalize_text(term)
    if not normalized_term:
        return False
    if " " in normalized_term:
        return bool(re.search(r"\b" + re.escape(normalized_term) + r"\b", normalized_text))
    return normalized_term in set(re.findall(r"[a-z0-9]+", normalized_text))


def _contains_any(normalized_text: str, terms: Iterable[str]) -> bool:
    return any(_term_present(normalized_text, term) for term in terms)


class SafetyPolicyEngine:
    def __init__(self, policy_path: Path = DEFAULT_POLICY_PATH) -> None:
        self.policy_path = policy_path
        self.policy = self._load_policy(policy_path)
        self.rules = sorted(
            self.policy.get("rules") or [],
            key=lambda rule: int(rule.get("priority") or 0),
            reverse=True,
        )

    @staticmethod
    def _load_policy(path: Path) -> dict[str, Any]:
        if not path.exists():
            return {"schema_version": "missing", "rules": []}
        return json.loads(path.read_text(encoding="utf-8"))

    def evaluate(self, question: str) -> PolicyDecision:
        normalized = normalize_text(question)
        for rule in self.rules:
            if self._matches_rule(normalized, rule):
                return PolicyDecision(
                    matched=True,
                    rule_id=str(rule.get("id") or ""),
                    intent=str(rule.get("intent") or ""),
                    action=str(rule.get("action") or ""),
                    subtype=str(rule.get("subtype") or ""),
                    reason=str(rule.get("reason") or ""),
                    warnings=list(rule.get("warnings") or []),
                    metadata={
                        "policy_schema": self.policy.get("schema_version"),
                        "policy_path": str(self.policy_path),
                        "priority": rule.get("priority"),
                    },
                )
        return PolicyDecision(matched=False)

    def _matches_rule(self, normalized: str, rule: dict[str, Any]) -> bool:
        if self._matches_any_pattern(normalized, rule.get("blocked_patterns") or []):
            return False

        all_terms = rule.get("all_terms") or []
        if all_terms and not all(_term_present(normalized, term) for term in all_terms):
            return False

        all_groups = rule.get("all_groups") or []
        for group in all_groups:
            if not _contains_any(normalized, group):
                return False

        any_terms = rule.get("any_terms") or []
        any_patterns = rule.get("any_patterns") or []
        numeric_overdose = rule.get("numeric_overdose") or {}
        has_any_gate = bool(any_terms or any_patterns or numeric_overdose)
        if has_any_gate and not (
            _contains_any(normalized, any_terms)
            or self._matches_any_pattern(normalized, any_patterns)
            or self._matches_numeric_overdose(normalized, numeric_overdose)
        ):
            return False

        return True

    @staticmethod
    def _matches_any_pattern(normalized: str, patterns: Iterable[str]) -> bool:
        return any(re.search(pattern, normalized) for pattern in patterns)

    @staticmethod
    def _matches_numeric_overdose(normalized: str, config: dict[str, Any]) -> bool:
        if not config:
            return False
        context_pattern = str(config.get("requires_context_pattern") or "")
        if context_pattern and not re.search(context_pattern, normalized):
            return False
        min_value = int(config.get("min_value") or 0)
        values = [int(value) for value in re.findall(r"\b(\d{1,2})\b", normalized)]
        return any(value >= min_value for value in values)


@lru_cache(maxsize=1)
def get_safety_policy_engine() -> SafetyPolicyEngine:
    return SafetyPolicyEngine()
