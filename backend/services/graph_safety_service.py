"""File-backed graph safety checks for medicine questions.

This mirrors the Neo4j knowledge graph checks while keeping the API runnable
without a local Neo4j server. The public result shape is intentionally stable
so a future Neo4j implementation can replace this class behind the same
contract.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, Iterable, List


ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DDINTER = ROOT_DIR / "data" / "processed" / "ddinter_interaction_edges.jsonl"
DEFAULT_OTC = ROOT_DIR / "data" / "processed" / "otc_condition_guardrails.jsonl"

ALIASES = {
    "aspirin": ["aspirin", "acetylsalicylic acid", "acid acetylsalicylic"],
    "paracetamol": ["paracetamol", "acetaminophen"],
    "diabetes": [
        "diabetes",
        "tieu duong",
        "dai thao duong",
        "benh tieu duong",
        "duong huyet",
    ],
    "cold_flu": [
        "thuoc cam",
        "thuoc cam cum",
        "cam",
        "cam cum",
        "nghet mui",
        "so mui",
        "cold",
        "flu",
    ],
}

COMMON_DRUG_TERMS = {
    "aspirin",
    "acetylsalicylic acid",
    "warfarin",
    "ibuprofen",
    "paracetamol",
    "acetaminophen",
    "atorvastatin",
    "simvastatin",
    "rosuvastatin",
    "clarithromycin",
    "erythromycin",
    "itraconazole",
    "ketoconazole",
    "diclofenac",
    "metronidazole",
    "amoxicillin",
    "pseudoephedrine",
    "phenylephrine",
    "ephedrine",
}

INTERACTION_RECOMMENDATION = (
    "Kh\u00f4ng t\u1ef1 ph\u1ed1i h\u1ee3p; "
    "h\u1ecfi b\u00e1c s\u0129/d\u01b0\u1ee3c s\u0129 "
    "tr\u01b0\u1edbc khi d\u00f9ng c\u00f9ng nhau."
)


def strip_accents(text: str) -> str:
    value = (text or "").replace("\u0110", "D").replace("\u0111", "d")
    decomposed = unicodedata.normalize("NFD", value)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", strip_accents(text).lower()).strip()


def iter_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def variants(term: str) -> List[str]:
    norm = normalize(term)
    for canonical, names in ALIASES.items():
        normalized_names = {normalize(name) for name in names}
        if norm == canonical or norm in normalized_names:
            return sorted(normalized_names)
    return [norm]


def mentioned(text: str, terms: List[str]) -> bool:
    normalized = normalize(text)
    return any(normalize(term) in normalized for term in terms)


class GraphSafetyService:
    """Safety checks over DDInter and curated condition guardrails."""

    def __init__(self, ddinter_path: Path = DEFAULT_DDINTER, otc_path: Path = DEFAULT_OTC) -> None:
        self.ddinter_path = ddinter_path
        self.otc_path = otc_path
        self._ddinter_edges: List[Dict[str, Any]] | None = None
        self._otc_rules: List[Dict[str, Any]] | None = None
        self._interaction_index: Dict[tuple, List[Dict[str, Any]]] | None = None

    def check(self, query: str) -> Dict[str, Any]:
        drugs = self.detect_query_drugs(query)
        findings = self.check_condition_otc(query) + self.check_interactions(drugs)
        return {
            "detected_drugs": drugs,
            "findings": findings,
            "highest_risk": self.highest_risk(findings),
            "should_warn": bool(findings),
        }

    def _load_ddinter_edges(self) -> List[Dict[str, Any]]:
        if self._ddinter_edges is None:
            self._ddinter_edges = list(iter_jsonl(self.ddinter_path))
        return self._ddinter_edges

    def _load_otc_rules(self) -> List[Dict[str, Any]]:
        if self._otc_rules is None:
            self._otc_rules = list(iter_jsonl(self.otc_path))
        return self._otc_rules

    def _load_interaction_index(self) -> Dict[tuple, List[Dict[str, Any]]]:
        if self._interaction_index is not None:
            return self._interaction_index

        index: Dict[tuple, List[Dict[str, Any]]] = {}
        for edge in self._load_ddinter_edges():
            edge_a = normalize(str(edge.get("drug_a") or ""))
            edge_b = normalize(str(edge.get("drug_b") or ""))
            if edge_a and edge_b:
                index.setdefault(tuple(sorted((edge_a, edge_b))), []).append(edge)

        self._interaction_index = index
        return index

    def detect_query_drugs(self, query: str) -> List[str]:
        normalized = normalize(query)
        found = {term for term in COMMON_DRUG_TERMS if normalize(term) in normalized}

        if len(found) < 2:
            for edge in self._load_ddinter_edges():
                for key in ("drug_a", "drug_b"):
                    name = str(edge.get(key) or "")
                    if name and normalize(name) in normalized:
                        found.add(name)
                if len(found) >= 2:
                    break

        deduped: Dict[str, str] = {}
        for name in found:
            deduped.setdefault(normalize(name), name)
        return [deduped[key] for key in sorted(deduped)]

    def check_condition_otc(self, query: str) -> List[Dict[str, Any]]:
        findings = []
        for rule in self._load_otc_rules():
            condition = str(rule.get("condition") or "")
            category = str(rule.get("otc_category") or "")
            if not mentioned(query, ALIASES.get(condition, [condition])):
                continue
            if category == "cold_flu" and not mentioned(query, ALIASES["cold_flu"]):
                continue
            findings.append(
                {
                    "type": "condition_otc_caution",
                    "severity": rule.get("risk_level") or "caution",
                    "condition": condition,
                    "otc_category": category,
                    "ingredients_to_avoid_or_check": rule.get("ingredients_to_avoid_or_check") or [],
                    "recommendation": rule.get("recommendation"),
                    "safer_options": rule.get("safer_options") or [],
                    "red_flags": rule.get("red_flags") or [],
                    "citations": rule.get("citations") or [],
                    "source": "otc_condition_guardrail",
                }
            )
        return findings

    def check_interactions(self, drugs: List[str]) -> List[Dict[str, Any]]:
        if len(drugs) < 2:
            return []

        drug_variants = {drug: variants(drug) for drug in drugs}
        interaction_index = self._load_interaction_index()
        findings = []
        seen = set()

        for index, left in enumerate(drugs):
            for right in drugs[index + 1 :]:
                for left_variant in drug_variants[left]:
                    for right_variant in drug_variants[right]:
                        key = tuple(sorted((left_variant, right_variant)))
                        for edge in interaction_index.get(key, []):
                            edge_key = (edge.get("drug_a"), edge.get("drug_b"), edge.get("level"))
                            if edge_key in seen:
                                continue
                            seen.add(edge_key)
                            findings.append(
                                {
                                    "type": "drug_drug_interaction",
                                    "severity": edge.get("level") or "Unknown",
                                    "drug_a": edge.get("drug_a"),
                                    "drug_b": edge.get("drug_b"),
                                    "source": edge.get("source") or "ddinter",
                                    "source_url": edge.get("source_url"),
                                    "recommendation": INTERACTION_RECOMMENDATION,
                                }
                            )
        return findings

    def highest_risk(self, findings: List[Dict[str, Any]]) -> str:
        order = {"major": 4, "moderate": 3, "caution": 2, "minor": 1, "unknown": 0}
        if not findings:
            return "none"
        return max(
            (str(row.get("severity") or "unknown") for row in findings),
            key=lambda item: order.get(item.lower(), 0),
        )


def format_graph_warning(findings: List[Dict[str, Any]]) -> str:
    if not findings:
        return ""
    lines = ["C\u1ea3nh b\u00e1o an to\u00e0n t\u1eeb graph:"]
    for finding in findings:
        if finding["type"] == "condition_otc_caution":
            ingredients = ", ".join(finding.get("ingredients_to_avoid_or_check") or [])
            lines.append(
                "- B\u1ec7nh n\u1ec1n/OTC: n\u00ean tr\u00e1nh ho\u1eb7c "
                "h\u1ecfi d\u01b0\u1ee3c s\u0129 tr\u01b0\u1edbc khi d\u00f9ng "
                f"{ingredients}."
            )
            if finding.get("recommendation"):
                lines.append(f"  L\u00fd do: {finding['recommendation']}")
        elif finding["type"] == "drug_drug_interaction":
            lines.append(
                "- T\u01b0\u01a1ng t\u00e1c thu\u1ed1c: "
                f"{finding.get('drug_a')} + {finding.get('drug_b')} "
                f"m\u1ee9c {finding.get('severity')}. {finding.get('recommendation')}"
            )
    return "\n".join(lines)
