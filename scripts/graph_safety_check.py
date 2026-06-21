"""File-backed safety check that mirrors the planned Neo4j graph queries."""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, Iterable, List


DEFAULT_DDINTER = "data/processed/ddinter_interaction_edges.jsonl"
DEFAULT_OTC = "data/processed/otc_condition_guardrails.jsonl"

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
        if norm == canonical or norm in {normalize(name) for name in names}:
            return [normalize(name) for name in names]
    return [norm]


def mentioned(text: str, terms: List[str]) -> bool:
    normalized = normalize(text)
    return any(normalize(term) in normalized for term in terms)


def detect_query_drugs(query: str, ddinter_path: Path) -> List[str]:
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

    # Add DDInter names that appear literally in the query; this keeps the demo
    # usable without loading a separate synonym service.
    if len(found) < 2:
        for edge in iter_jsonl(ddinter_path):
            for key in ("drug_a", "drug_b"):
                name = str(edge.get(key) or "")
                if name and normalize(name) in normalized:
                    found.add(name)
            if len(found) >= 2:
                break
    return sorted(found)


def check_interactions(drugs: List[str], ddinter_path: Path) -> List[Dict[str, Any]]:
    if len(drugs) < 2:
        return []
    drug_variants = {drug: variants(drug) for drug in drugs}
    findings = []
    for edge in iter_jsonl(ddinter_path):
        edge_a = normalize(str(edge.get("drug_a") or ""))
        edge_b = normalize(str(edge.get("drug_b") or ""))
        for i, left in enumerate(drugs):
            for right in drugs[i + 1 :]:
                left_variants = drug_variants[left]
                right_variants = drug_variants[right]
                if (edge_a in left_variants and edge_b in right_variants) or (
                    edge_a in right_variants and edge_b in left_variants
                ):
                    findings.append(
                        {
                            "type": "drug_drug_interaction",
                            "severity": edge.get("level"),
                            "drug_a": edge.get("drug_a"),
                            "drug_b": edge.get("drug_b"),
                            "source": edge.get("source"),
                            "source_url": edge.get("source_url"),
                            "recommendation": "Không tự phối hợp; hỏi bác sĩ/dược sĩ trước khi dùng cùng nhau.",
                        }
                    )
    return findings


def check_condition_otc(query: str, otc_path: Path) -> List[Dict[str, Any]]:
    findings = []
    for rule in iter_jsonl(otc_path):
        condition = str(rule.get("condition") or "")
        category = str(rule.get("otc_category") or "")
        if not mentioned(query, ALIASES.get(condition, [condition])):
            continue
        if category == "cold_flu" and not mentioned(query, ALIASES["cold_flu"]):
            continue
        findings.append(
            {
                "type": "condition_otc_caution",
                "condition": condition,
                "otc_category": category,
                "risk_level": rule.get("risk_level"),
                "ingredients_to_avoid_or_check": rule.get("ingredients_to_avoid_or_check"),
                "recommendation": rule.get("recommendation"),
                "safer_options": rule.get("safer_options"),
                "red_flags": rule.get("red_flags"),
                "citations": rule.get("citations"),
            }
        )
    return findings


def answer_from_findings(query: str, findings: List[Dict[str, Any]]) -> str:
    if not findings:
        return "Chưa tìm thấy cảnh báo có cấu trúc trong graph safety data. Nên hỏi dược sĩ nếu có bệnh nền, đang dùng thuốc khác, mang thai/cho con bú hoặc dùng thuốc kê đơn."

    lines = ["Kết quả kiểm tra an toàn theo graph:"]
    for finding in findings:
        if finding["type"] == "condition_otc_caution":
            ingredients = ", ".join(finding.get("ingredients_to_avoid_or_check") or [])
            lines.append(f"- Bệnh nền + OTC: nên tránh hoặc hỏi dược sĩ trước khi dùng nhóm/hoạt chất: {ingredients}.")
            if finding.get("recommendation"):
                lines.append(f"  Lý do: {finding['recommendation']}")
            safer = finding.get("safer_options") or []
            if safer:
                lines.append("  Có thể hỏi dược sĩ về lựa chọn an toàn hơn: " + "; ".join(safer))
        elif finding["type"] == "drug_drug_interaction":
            lines.append(
                f"- Tương tác thuốc: {finding['drug_a']} + {finding['drug_b']} mức {finding['severity']}. {finding['recommendation']}"
            )
    lines.append("Đây là cảnh báo hỗ trợ, không thay thế bác sĩ/dược sĩ.")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--ddinter", default=DEFAULT_DDINTER)
    parser.add_argument("--otc", default=DEFAULT_OTC)
    parser.add_argument("--json-output")
    args = parser.parse_args()

    drugs = detect_query_drugs(args.query, Path(args.ddinter))
    findings = check_condition_otc(args.query, Path(args.otc)) + check_interactions(drugs, Path(args.ddinter))
    result = {
        "query": args.query,
        "detected_drugs": drugs,
        "findings": findings,
        "answer": answer_from_findings(args.query, findings),
    }
    if args.json_output:
        Path(args.json_output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
