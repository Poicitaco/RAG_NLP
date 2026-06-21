"""File-backed graph safety checks for medicine questions.

This mirrors the Neo4j knowledge graph checks while keeping the API runnable
without a local Neo4j server. A future Neo4j implementation can keep the same
public result shape.
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
    "diabetes": ["diabetes", "tieu duong", "dai thao duong", "đái tháo đường", "tiểu đường"],
    "cold_flu": ["thuoc cam", "cam cum", "cảm", "cảm cúm", "cold", "flu"],
}


def strip_accents(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text or "")
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
            return list(normalized_names)
    return [norm]


def mentioned(text: str, terms: List[str]) -> bool:
    normalized = normalize(text)
    return any(normalize(term) in normalized for term in terms)


class GraphSafetyService:
    """Safety checks over DDInter and curated condition guardrails."""

    def __init__(self, ddinter_path: Path = DEFAULT_DDINTER, otc_path: Path = DEFAULT_OTC) -> None:
        self.ddinter_path = ddinter_path
        self.otc_path = otc_path

    def check(self, query: str) -> Dict[str, Any]:
        drugs = self.detect_query_drugs(query)
        findings = self.check_condition_otc(query) + self.check_interactions(drugs)
        return {
            "detected_drugs": drugs,
            "findings": findings,
            "highest_risk": self.highest_risk(findings),
            "should_warn": bool(findings),
        }

    def detect_query_drugs(self, query: str) -> List[str]:
        normalized = normalize(query)
        known = {
            "aspirin",
            "acetylsalicylic acid",
            "warfarin",
            "ibuprofen",
            "paracetamol",
            "acetaminophen",
            "pseudoephedrine",
            "phenylephrine",
            "ephedrine",
        }
        found = {term for term in known if normalize(term) in normalized}

        if len(found) < 2:
            for edge in iter_jsonl(self.ddinter_path):
                for key in ("drug_a", "drug_b"):
                    name = str(edge.get(key) or "")
                    if name and normalize(name) in normalized:
                        found.add(name)
                if len(found) >= 2:
                    break
        return sorted(found)

    def check_condition_otc(self, query: str) -> List[Dict[str, Any]]:
        findings = []
        for rule in iter_jsonl(self.otc_path):
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
        findings = []
        for edge in iter_jsonl(self.ddinter_path):
            edge_a = normalize(str(edge.get("drug_a") or ""))
            edge_b = normalize(str(edge.get("drug_b") or ""))
            for index, left in enumerate(drugs):
                for right in drugs[index + 1 :]:
                    left_variants = drug_variants[left]
                    right_variants = drug_variants[right]
                    if (edge_a in left_variants and edge_b in right_variants) or (
                        edge_a in right_variants and edge_b in left_variants
                    ):
                        findings.append(
                            {
                                "type": "drug_drug_interaction",
                                "severity": edge.get("level") or "Unknown",
                                "drug_a": edge.get("drug_a"),
                                "drug_b": edge.get("drug_b"),
                                "source": edge.get("source") or "ddinter",
                                "source_url": edge.get("source_url"),
                                "recommendation": "Không tự phối hợp; hỏi bác sĩ/dược sĩ trước khi dùng cùng nhau.",
                            }
                        )
        return findings

    def highest_risk(self, findings: List[Dict[str, Any]]) -> str:
        order = {"major": 4, "moderate": 3, "caution": 2, "minor": 1, "unknown": 0}
        if not findings:
            return "none"
        return max((str(row.get("severity") or "unknown") for row in findings), key=lambda item: order.get(item.lower(), 0))


def format_graph_warning(findings: List[Dict[str, Any]]) -> str:
    if not findings:
        return ""
    lines = ["Cảnh báo an toàn từ graph:"]
    for finding in findings:
        if finding["type"] == "condition_otc_caution":
            ingredients = ", ".join(finding.get("ingredients_to_avoid_or_check") or [])
            lines.append(f"- Bệnh nền/OTC: nên tránh hoặc hỏi dược sĩ trước khi dùng {ingredients}.")
            if finding.get("recommendation"):
                lines.append(f"  Lý do: {finding['recommendation']}")
        elif finding["type"] == "drug_drug_interaction":
            lines.append(
                f"- Tương tác thuốc: {finding.get('drug_a')} + {finding.get('drug_b')} mức {finding.get('severity')}. "
                f"{finding.get('recommendation')}"
            )
    return "\n".join(lines)
