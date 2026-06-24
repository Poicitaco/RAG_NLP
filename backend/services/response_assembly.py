"""Cac ham tro giup tong hop response cho Safe RAG pipeline.

Chua: citation builder, agent trace, response block helpers,
patient context augmentation. Duoc tach ra tu safe_rag_service.py.
"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from backend.models import Citation
from backend.services.final_response_builder import build_response_blocks, format_response_blocks


# ---------------------------------------------------------------------------
# Citation helpers
# ---------------------------------------------------------------------------

def xay_citation_tu_row(chi_so: int, row: Dict[str, Any]) -> Citation:
    """Tao Citation tu 1 row ket qua retrieval."""
    metadata = row.get("metadata") or {}
    tieu_de = (
        metadata.get("title")
        or metadata.get("drug_name")
        or (row.get("document_preview") or row.get("document") or "")[:60].strip()
        or None
    )
    nguon = str(metadata.get("source") or metadata.get("source_dataset") or row.get("source") or "unknown")
    return Citation(
        id=f"S{chi_so}",
        source=nguon,
        title=tieu_de,
        url=metadata.get("source_url") or metadata.get("url"),
        page=metadata.get("page"),
        section=metadata.get("section") or metadata.get("type"),
        similarity=row.get("hybrid_score"),
    )


def xay_citations_tu_graph_findings(findings: List[Dict[str, Any]]) -> List[Citation]:
    """Chuyen ket qua graph safety findings thanh danh sach Citation."""
    citations: List[Citation] = []
    for finding in findings:
        if finding.get("source") or finding.get("source_url"):
            if finding.get("type") == "drug_drug_interaction":
                tieu_de = f"{finding.get('drug_a') or 'Drug A'} - {finding.get('drug_b') or 'Drug B'}"
            else:
                tieu_de = finding.get("condition") or finding.get("otc_category") or finding.get("type")
            citations.append(
                Citation(
                    id=f"S{len(citations) + 1}",
                    source=finding.get("source") or "graph_safety",
                    title=tieu_de,
                    url=finding.get("source_url"),
                    section=finding.get("otc_category") or finding.get("type"),
                )
            )
        for source in finding.get("citations") or []:
            if not isinstance(source, dict):
                continue
            citations.append(
                Citation(
                    id=f"S{len(citations) + 1}",
                    source=finding.get("source") or "graph_safety",
                    title=source.get("title") or finding.get("condition") or finding.get("type"),
                    url=source.get("url") or finding.get("source_url"),
                    section=finding.get("otc_category") or finding.get("type"),
                )
            )
    return citations


def citation_an_toan_mac_dinh(action: str = "", subtype: str = "") -> List[Citation]:
    """Tra ve citation mac dinh cho truong hop emergency/clarification/handoff."""
    citations = [
        Citation(
            id="S1",
            source="system_safety_policy",
            title="Clinical safety policy: triage and patient-context guardrails",
            url="docs/PIPELINE.md",
            section=subtype or action or "medication_safety_guardrail",
        )
    ]
    if action == "needs_clarification":
        citations.append(
            Citation(
                id="S2",
                source="patient_context_collector",
                title="Patient context requirement before medication advice",
                url="docs/PIPELINE.md",
                section="missing_patient_context",
            )
        )
    return citations


def danh_so_lai_citations(citations: List[Citation]) -> List[Citation]:
    """Loai bo trung lap va danh so lai citations tu S1."""
    unique: List[Citation] = []
    da_thay = set()
    for citation in citations:
        khoa = (citation.source, citation.title, citation.url, citation.section)
        if khoa in da_thay:
            continue
        da_thay.add(khoa)
        unique.append(citation)
    for idx, citation in enumerate(unique, 1):
        citation.id = f"S{idx}"
    return unique


def citations_thanh_dict(citations: List[Citation]) -> List[Dict[str, Any]]:
    return [citation.model_dump() for citation in citations]


# ---------------------------------------------------------------------------
# Response block helpers
# ---------------------------------------------------------------------------

def them_citation_block_vao_response(
    response_blocks: Dict[str, Any],
    citations: List[Citation],
) -> Dict[str, Any]:
    """Gan danh sach citations vao block citations cua response."""
    blocks = response_blocks.setdefault("blocks", {})
    citation_block = blocks.setdefault(
        "citations",
        {"title": "**DẪN NGUỒN ĐỐI SOÁT**", "items": [], "sources": []},
    )
    citation_block["sources"] = [citation.model_dump() for citation in citations]
    citation_block["items"] = [
        f"[{citation.id}] {citation.title or citation.source} - nguồn: {citation.source}"
        + (f", mục: {citation.section}" if citation.section else "")
        + "."
        for citation in citations
    ]
    return response_blocks


def tao_response_blocks_lam_ro(
    *,
    intent: str,
    questions: List[str],
    selected_agents: List[str],
    reason: str,
) -> Dict[str, Any]:
    """Tao response blocks cho truong hop bot can hoi them thong tin."""
    return {
        "schema_version": "agent_response_v1",
        "render_order": ["safety_guardrail", "core_action", "clinical_reason", "citations"],
        "selected_agents": selected_agents,
        "blocks": {
            "safety_guardrail": {
                "title": "**Lưu ý an toàn**",
                "level": "caution",
                "items": [
                    "Mình cần xác nhận thêm thông tin an toàn trước khi gợi ý thuốc hoặc cách dùng cụ thể.",
                ],
            },
            "core_action": {
                "title": "**Hướng dẫn nhanh**",
                "items": questions,
            },
            "clinical_reason": {
                "title": "**Giải thích thêm**",
                "items": [
                    "Tuổi, cân nặng, bệnh nền, dị ứng và thuốc đang dùng có thể làm thay đổi lựa chọn thuốc, liều dùng hoặc nguy cơ tương tác.",
                    "Mình hỏi lại để tránh tư vấn sai thuốc nếu thiếu thông tin y tế của bạn.",
                ],
            },
            "citations": {
                "title": "**Nguồn tham khảo**",
                "items": ["Chưa truy xuất nguồn vì cần bạn xác nhận thông tin an toàn trước."],
                "sources": [],
            },
        },
    }


# ---------------------------------------------------------------------------
# Patient context augmentation
# ---------------------------------------------------------------------------

def bo_sung_patient_context_vao_tin_nhan(message: str, patient_context: Dict[str, Any]) -> str:
    """Noi them thong tin benh nhan vao cuoi tin nhan de RAG retrieval chinh xac hon."""
    context_terms = []
    age = patient_context.get("age")
    age_months = patient_context.get("age_months")
    weight = patient_context.get("weight_kg")
    conditions = patient_context.get("conditions") or []
    current_medications = patient_context.get("current_medications") or []
    allergies = patient_context.get("allergies") or []

    if age is not None:
        context_terms.append(f"age: {age}")
    if age_months is not None:
        context_terms.append(f"age_months: {age_months}")
    if weight is not None:
        context_terms.append(f"weight_kg: {weight}")
    if conditions:
        context_terms.append("conditions: " + "; ".join(str(item) for item in conditions))
    if current_medications:
        context_terms.append("current_medications: " + "; ".join(str(item) for item in current_medications))
    if allergies:
        context_terms.append("allergies: " + "; ".join(str(item) for item in allergies))
    if patient_context.get("pregnant") is True:
        context_terms.append("pregnant: true")
    if patient_context.get("breastfeeding") is True:
        context_terms.append("breastfeeding: true")

    if not context_terms:
        return message
    return message + "\nPatient context: " + "; ".join(context_terms)


# ---------------------------------------------------------------------------
# Agent trace helpers
# ---------------------------------------------------------------------------

def them_buoc_trace(
    trace: List[Dict[str, Any]],
    node: str,
    status: str = "completed",
    details: Optional[Dict[str, Any]] = None,
    started_at: Optional[float] = None,
) -> None:
    """Ghi mot buoc xu ly vao danh sach trace de debug."""
    buoc = {
        "node": node,
        "status": status,
        "details": details or {},
    }
    if started_at is not None:
        buoc["duration_ms"] = round((time.perf_counter() - started_at) * 1000, 2)
    trace.append(buoc)


def tao_agent_pipeline(
    trace: List[Dict[str, Any]],
    graph_overrode_rag: bool = False,
) -> Dict[str, Any]:
    return {
        "name": "safe_rag_agent_pipeline_v1",
        "execution_mode": "graph_first_hybrid_rag_with_evidence_join",
        "graph_overrode_rag": graph_overrode_rag,
        "trace": trace,
    }


def lay_diem_reranker_tu_trace(trace: List[Dict[str, Any]]) -> Optional[float]:
    for step in trace:
        if step.get("node") == "reranker_agent":
            return step.get("details", {}).get("top_score")
    return None


def chon_agents(
    intent: str,
    graph_result: Dict[str, Any],
    alignment: Optional[Dict[str, Any]] = None,
) -> List[str]:
    """Chon danh sach agents dua tren intent va graph result."""
    agents = ["triage_risk_agent", "retrieval_agent", "final_response_builder"]
    if alignment and alignment.get("used"):
        agents.insert(1, "drug_name_alignment_agent")
    if graph_result.get("should_warn"):
        agents.insert(1, "graph_safety_agent")
    if intent == "otc_recommendation":
        agents.insert(1, "otc_recommendation_agent")
    elif intent == "dosage":
        agents.insert(1, "dosage_agent")
    elif intent == "interaction":
        agents.insert(1, "interaction_agent")
    elif intent == "pediatric_symptom":
        agents.insert(1, "pediatric_safety_agent")
    elif intent in {"high_risk_context", "emergency"}:
        agents.insert(1, "safety_monitor_agent")
    return list(dict.fromkeys(agents))
