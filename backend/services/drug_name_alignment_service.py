"""Deterministic drug name alignment before graph/RAG lookup.

People often ask with brand names, misspellings, hyphenated names, or colloquial
Vietnamese spellings. This service maps those mentions to canonical drug names
or active ingredients before graph safety and retrieval run.
"""
from __future__ import annotations

import csv
import json
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DAV_OTC = ROOT_DIR / "data" / "processed" / "dav_otc_drugs.csv"
DEFAULT_DAV_ALL = ROOT_DIR / "data" / "processed" / "dav_all_drugs.csv"
DEFAULT_DUOCTHU = ROOT_DIR / "data" / "processed" / "trungtamthuoc_duocthu_monographs.jsonl"


MANUAL_ALIASES = {
    "pa na don": ("Panadol", "paracetamol", "manual_alias"),
    "panadol": ("Panadol", "paracetamol", "manual_alias"),
    "hapacol": ("Hapacol", "paracetamol", "manual_alias"),
    "efferalgan": ("Efferalgan", "paracetamol", "manual_alias"),
    "tylenol": ("Tylenol", "paracetamol", "manual_alias"),
    "para": ("Paracetamol", "paracetamol", "manual_alias"),
    "paracetamol": ("Paracetamol", "paracetamol", "manual_alias"),
    "acetaminophen": ("Acetaminophen", "paracetamol", "manual_alias"),
    "li pi to": ("Lipitor", "atorvastatin", "manual_alias"),
    "lipito": ("Lipitor", "atorvastatin", "manual_alias"),
    "lipitor": ("Lipitor", "atorvastatin", "manual_alias"),
    "thuoc mo mau lipitor": ("Lipitor", "atorvastatin", "manual_alias"),
    "aspirin": ("Aspirin", "acetylsalicylic acid", "manual_alias"),
    "asa": ("Aspirin", "acetylsalicylic acid", "manual_alias"),
    "warfarin": ("Warfarin", "warfarin", "manual_alias"),
    "clarithromycin": ("Clarithromycin", "clarithromycin", "manual_alias"),
}


STOPWORDS = {
    "thuoc",
    "uong",
    "dung",
    "voi",
    "cung",
    "them",
    "mua",
    "ban",
    "cho",
    "toi",
    "tui",
    "minh",
    "con",
    "be",
    "bi",
    "nguoi",
    "benh",
    "tieu",
    "dai",
    "thao",
    "duong",
    "sot",
    "ho",
    "cam",
    "dau",
    "co",
    "gio",
    "muon",
    "thi",
    "nen",
    "khong",
    "tranh",
    "loai",
    "nao",
}


def normalize_name(value: str) -> str:
    text = (value or "").replace("Đ", "D").replace("đ", "d").lower()
    decomposed = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def compact_name(value: str) -> str:
    return normalize_name(value).replace(" ", "")


