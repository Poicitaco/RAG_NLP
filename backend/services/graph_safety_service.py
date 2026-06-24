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
    "hypertension": ["hypertension", "huyet ap", "cao huyet ap", "tang huyet ap"],
    "heart_disease": ["heart disease", "tim mach", "benh tim", "suy tim"],
    "kidney_disease": ["kidney disease", "suy than", "benh than", "hong than"],
    "liver_disease": ["liver disease", "suy gan", "benh gan", "vang da", "vang mat"],
    "stomach_ulcer": ["stomach ulcer", "dau bao tu", "viem loet da day", "loet da day"],
    "asthma": ["asthma", "hen", "suyen", "hen suyen"],
    "pregnancy": ["pregnancy", "mang thai", "co thai", "bau", "cho con bu"],
    "general": ["toi", "minh", "nguoi lon", "adult", "nam", "nu"],
    "zinc_supplement": [
        "kem",
        "zinc",
        "bo sung kem",
        "vien kem",
        "uong kem",
        "loai kem",
    ],
    "cold_flu": [
        "thuoc cam",
        "thuoc cam cum",
        "mua thuoc cam",
        "bi cam",
        "cam cum",
        "nghet mui",
        "so mui",
        "cold",
        "flu",
    ],
    "cough": ["ho", "thuoc ho", "siro ho", "ho khan", "ho dom", "long dom"],
    "diarrhea": [
        "tieu chay",
        "di ngoai",
        "ia",
        "buon ia",
        "buon di ngoai",
        "dau bung",
        "dau bung di ngoai",
        "quan bung",
        "tao thao",
        "di toilet",
        "cam tieu chay",
        "oresol",
    ],
    "vitamin_c": ["vitamin c", "c vitamin", "c sui", "c sủi", "lieu cao"],
    "pain_fever": [
        "giam dau",
        "ha sot",
        "dau dau",
        "dau bung",
        "dau lung",
        "dau khop",
        "sot",
        "pain",
        "fever",
    ],
}
CATEGORY_NEGATIVES = {
    "diarrhea": [
        "khong di ngoai",
        "khong di duoc",
        "may ngay roi khong di ngoai",
        "tao bon",
        "bon",
    ],
    "zinc_supplement": [
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
    "cold_flu": [
        "khang sinh",
        "bia",
        "ruou",
        "gout",
        "dau khop",
        "dau lung",
        "dau bao tu",
        "dau da day",
    ],
    "cough": [
        "loang xuong",
        "alendronic",
        "alendronate",
        "alendronat",
        "bisphosphonate",
        "ppi",
        "trao nguoc da day",
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

BUILTIN_CONDITION_RULES: List[Dict[str, Any]] = [
    {
        "id": "builtin:hypertension:cold:oral-decongestants",
        "condition": "hypertension",
        "otc_category": "cold_flu",
        "risk_level": "caution",
        "ingredients_to_avoid_or_check": ["pseudoephedrine", "phenylephrine", "ephedrine"],
        "recommendation": (
            "Ng\u01b0\u1eddi c\u00f3 t\u0103ng huy\u1ebft \u00e1p ho\u1eb7c b\u1ec7nh tim m\u1ea1ch "
            "kh\u00f4ng n\u00ean t\u1ef1 d\u00f9ng thu\u1ed1c c\u1ea3m/ngh\u1eb9t m\u0169i "
            "c\u00f3 nh\u00f3m co m\u1ea1ch \u0111\u01b0\u1eddng u\u1ed1ng nh\u01b0 pseudoephedrine, "
            "phenylephrine ho\u1eb7c ephedrine n\u1ebfu ch\u01b0a h\u1ecfi b\u00e1c s\u0129/d\u01b0\u1ee3c s\u0129."
        ),
    },
    {
        "id": "builtin:heart:cold:oral-decongestants",
        "condition": "heart_disease",
        "otc_category": "cold_flu",
        "risk_level": "caution",
        "ingredients_to_avoid_or_check": ["pseudoephedrine", "phenylephrine", "ephedrine"],
        "recommendation": (
            "Ng\u01b0\u1eddi c\u00f3 b\u1ec7nh tim m\u1ea1ch c\u1ea7n h\u1ecfi chuy\u00ean m\u00f4n "
            "tr\u01b0\u1edbc khi d\u00f9ng thu\u1ed1c c\u1ea3m c\u00f3 ch\u1ea5t co m\u1ea1ch, "
            "v\u00ec c\u00f3 th\u1ec3 l\u00e0m t\u0103ng nh\u1ecbp tim ho\u1eb7c huy\u1ebft \u00e1p."
        ),
    },
    {
        "id": "builtin:kidney:pain_fever:nsaids",
        "condition": "kidney_disease",
        "otc_category": "pain_fever",
        "risk_level": "caution",
        "ingredients_to_avoid_or_check": ["ibuprofen", "diclofenac", "naproxen", "aspirin"],
        "recommendation": (
            "Ng\u01b0\u1eddi c\u00f3 b\u1ec7nh th\u1eadn/suy th\u1eadn kh\u00f4ng n\u00ean t\u1ef1 d\u00f9ng "
            "NSAID nh\u01b0 ibuprofen, diclofenac, naproxen ho\u1eb7c aspirin \u0111\u1ec3 gi\u1ea3m \u0111au/h\u1ea1 s\u1ed1t "
            "n\u1ebfu ch\u01b0a h\u1ecfi b\u00e1c s\u0129/d\u01b0\u1ee3c s\u0129."
        ),
    },
    {
        "id": "builtin:liver:pain_fever:paracetamol",
        "condition": "liver_disease",
        "otc_category": "pain_fever",
        "risk_level": "caution",
        "ingredients_to_avoid_or_check": ["paracetamol", "acetaminophen", "alcohol"],
        "recommendation": (
            "Ng\u01b0\u1eddi c\u00f3 b\u1ec7nh gan c\u1ea7n h\u1ecfi b\u00e1c s\u0129/d\u01b0\u1ee3c s\u0129 "
            "tr\u01b0\u1edbc khi d\u00f9ng paracetamol/acetaminophen, \u0111\u1eb7c bi\u1ec7t n\u1ebfu c\u00f3 u\u1ed1ng r\u01b0\u1ee3u "
            "ho\u1eb7c \u0111ang d\u00f9ng nhi\u1ec1u thu\u1ed1c."
        ),
    },
    {
        "id": "builtin:stomach_ulcer:pain_fever:nsaids",
        "condition": "stomach_ulcer",
        "otc_category": "pain_fever",
        "risk_level": "caution",
        "ingredients_to_avoid_or_check": ["ibuprofen", "diclofenac", "naproxen", "aspirin"],
        "recommendation": (
            "Ng\u01b0\u1eddi \u0111au bao t\u1eed/vi\u00eam lo\u00e9t d\u1ea1 d\u00e0y c\u1ea7n tr\u00e1nh t\u1ef1 d\u00f9ng "
            "NSAID v\u00ec c\u00f3 th\u1ec3 l\u00e0m t\u0103ng nguy c\u01a1 \u0111au d\u1ea1 d\u00e0y ho\u1eb7c xu\u1ea5t huy\u1ebft."
        ),
    },
    {
        "id": "builtin:asthma:pain_fever:nsaids",
        "condition": "asthma",
        "otc_category": "pain_fever",
        "risk_level": "caution",
        "ingredients_to_avoid_or_check": ["aspirin", "ibuprofen", "diclofenac", "naproxen"],
        "recommendation": (
            "M\u1ed9t s\u1ed1 ng\u01b0\u1eddi hen/suy\u1ec5n c\u00f3 th\u1ec3 nh\u1ea1y c\u1ea3m v\u1edbi aspirin/NSAID; "
            "kh\u00f4ng n\u00ean t\u1ef1 d\u00f9ng n\u1ebfu t\u1eebng kh\u00f2 kh\u00e8, kh\u00f3 th\u1edf ho\u1eb7c d\u1ecb \u1ee9ng sau khi d\u00f9ng nh\u00f3m n\u00e0y."
        ),
    },
    {
        "id": "builtin:pregnancy:any:otc",
        "condition": "pregnancy",
        "otc_category": "",
        "risk_level": "caution",
        "ingredients_to_avoid_or_check": ["self-medication"],
        "recommendation": (
            "Ph\u1ee5 n\u1eef mang thai ho\u1eb7c cho con b\u00fa kh\u00f4ng n\u00ean t\u1ef1 mua thu\u1ed1c OTC "
            "n\u1ebfu ch\u01b0a h\u1ecfi b\u00e1c s\u0129/d\u01b0\u1ee3c s\u0129, v\u00ec l\u1ef1a ch\u1ecdn thu\u1ed1c ph\u1ee5 thu\u1ed9c tu\u1ed5i thai, "
            "tri\u1ec7u ch\u1ee9ng v\u00e0 thu\u1ed1c \u0111ang d\u00f9ng."
        ),
    },
]


def strip_accents(text: str) -> str:
    value = (text or "").replace("\u0110", "D").replace("\u0111", "d")
    decomposed = unicodedata.normalize("NFD", value)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def normalize(text: str) -> str:
    text_with_spaces = str(text or "").replace("_", " ")
    return re.sub(r"\s+", " ", strip_accents(text_with_spaces).lower()).strip()


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
    tokens = set(re.findall(r"[a-z0-9]+", normalized))
    for term in terms:
        normalized_term = normalize(term)
        if not normalized_term:
            continue
        if " " in normalized_term:
            if re.search(r"\b" + re.escape(normalized_term) + r"\b", normalized):
                return True
        elif normalized_term in tokens:
            return True
    return False


def category_blocked(query: str, category: str) -> bool:
    return any(mentioned(query, [term]) for term in CATEGORY_NEGATIVES.get(category, []))


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
        findings = self.check_condition_otc(query, drugs) + self.check_interactions(drugs)
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

    def check_condition_otc(self, query: str, drugs: List[str] = None) -> List[Dict[str, Any]]:
        findings = []
        seen_rules = set()
        drugs = drugs or self.detect_query_drugs(query)
        for rule in list(self._load_otc_rules()) + BUILTIN_CONDITION_RULES:
            rule_id = str(rule.get("id") or "")
            if rule_id and rule_id in seen_rules:
                continue
            if rule_id:
                seen_rules.add(rule_id)
            condition = str(rule.get("condition") or "")
            category = str(rule.get("otc_category") or "")
            ingredients = rule.get("ingredients_to_avoid_or_check") or []
            if condition and not mentioned(query, ALIASES.get(condition, [condition])):
                continue
            
            category_mentioned = False
            if not category or (category in ALIASES and mentioned(query, ALIASES[category])):
                category_mentioned = True
            
            ingredient_matched = False
            for drug in drugs:
                if normalize(drug) in [normalize(i) for i in ingredients]:
                    ingredient_matched = True
                    break
                    
            if not category_mentioned and not ingredient_matched:
                continue
                
            if category and category_blocked(query, category):
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
