"""Export pharmaceutical safety data to Neo4j-friendly CSV files.

The export is intentionally conservative: it creates stable IDs and keeps source
URLs/trust metadata so the graph can explain why a warning fired.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List


DEFAULT_DDINTER = "data/processed/ddinter_interaction_edges.jsonl"
DEFAULT_OTC = "data/processed/otc_condition_guardrails.jsonl"
DEFAULT_DAV = "data/processed/dav_all_drugs.jsonl"
DEFAULT_DUOCTHU = "data/processed/trungtamthuoc_duocthu_monographs.jsonl"
DEFAULT_OUTPUT = "data/graph/neo4j_import"


def strip_accents(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text or "")
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def stable_key(value: str) -> str:
    text = strip_accents(value).lower()
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return text or "unknown"


def safe_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return str(value).replace("\r", " ").replace("\n", " ").strip()


def iter_jsonl(path: Path, limit: int | None = None) -> Iterator[Dict[str, Any]]:
    if not path.exists():
        return
    count = 0
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            yield json.loads(line)
            count += 1
            if limit is not None and count >= limit:
                return


def add_unique(rows: OrderedDict[str, Dict[str, Any]], row_id: str, row: Dict[str, Any]) -> None:
    if row_id and row_id not in rows:
        rows[row_id] = row


def split_dav_ingredients(raw: str) -> List[str]:
    raw = re.sub(r"\([^)]*\)", " ", raw or "")
    parts = re.split(r";|\+|,|\bvà\b|\band\b", raw, flags=re.IGNORECASE)
    cleaned = []
    for part in parts:
        value = re.sub(r"\b\d+([.,]\d+)?\s*(mg|mcg|g|ml|iu|%)\b", " ", part, flags=re.IGNORECASE)
        value = re.sub(r"\s+", " ", value).strip(" :-")
        if 2 <= len(value) <= 90 and not value.lower().startswith(("moi ", "mỗi ", "thanh phan")):
            cleaned.append(value)
    return cleaned[:8]


def write_csv(path: Path, rows: Iterable[Dict[str, Any]], fieldnames: List[str]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: safe_text(row.get(key)) for key in fieldnames})
            count += 1
    return count


def build_graph(args: argparse.Namespace) -> Dict[str, int]:
    drugs: OrderedDict[str, Dict[str, Any]] = OrderedDict()
    ingredients: OrderedDict[str, Dict[str, Any]] = OrderedDict()
    products: OrderedDict[str, Dict[str, Any]] = OrderedDict()
    conditions: OrderedDict[str, Dict[str, Any]] = OrderedDict()
    otc_categories: OrderedDict[str, Dict[str, Any]] = OrderedDict()

    interactions: List[Dict[str, Any]] = []
    product_ingredients: List[Dict[str, Any]] = []
    monograph_refs: List[Dict[str, Any]] = []
    condition_warnings: List[Dict[str, Any]] = []
    category_warnings: List[Dict[str, Any]] = []

    for edge in iter_jsonl(Path(args.ddinter)):
        drug_a = safe_text(edge.get("drug_a"))
        drug_b = safe_text(edge.get("drug_b"))
        if not drug_a or not drug_b:
            continue
        id_a = "drug:" + stable_key(drug_a)
        id_b = "drug:" + stable_key(drug_b)
        add_unique(
            drugs,
            id_a,
            {"drug_id": id_a, "name": drug_a, "normalized_name": stable_key(drug_a), "source": "ddinter"},
        )
        add_unique(
            drugs,
            id_b,
            {"drug_id": id_b, "name": drug_b, "normalized_name": stable_key(drug_b), "source": "ddinter"},
        )
        interactions.append(
            {
                "from_id": id_a,
                "to_id": id_b,
                "interaction_id": edge.get("id"),
                "level": edge.get("level") or "Unknown",
                "source": "ddinter",
                "source_url": edge.get("source_url"),
                "license": edge.get("license"),
                "requires_review": edge.get("requires_review", True),
            }
        )

    for row in iter_jsonl(Path(args.duocthu), args.duocthu_limit):
        if row.get("source_kind") != "active_ingredient":
            continue
        name = safe_text(row.get("title"))
        if not name:
            continue
        ingredient_id = "ingredient:" + stable_key(name)
        add_unique(
            ingredients,
            ingredient_id,
            {
                "ingredient_id": ingredient_id,
                "name": name,
                "normalized_name": stable_key(name),
                "source": "trungtamthuoc_duocthu",
                "source_url": row.get("source_url"),
            },
        )
        monograph_refs.append(
            {
                "from_id": ingredient_id,
                "monograph_url": row.get("source_url"),
                "title": name,
                "section_count": row.get("section_count"),
                "trust_level": row.get("trust_level"),
            }
        )

    for row in iter_jsonl(Path(args.dav), args.dav_limit):
        reg = safe_text(row.get("registration_number"))
        name = safe_text(row.get("drug_name"))
        if not reg or not name:
            continue
        product_id = "product:" + stable_key(reg)
        add_unique(
            products,
            product_id,
            {
                "product_id": product_id,
                "registration_number": reg,
                "name": name,
                "active_ingredient_raw": row.get("active_ingredient"),
                "strength": row.get("strength"),
                "dosage_form": row.get("dosage_form"),
                "manufacturer": row.get("manufacturer_name"),
                "source": "dav_all",
                "source_url": row.get("source_url"),
            },
        )
        for ingredient_name in split_dav_ingredients(safe_text(row.get("active_ingredient"))):
            ingredient_id = "ingredient:" + stable_key(ingredient_name)
            add_unique(
                ingredients,
                ingredient_id,
                {
                    "ingredient_id": ingredient_id,
                    "name": ingredient_name,
                    "normalized_name": stable_key(ingredient_name),
                    "source": "dav_all",
                    "source_url": row.get("source_url"),
                },
            )
            product_ingredients.append(
                {
                    "from_id": product_id,
                    "to_id": ingredient_id,
                    "source": "dav_all",
                    "registration_number": reg,
                }
            )

    for rule in iter_jsonl(Path(args.otc)):
        condition = safe_text(rule.get("condition"))
        category = safe_text(rule.get("otc_category"))
        condition_id = "condition:" + stable_key(condition)
        category_id = "otc:" + stable_key(category)
        add_unique(
            conditions,
            condition_id,
            {
                "condition_id": condition_id,
                "name": condition,
                "name_vi": rule.get("condition_vi"),
                "normalized_name": stable_key(condition),
            },
        )
        add_unique(
            otc_categories,
            category_id,
            {"category_id": category_id, "name": category, "symptom_group": rule.get("symptom_group")},
        )
        for ingredient in rule.get("ingredients_to_avoid_or_check") or []:
            ingredient_id = "ingredient:" + stable_key(ingredient)
            add_unique(
                ingredients,
                ingredient_id,
                {
                    "ingredient_id": ingredient_id,
                    "name": ingredient,
                    "normalized_name": stable_key(ingredient),
                    "source": "otc_condition_guardrail",
                },
            )
            condition_warnings.append(
                {
                    "from_id": condition_id,
                    "to_id": ingredient_id,
                    "risk_level": rule.get("risk_level"),
                    "recommendation": rule.get("recommendation"),
                    "safer_options": json.dumps(rule.get("safer_options") or [], ensure_ascii=False),
                    "red_flags": json.dumps(rule.get("red_flags") or [], ensure_ascii=False),
                    "citations": json.dumps(rule.get("citations") or [], ensure_ascii=False),
                    "source": "otc_condition_guardrail",
                }
            )
            category_warnings.append(
                {
                    "from_id": category_id,
                    "to_id": ingredient_id,
                    "reason": "common OTC cold/flu ingredient requiring condition-aware screening",
                    "source": "otc_condition_guardrail",
                }
            )

    output = Path(args.output_dir)
    counts = {
        "drugs": write_csv(output / "drugs.csv", drugs.values(), ["drug_id", "name", "normalized_name", "source"]),
        "ingredients": write_csv(
            output / "ingredients.csv",
            ingredients.values(),
            ["ingredient_id", "name", "normalized_name", "source", "source_url"],
        ),
        "products": write_csv(
            output / "products.csv",
            products.values(),
            [
                "product_id",
                "registration_number",
                "name",
                "active_ingredient_raw",
                "strength",
                "dosage_form",
                "manufacturer",
                "source",
                "source_url",
            ],
        ),
        "conditions": write_csv(
            output / "conditions.csv",
            conditions.values(),
            ["condition_id", "name", "name_vi", "normalized_name"],
        ),
        "otc_categories": write_csv(
            output / "otc_categories.csv", otc_categories.values(), ["category_id", "name", "symptom_group"]
        ),
        "interacts_with": write_csv(
            output / "interacts_with.csv",
            interactions,
            ["from_id", "to_id", "interaction_id", "level", "source", "source_url", "license", "requires_review"],
        ),
        "product_has_ingredient": write_csv(
            output / "product_has_ingredient.csv",
            product_ingredients,
            ["from_id", "to_id", "source", "registration_number"],
        ),
        "ingredient_has_monograph": write_csv(
            output / "ingredient_has_monograph.csv",
            monograph_refs,
            ["from_id", "monograph_url", "title", "section_count", "trust_level"],
        ),
        "condition_caution_ingredient": write_csv(
            output / "condition_caution_ingredient.csv",
            condition_warnings,
            [
                "from_id",
                "to_id",
                "risk_level",
                "recommendation",
                "safer_options",
                "red_flags",
                "citations",
                "source",
            ],
        ),
        "otc_category_caution_ingredient": write_csv(
            output / "otc_category_caution_ingredient.csv",
            category_warnings,
            ["from_id", "to_id", "reason", "source"],
        ),
    }
    (output / "manifest.json").write_text(json.dumps(counts, ensure_ascii=False, indent=2), encoding="utf-8")
    return counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ddinter", default=DEFAULT_DDINTER)
    parser.add_argument("--otc", default=DEFAULT_OTC)
    parser.add_argument("--dav", default=DEFAULT_DAV)
    parser.add_argument("--duocthu", default=DEFAULT_DUOCTHU)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT)
    parser.add_argument("--dav-limit", type=int, default=None)
    parser.add_argument("--duocthu-limit", type=int, default=None)
    args = parser.parse_args()
    print(json.dumps(build_graph(args), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
