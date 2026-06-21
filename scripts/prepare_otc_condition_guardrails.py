"""Create curated OTC condition guardrail chunks for common public questions."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


RULES: List[Dict[str, Any]] = [
    {
        "id": "otc-condition:diabetes:cold:oral-decongestants",
        "condition": "diabetes",
        "condition_vi": "tiểu đường/đái tháo đường",
        "otc_category": "cold_flu",
        "symptom_group": "nghẹt mũi/cảm cúm",
        "ingredients_to_avoid_or_check": ["pseudoephedrine", "phenylephrine", "ephedrine"],
        "risk_level": "caution",
        "recommendation": (
            "Người có tiểu đường nên tránh tự mua thuốc cảm/nghẹt mũi có thuốc co mạch đường uống như "
            "pseudoephedrine, phenylephrine hoặc ephedrine nếu chưa hỏi bác sĩ/dược sĩ, vì nhóm này có thể làm tăng "
            "đường huyết, tăng huyết áp hoặc ảnh hưởng bệnh nền/thuốc đang dùng."
        ),
        "safer_options": [
            "xịt/rửa mũi bằng nước muối sinh lý",
            "thuốc chỉ chứa paracetamol để hạ sốt/đau nếu không có chống chỉ định và không dùng quá liều",
            "hỏi dược sĩ để chọn thuốc không đường nếu cần siro",
        ],
        "red_flags": [
            "sốt cao hoặc kéo dài",
            "khó thở, đau ngực",
            "đường huyết tăng cao bất thường",
            "đang dùng nhiều thuốc điều trị tiểu đường/tim mạch/huyết áp",
        ],
        "citations": [
            {
                "title": "21 CFR 341.80 OTC nasal decongestant warnings",
                "url": "https://www.law.cornell.edu/cfr/text/21/341.80",
                "note": "US OTC monograph warnings mention diabetes for decongestant products unless directed by a doctor.",
            },
            {
                "title": "Mayo Clinic Q and A: Decongestants can sometimes cause more harm than good",
                "url": "https://newsnetwork.mayoclinic.org/discussion/mayo-clinic-q-and-a-decongestants-can-sometimes-cause-more-harm-than-good/",
                "note": "Oral decongestants can raise blood pressure and blood sugar and may affect diabetes medicines.",
            },
            {
                "title": "FDA proposes ending oral phenylephrine as OTC nasal decongestant",
                "url": "https://www.fda.gov/news-events/press-announcements/fda-proposes-ending-use-oral-phenylephrine-otc-monograph-nasal-decongestant-active-ingredient-after",
                "note": "FDA states oral phenylephrine is proposed for removal from OTC monograph due to lack of effectiveness.",
            },
        ],
    }
]


def rule_to_chunk(rule: Dict[str, Any]) -> Dict[str, Any]:
    ingredients = ", ".join(rule["ingredients_to_avoid_or_check"])
    options = "; ".join(rule["safer_options"])
    red_flags = "; ".join(rule["red_flags"])
    citation_titles = "; ".join(citation["title"] for citation in rule["citations"])
    document = (
        f"Hỏi đáp OTC theo bệnh nền\n"
        f"Bệnh nền: {rule['condition_vi']} ({rule['condition']}).\n"
        f"Nhu cầu: mua thuốc cảm/cúm, đặc biệt khi có {rule['symptom_group']}.\n"
        f"Hoạt chất cần tránh hoặc hỏi dược sĩ/bác sĩ trước: {ingredients}.\n"
        f"Khuyến nghị: {rule['recommendation']}\n"
        f"Lựa chọn thường an toàn hơn để hỏi dược sĩ: {options}.\n"
        f"Dấu hiệu cần đi khám/gọi hỗ trợ y tế: {red_flags}.\n"
        f"Nguồn đối chiếu: {citation_titles}."
    )
    return {
        "id": rule["id"],
        "document": document,
        "metadata": {
            "source": "otc_condition_guardrail",
            "source_url": rule["citations"][0]["url"],
            "title": f"{rule['condition_vi']} - thuốc cảm cần thận trọng",
            "condition": rule["condition"],
            "condition_vi": rule["condition_vi"],
            "otc_category": rule["otc_category"],
            "ingredients": json.dumps(rule["ingredients_to_avoid_or_check"], ensure_ascii=False),
            "section": "condition_otc_safety",
            "type": "condition_guardrail",
            "risk_level": rule["risk_level"],
            "trust_level": "curated_condition_guardrail",
            "requires_review": True,
        },
    }


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rules-output", default="data/processed/otc_condition_guardrails.jsonl")
    parser.add_argument("--chunks-output", default="data/chunks/otc_condition_guardrail_chunks.jsonl")
    parser.add_argument("--manifest", default="data/processed/otc_condition_guardrails_manifest.json")
    args = parser.parse_args()

    rule_count = write_jsonl(Path(args.rules_output), RULES)
    chunk_count = write_jsonl(Path(args.chunks_output), (rule_to_chunk(rule) for rule in RULES))
    manifest = {
        "rules_output": args.rules_output,
        "chunks_output": args.chunks_output,
        "rule_count": rule_count,
        "chunk_count": chunk_count,
        "scope": "Initial curated OTC guardrails for condition-aware public medication advice.",
    }
    Path(args.manifest).write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