def _clean_active_ingredient(value: str) -> str:
    text = re.sub(r"\([^)]*\)", "", value or "")
    text = re.split(r"[;,/+]", text)[0]
    text = re.sub(r"\b(bp|usp|ep|jp)\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    normalized = normalize_name(text)
    if not re.search(r"[a-z]", normalized) or re.fullmatch(r"[\d\s.,]*(mg|mcg|g|ml|iu|%)?", normalized):
        return ""
    return text


def _ngrams(tokens: List[str], min_n: int = 1, max_n: int = 4) -> Iterable[str]:
    for n in range(max_n, min_n - 1, -1):
        for index in range(0, len(tokens) - n + 1):
            gram = " ".join(tokens[index : index + n])
            if gram and gram not in STOPWORDS:
                yield gram


class DrugNameAlignmentService:
    """Builds a small canonical lexicon and aligns noisy user mentions."""

    def __init__(
        self,
        dav_otc_path: Path = DEFAULT_DAV_OTC,
        dav_all_path: Path = DEFAULT_DAV_ALL,
        duocthu_path: Path = DEFAULT_DUOCTHU,
        max_dav_rows: int = 80000,
    ) -> None:
        self.dav_otc_path = dav_otc_path
        self.dav_all_path = dav_all_path
        self.duocthu_path = duocthu_path
        self.max_dav_rows = max_dav_rows
        self._lexicon: Dict[str, Dict[str, Any]] | None = None
        self._compact_index: Dict[str, str] | None = None
        self._fuzzy_buckets: Dict[str, List[str]] | None = None

    def align(self, query: str, max_matches: int = 5) -> Dict[str, Any]:
        lexicon = self._load_lexicon()
        compact_index = self._compact_index or {}
        normalized_query = normalize_name(query)
        compact_query = compact_name(query)
        tokens = [token for token in normalized_query.split() if token not in STOPWORDS]

        matches: List[Dict[str, Any]] = []
        seen_keys = set()

        for alias, (display, canonical, source) in MANUAL_ALIASES.items():
            alias_norm = normalize_name(alias)
            alias_compact = compact_name(alias)
            if alias_norm in normalized_query or alias_compact in compact_query:
                key = (display, canonical, source)
                if key not in seen_keys:
                    seen_keys.add(key)
                    matches.append(
                        {
                            "mention": alias,
                            "matched_name": display,
                            "canonical_name": canonical,
                            "match_type": source,
                            "score": 1.0,
                        }
                    )

        for term in _ngrams(tokens):
            term_compact = compact_name(term)
            if term in lexicon:
                self._append_match(matches, seen_keys, term, lexicon[term], 0.98, "exact_lexicon")
            elif term_compact in compact_index:
                key = compact_index[term_compact]
                self._append_match(matches, seen_keys, term, lexicon[key], 0.95, "compact_exact")

        if len(matches) < max_matches:
            matched_mentions = {normalize_name(row["mention"]) for row in matches}
            fuzzy = self._fuzzy_candidates(tokens, lexicon)
            for term, key, score in fuzzy:
                if normalize_name(term) in matched_mentions:
                    continue
                self._append_match(matches, seen_keys, term, lexicon[key], score, "fuzzy_lexicon")
                if len(matches) >= max_matches:
                    break

        matches = sorted(matches, key=lambda row: row["score"], reverse=True)[:max_matches]
        canonical_terms = list(dict.fromkeys(row["canonical_name"] for row in matches if row.get("canonical_name")))
        augmented_query = query
        if canonical_terms:
            augmented_query = query + "\nAligned drug entities: " + "; ".join(canonical_terms)

        return {
            "query": query,
            "augmented_query": augmented_query,
            "matches": matches,
            "canonical_terms": canonical_terms,
            "used": bool(matches),
        }

    def _append_match(
        self,
        matches: List[Dict[str, Any]],
        seen_keys: set,
        mention: str,
        entry: Dict[str, Any],
        score: float,
        match_type: str,
    ) -> None:
        key = (entry["normalized_name"], entry.get("canonical_name"))
        if key in seen_keys:
            return
        seen_keys.add(key)
        matches.append(
            {
                "mention": mention,
                "matched_name": entry["display_name"],
                "canonical_name": entry.get("canonical_name") or entry["display_name"],
                "match_type": match_type,
                "source": entry.get("source"),
                "score": round(score, 4),
            }
        )

    def _fuzzy_candidates(
        self,
        tokens: List[str],
        lexicon: Dict[str, Dict[str, Any]],
    ) -> List[Tuple[str, str, float]]:
        candidates = []
        fuzzy_buckets = self._fuzzy_buckets or {}
        for term in _ngrams(tokens, min_n=1, max_n=3):
            term_compact = compact_name(term)
            if len(term_compact) < 6:
                continue
            for key in fuzzy_buckets.get(term_compact[0], []):
                entry = lexicon[key]
                name_compact = entry["compact_name"]
                if abs(len(term_compact) - len(name_compact)) > 4:
                    continue
                score = SequenceMatcher(None, term_compact, name_compact).ratio()
                if score >= 0.88:
                    candidates.append((term, key, score))
        candidates.sort(key=lambda item: item[2], reverse=True)
        return candidates[:20]

    def _load_lexicon(self) -> Dict[str, Dict[str, Any]]:
        if self._lexicon is not None:
            return self._lexicon
        lexicon: Dict[str, Dict[str, Any]] = {}
        for path in (self.dav_otc_path, self.dav_all_path):
            self._load_dav_csv(path, lexicon)
        self._load_duocthu_titles(self.duocthu_path, lexicon)
        for alias, (display, canonical, source) in MANUAL_ALIASES.items():
            self._add_entry(lexicon, display, canonical, source)
        self._lexicon = lexicon
        self._compact_index = {compact_name(key): key for key in lexicon}
        fuzzy_buckets: Dict[str, List[str]] = {}
        for key, entry in lexicon.items():
            compact = entry["compact_name"]
            if 5 <= len(compact) <= 28:
                fuzzy_buckets.setdefault(compact[0], []).append(key)
        self._fuzzy_buckets = fuzzy_buckets
        return lexicon

    def _load_dav_csv(self, path: Path, lexicon: Dict[str, Dict[str, Any]]) -> None:
        if not path.exists():
            return
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for index, row in enumerate(reader):
                if index >= self.max_dav_rows:
                    break
                drug_name = row.get("drug_name") or ""
                active = _clean_active_ingredient(row.get("active_ingredient") or "")
                if drug_name:
                    self._add_entry(lexicon, drug_name, active or drug_name, row.get("source_dataset") or "dav")
                if active:
                    self._add_entry(lexicon, active, active, row.get("source_dataset") or "dav")

    def _load_duocthu_titles(self, path: Path, lexicon: Dict[str, Dict[str, Any]]) -> None:
        if not path.exists():
            return
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                row = json.loads(line)
                title = row.get("title") or ""
                if title and len(title) <= 80:
                    self._add_entry(lexicon, title, title, row.get("source") or "duocthu")

    def _add_entry(
        self,
        lexicon: Dict[str, Dict[str, Any]],
        display_name: str,
        canonical_name: str,
        source: str,
    ) -> None:
        normalized = normalize_name(display_name)
        if not normalized or len(normalized) < 3 or normalized in STOPWORDS:
            return
        existing = lexicon.get(normalized)
        if existing and existing.get("source") == "dav_otc":
            return
        lexicon[normalized] = {
            "display_name": display_name,
            "normalized_name": normalized,
            "compact_name": compact_name(display_name),
            "canonical_name": canonical_name or display_name,
            "source": source,
        }
