"""Data-driven query expansion built from DAV drug records."""
from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Union

from backend.safety.evidence_guardrails import normalize_text


logger = logging.getLogger(__name__)

# Medical synonyms tĩnh cho thuật ngữ y khoa tiếng Việt thường bị miss bởi DAV expansion
MEDICAL_SYNONYMS_VI: Dict[str, List[str]] = {
    "sot": ["tang than nhiet", "ha sot", "sot cao", "nhiet do cao"],
    "dau dau": ["nhuc dau", "dau cang dau"],
    "ho": ["viem hong", "khan tieng"],
    "tieu chay": ["roi loan tieu hoa", "phan long"],
    "dau da day": ["dau bung", "viem loet da day", "trao nguoc"],
    "tang huyet ap": ["cao huyet ap", "huyet ap cao", "tang ha", "hypertension"],
    "tieu duong": ["dai thao duong", "glucose mau cao", "insulin", "diabetes"],
    "hen suyen": ["hen phe quan", "kho tho", "con hen", "asthma"],
    "suy than": ["benh than", "chuc nang than", "renal"],
    "suy gan": ["benh gan", "viem gan", "xo gan", "hepatic"],
    "paracetamol": ["acetaminophen", "tylenol", "efferalgan", "panadol"],
    "ibuprofen": ["nurofen", "advil", "brufen"],
    "aspirin": ["acid acetylsalicylic"],
    "omeprazole": ["losec", "esomeprazole"],
    "metformin": ["glucophage"],
    "amoxicillin": ["amoxil", "augmentin"],
}

INGREDIENT_FIELDS = [
    "active_ingredients",
    "main_ingredient",
    "hoat_chat",
    "ten_hoat_chat",
]
LOOKUP_ONLY_FIELDS = ["drug_name", "ten_thuoc", "brand_name"]
DOSAGE_PATTERN = re.compile(r"\d+\s*(mg|ml|mcg|g|iu|đvqt)", re.IGNORECASE)
PARENTHETICAL_PATTERN = re.compile(r"\([^)]*(?:\)|$)")
COMBO_SEPARATOR_PATTERN = re.compile(r"\s*(?:\+|/|;|,)\s*")
PACKAGING_WORDS = {"goi", "vien", "ong", "chai", "hop"}
CONTAINS_MARKERS = ("chua:", "chua ")
LOW_QUALITY_TERMS = {
    "va",
    "va/",
    "or",
    "and",
    "the",
    "cac",
    "cho",
    "de",
    "co",
    "moi",
    "chua",
    "dang",
    "vi",
    "nang",
    "microencapsulate",
}


