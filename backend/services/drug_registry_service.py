"""File-backed drug registry and interaction services.

The current project already keeps DAV registry exports and DDInter edges as
JSONL files. These helpers make the `/drug/*` endpoints useful without adding
a database dependency.
"""
from __future__ import annotations

import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from backend.models import Citation, InteractionSeverity
from backend.services.graph_safety_service import GraphSafetyService


ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY_PATHS = (
    ROOT_DIR / "data" / "processed" / "dav_otc_drugs.jsonl",
    ROOT_DIR / "data" / "processed" / "dav_all_drugs.jsonl",
)


def normalize_text(text: str) -> str:
    value = (text or "").replace("Đ", "D").replace("đ", "d").lower()
    decomposed = unicodedata.normalize("NFD", value)
    stripped = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", stripped).strip()


def token_set(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", normalize_text(text)))


def iter_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def public_drug_id(row: Dict[str, Any]) -> str:
    return str(row.get("registration_number") or row.get("dav_id") or row.get("drug_name") or "")


def source_url_for(row: Dict[str, Any]) -> str:
    return str(row.get("source_url") or "")


def citation_for(row: Dict[str, Any], index: int = 1, section: str = "drug_registry") -> Citation:
    return Citation(
        id=f"S{index}",
        source=str(row.get("source_dataset") or "dav_registry"),
        title=str(row.get("drug_name") or row.get("registration_number") or "DAV registry"),
        url=source_url_for(row) or None,
        section=section,
        updated_at=str(row.get("registration_date") or "") or None,
    )


def serialize_registry_row(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "drug_id": public_drug_id(row),
        "dav_id": row.get("dav_id"),
        "name": row.get("drug_name"),
        "registration_number": row.get("registration_number"),
        "active_ingredient": row.get("active_ingredient"),
        "strength": row.get("strength"),
        "dosage_form": row.get("dosage_form"),
        "packaging": row.get("packaging"),
        "route": row.get("route"),
        "manufacturer_name": row.get("manufacturer_name"),
        "manufacturer_country": row.get("manufacturer_country"),
        "registrant_name": row.get("registrant_name"),
        "registration_date": row.get("registration_date"),
        "expiry_date": row.get("expiry_date"),
        "is_revoked": row.get("is_revoked"),
        "source": row.get("source_dataset"),
        "source_url": row.get("source_url"),
        "citation": citation_for(row).model_dump(),
    }


def score_row(row: Dict[str, Any], query: str) -> float:
    query_norm = normalize_text(query)
    query_tokens = token_set(query)
    if not query_norm or not query_tokens:
        return 0.0

    fields = {
        "drug_name": 4.0,
        "registration_number": 4.0,
        "active_ingredient": 3.0,
        "manufacturer_name": 1.0,
        "registrant_name": 0.5,
    }
    score = 0.0
    for field, weight in fields.items():
        value = normalize_text(str(row.get(field) or ""))
        if not value:
            continue
        if query_norm == value:
            score += weight * 3
        elif query_norm in value:
            score += weight * 2
        overlap = len(query_tokens & token_set(value))
        if overlap:
            score += weight * overlap / max(len(query_tokens), 1)
    if row.get("source_dataset") == "dav_otc":
        score += 0.1
    return score


def severity_to_model(value: str) -> InteractionSeverity:
    normalized = normalize_text(value)
    if normalized in {"critical"}:
        return InteractionSeverity.CRITICAL
    if normalized in {"major", "high"}:
        return InteractionSeverity.HIGH
    if normalized in {"moderate", "caution"}:
        return InteractionSeverity.MODERATE
    if normalized in {"minor", "low"}:
        return InteractionSeverity.LOW
    return InteractionSeverity.NONE


class DrugRegistryService:
    def __init__(self, registry_paths: tuple[Path, ...] = DEFAULT_REGISTRY_PATHS) -> None:
        self.registry_paths = registry_paths
        self.graph_safety = GraphSafetyService()

    @lru_cache(maxsize=1)
    def rows(self) -> tuple[Dict[str, Any], ...]:
        seen: set[tuple[str, str]] = set()
        rows: List[Dict[str, Any]] = []
        for path in self.registry_paths:
            for row in iter_jsonl(path):
                key = (
                    str(row.get("source_dataset") or ""),
                    str(row.get("registration_number") or row.get("dav_id") or row.get("drug_name") or ""),
                )
                if key in seen:
                    continue
                seen.add(key)
                rows.append(row)
        return tuple(rows)

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        scored = [(score_row(row, query), row) for row in self.rows()]
        matches = [item for item in scored if item[0] > 0]
        matches.sort(key=lambda item: item[0], reverse=True)
        return [
            {
                **serialize_registry_row(row),
                "score": round(score, 4),
            }
            for score, row in matches[:limit]
        ]

    def get(self, drug_id: str) -> Optional[Dict[str, Any]]:
        target = normalize_text(drug_id)
        for row in self.rows():
            candidates = {
                normalize_text(str(row.get("registration_number") or "")),
                normalize_text(str(row.get("dav_id") or "")),
                normalize_text(str(row.get("drug_name") or "")),
            }
            if target in candidates:
                return serialize_registry_row(row)
        matches = self.search(drug_id, limit=1)
        return matches[0] if matches else None

    def check_interactions(self, drugs: List[str]) -> Dict[str, Any]:
        findings = self.graph_safety.check_interactions(drugs)
        highest = self.graph_safety.highest_risk(findings)
        severity = severity_to_model(highest)
        citations = []
        for index, finding in enumerate(findings, 1):
            citations.append(
                Citation(
                    id=f"S{index}",
                    source=str(finding.get("source") or "ddinter"),
                    title=f"{finding.get('drug_a')} - {finding.get('drug_b')}",
                    url=finding.get("source_url"),
                    section="drug_drug_interaction",
                ).model_dump()
            )
        return {
            "has_interactions": bool(findings),
            "severity": severity.value,
            "highest_risk": highest,
            "detected_drugs": drugs,
            "interactions": findings,
            "total_interactions": len(findings),
            "sources": citations,
            "warnings": (
                ["Không tự phối hợp thuốc khi có cảnh báo tương tác; hãy hỏi bác sĩ/dược sĩ."]
                if findings
                else []
            ),
        }

    def dosage_lookup(self, drug_name: str) -> Dict[str, Any]:
        matches = self.search(drug_name, limit=3)
        sources = [row["citation"] for row in matches]
        return {
            "drug_name": drug_name,
            "recommended_dosage": (
                "Không tự tính hoặc tự đổi liều từ endpoint này. "
                "Chỉ dùng kết quả để đối chiếu tên thuốc/hoạt chất và hỏi bác sĩ/dược sĩ."
            ),
            "frequency": None,
            "warnings": [
                "Thiếu protocol liều dùng đã kiểm chứng theo tuổi, cân nặng, bệnh nền và toa thuốc.",
                "Nếu đây là thuốc kê đơn, dùng đúng toa và không tự điều chỉnh liều.",
            ],
            "sources": sources,
            "matched_drugs": matches,
        }


_drug_registry_service: Optional[DrugRegistryService] = None


def get_drug_registry_service() -> DrugRegistryService:
    global _drug_registry_service
    if _drug_registry_service is None:
        _drug_registry_service = DrugRegistryService()
    return _drug_registry_service