class QueryExpander:
    """Expand queries with related drug and ingredient names from DAV data."""

    def __init__(self, dav_path: Optional[Union[str, Path]] = None) -> None:
        self.dav_path = Path(dav_path) if dav_path is not None else self._detect_dav_path()
        self.expansion_map: Dict[str, Set[str]] = {}
        self._loaded_count = 0
        records = self._load_records(self.dav_path)
        self._loaded_count = len(records)
        self.expansion_map = self._build_map(records)
        logger.info(
            "QueryExpander loaded %s records with %s expansion keys",
            self.loaded_count,
            self.map_size,
        )

    @property
    def loaded_count(self) -> int:
        return self._loaded_count

    @property
    def map_size(self) -> int:
        return len(self.expansion_map)

    def expand(self, query: str) -> List[str]:
        normalized_query = normalize_text(query or "")
        found: Set[str] = set()
        for term, expansions in self.expansion_map.items():
            if term in normalized_query:
                found.update(expansions)
        found = {
            term
            for term in found
            if term and term not in normalized_query and self._is_clean_expansion(term)
        }
        # Thêm medical synonyms tiếng Việt
        for key, synonyms in MEDICAL_SYNONYMS_VI.items():
            if key in normalized_query:
                found.update(s for s in synonyms if s not in normalized_query)
            else:
                for syn in synonyms:
                    if syn in normalized_query:
                        found.add(key)
                        found.update(s for s in synonyms if s != syn and s not in normalized_query)
                        break
        return sorted(found)[:12]

    def expand_query(self, query: str) -> str:
        expansions = self.expand(query)
        if not expansions:
            return query
        return query + " " + " ".join(expansions)

    def _detect_dav_path(self) -> Optional[Path]:
        current = Path(__file__).resolve()
        for parent in [current.parent, *current.parents[:4]]:
            candidate = parent / "data" / "processed" / "dav_all_drugs.jsonl"
            if candidate.exists():
                return candidate
        return None

    def _load_records(self, dav_path: Optional[Path]) -> List[Dict]:
        if dav_path is None or not dav_path.exists():
            logger.warning("DAV drug data file not found; query expansion disabled")
            return []

        records: List[Dict] = []
        try:
            with dav_path.open("r", encoding="utf-8") as handle:
                for line_number, line in enumerate(handle, 1):
                    try:
                        record = json.loads(line)
                    except Exception:
                        logger.warning("Skipping malformed DAV JSONL line %s", line_number)
                        continue
                    if isinstance(record, dict):
                        records.append(record)
        except Exception as exc:
            logger.warning("Could not load DAV drug data from %s: %s", dav_path, exc)
            return []
        return records

    def _build_map(self, records: List[Dict]) -> Dict[str, Set[str]]:
        ingredient_groups: List[Set[str]] = []
        lookup_links: List[tuple[Set[str], Set[str]]] = []
        for record in records:
            ingredient_group_candidates = self._ingredient_groups_from_record(record)
            if not ingredient_group_candidates:
                continue
            is_combo_record = len(ingredient_group_candidates) >= 2
            lookup_terms = (
                self._lookup_terms_from_record(record)
                if is_combo_record
                else self._terms_from_record(record, LOOKUP_ONLY_FIELDS, output_terms=False)
            )
            combo_terms: Set[str] = set()
            for ingredient_terms in ingredient_group_candidates:
                ingredient_groups.append(ingredient_terms)
                combo_terms.update(ingredient_terms)
            if is_combo_record:
                lookup_terms = {term for term in lookup_terms if term not in combo_terms}
            if lookup_terms:
                lookup_links.append((lookup_terms, combo_terms))

        merged_groups = self._merge_groups(ingredient_groups)
        term_group: Dict[str, Set[str]] = {}
        for group in merged_groups:
            for term in group:
                term_group[term] = group

        expansion_map: Dict[str, Set[str]] = {}
        for group in merged_groups:
            for variant in group:
                related = group - {variant}
                if not related:
                    continue
                expansion_map.setdefault(variant, set()).update(related)

        for lookup_terms, ingredient_terms in lookup_links:
            linked_group: Set[str] = set()
            for ingredient_term in ingredient_terms:
                linked_group.update(term_group.get(ingredient_term, ingredient_terms))
            for lookup_term in lookup_terms:
                expansion_map.setdefault(lookup_term, set()).update(linked_group)
        return expansion_map

    def _ingredient_groups_from_record(self, record: Dict) -> List[Set[str]]:
        groups: List[Set[str]] = []
        for value in self._raw_values_from_record(record, INGREDIENT_FIELDS):
            parts = self._split_combo_value(value)
            if self._is_combo_value(value, parts):
                for part in parts:
                    terms = self._terms_from_value(part, output_terms=True)
                    if terms:
                        groups.append(terms)
            else:
                terms = self._terms_from_value(value, output_terms=True)
                if terms:
                    groups.append(terms)
        return groups

    def _terms_from_record(self, record: Dict, fields: List[str], output_terms: bool) -> Set[str]:
        terms: Set[str] = set()
        for value in self._raw_values_from_record(record, fields):
            terms.update(self._terms_from_value(value, output_terms=output_terms))
        return terms

    def _lookup_terms_from_record(self, record: Dict) -> Set[str]:
        terms: Set[str] = set()
        for value in self._raw_values_from_record(record, LOOKUP_ONLY_FIELDS):
            normalized = normalize_text(value)
            cleaned = self._clean_term(normalized)
            for candidate in {normalized, cleaned}:
                if self._is_quality_term(candidate):
                    terms.add(candidate)
        return terms

    @staticmethod
    def _raw_values_from_record(record: Dict, fields: List[str]) -> List[str]:
        values: List[str] = []
        for field in fields:
            value = record.get(field)
            if isinstance(value, str):
                values.append(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        values.append(item)
        return values

    @classmethod
    def _terms_from_value(cls, value: str, output_terms: bool) -> Set[str]:
        terms: Set[str] = set()
        cls._add_terms(terms, value, output_terms=output_terms)
        return terms

    @classmethod
    def _is_combo_value(cls, value: str, parts: List[str]) -> bool:
        return bool(COMBO_SEPARATOR_PATTERN.search(value)) or len(parts) >= 2

    @classmethod
    def _split_combo_value(cls, value: str) -> List[str]:
        cleaned = normalize_text(value)
        return [
            cls._clean_term(part)
            for part in COMBO_SEPARATOR_PATTERN.split(cleaned)
            if cls._is_quality_term(cls._clean_term(part))
        ]

    @classmethod
    def _add_terms(cls, terms: Set[str], value: str, output_terms: bool) -> None:
        normalized = normalize_text(value)
        candidates = {normalized}
        candidates.update(cls._parenthetical_terms(normalized))
        cleaned = cls._clean_term(normalized)
        if cleaned:
            candidates.add(cleaned)
            candidates.update(cls._split_terms(cleaned))
        if not output_terms:
            extracted = cls._extract_lookup_term(normalized)
            if extracted:
                candidates.add(extracted)
                candidates.update(cls._split_terms(extracted))

        for candidate in candidates:
            if not cls._is_quality_term(candidate):
                continue
            if output_terms and not cls._is_clean_expansion(candidate):
                continue
            terms.add(candidate)

    @staticmethod
    def _is_quality_term(term: str) -> bool:
        normalized = (term or "").strip()
        words = normalized.split()
        return (
            len(normalized) >= 4
            and normalized not in LOW_QUALITY_TERMS
            and not LOW_QUALITY_TERMS.intersection(words)
            and len(words) <= 3
        )

    @staticmethod
    def _is_clean_expansion(term: str) -> bool:
        if len(term) > 40:
            return False
        if any(character.isdigit() for character in term):
            return False
        if term.isdigit():
            return False
        if DOSAGE_PATTERN.search(term):
            return False
        if any(character in term for character in ("(", ")", "%")):
            return False
        if any(separator in term for separator in ("/", ",", ";", ":")):
            return False
        if re.search(r"[^a-z\s-]", term):
            return False
        words = set(term.split())
        if PACKAGING_WORDS.intersection(words):
            return False
        return True

    @staticmethod
    def _clean_term(term: str) -> str:
        cleaned = PARENTHETICAL_PATTERN.sub("", term)
        cleaned = DOSAGE_PATTERN.sub("", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip(" .:-,;/")
        return cleaned

    @classmethod
    def _parenthetical_terms(cls, term: str) -> Set[str]:
        matches = re.findall(r"\(([^)]*)\)", term)
        return {cls._clean_term(match) for match in matches if cls._clean_term(match)}

    @classmethod
    def _split_terms(cls, term: str) -> Set[str]:
        parts = re.split(r"\s*(?:/|,|;|\+|\bva\b|\band\b)\s*", term)
        return {cls._clean_term(part) for part in parts if cls._clean_term(part)}

    @classmethod
    def _extract_lookup_term(cls, term: str) -> str:
        for marker in CONTAINS_MARKERS:
            if marker in term:
                return cls._clean_term(term.split(marker, 1)[1])
        return ""

    @staticmethod
    def _merge_groups(groups: List[Set[str]]) -> List[Set[str]]:
        parent = list(range(len(groups)))

        def find(index: int) -> int:
            while parent[index] != index:
                parent[index] = parent[parent[index]]
                index = parent[index]
            return index

        def union(left: int, right: int) -> None:
            left_root = find(left)
            right_root = find(right)
            if left_root != right_root:
                parent[right_root] = left_root

        term_owner: Dict[str, int] = {}
        for index, group in enumerate(groups):
            for term in group:
                owner = term_owner.get(term)
                if owner is None:
                    term_owner[term] = index
                else:
                    union(index, owner)

        root_groups: Dict[int, Set[str]] = {}
        for index, group in enumerate(groups):
            root = find(index)
            root_groups.setdefault(root, set()).update(group)
        return list(root_groups.values())
