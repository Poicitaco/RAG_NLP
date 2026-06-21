"""Safe RAG service used by the chat API.

The service retrieves evidence, applies evidence and graph guardrails, then
returns a citation-backed answer. An LLM can optionally rewrite that approved
answer, but it is never used as the source of medical truth.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from backend.models import AgentType, ChatResponse, Citation
from backend.safety.evidence_guardrails import (
    EvidenceAction,
    evaluate_evidence,
    is_unverified_ocr,
    mentioned_common_drugs,
    normalize_text,
)
from backend.services.final_response_builder import build_response_blocks, format_response_blocks
from backend.services.graph_safety_service import GraphSafetyService, format_graph_warning
from backend.services.llm_answer_service import LLMAnswerService
from backend.services.drug_name_alignment_service import DrugNameAlignmentService
from backend.utils import format_medical_disclaimer


ROOT_DIR = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = ROOT_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from hybrid_search_rag import chroma_search, combine_results, load_bm25_index  # noqa: E402
from smoke_search_bm25 import search as bm25_search  # noqa: E402


DEFAULT_BM25_INDEX = ROOT_DIR / "data" / "embeddings" / "bm25" / "rag_bm25.pkl.gz"
DEFAULT_CHROMA_DIR = ROOT_DIR / "data" / "embeddings" / "chroma_priority"
DEFAULT_COLLECTION = "pharmaceutical_priority"
DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

SOURCE_PRIORITY = {
    "dav_recall": 0,
    "canhgiacduoc": 1,
    "dav_all": 2,
    "dav_otc": 2,
    "trungtamthuoc_duocthu": 3,
    "ddinter": 2,
    "otc_condition_guardrail": 0,
    "dav_pdf": 3,
    "dav_pdf_ocr": 5,
}


def _metadata(row: Dict[str, Any]) -> Dict[str, Any]:
    return row.get("metadata") or {}


def _source(row: Dict[str, Any]) -> str:
    metadata = _metadata(row)
    return str(metadata.get("source") or metadata.get("source_dataset") or row.get("source") or "")


def _row_text(row: Dict[str, Any]) -> str:
    metadata = _metadata(row)
    values = [
        row.get("document_preview"),
        row.get("document"),
        metadata.get("title"),
        metadata.get("drug_name"),
        metadata.get("active_ingredients"),
        metadata.get("main_ingredient"),
    ]
    return normalize_text(" ".join(str(value) for value in values if value))


def _rank_for_answer(question: str, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    question_drugs = mentioned_common_drugs(question)

    def key(row: Dict[str, Any]) -> tuple:
        text = _row_text(row)
        drug_match = 0 if not question_drugs or any(term in text for term in question_drugs) else 1
        ocr_penalty = 1 if is_unverified_ocr(row) else 0
        return (
            drug_match,
            ocr_penalty,
            SOURCE_PRIORITY.get(_source(row), 4),
            row.get("rank") or 999,
        )

    return sorted(results, key=key)


def _select_answer_rows(graph_result: Dict[str, Any], ranked: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    findings = graph_result.get("findings") or []
    if not findings:
        return ranked

    preferred_sources = set()
    preferred_types = set()
    exact_interaction_pairs = []
    for finding in findings:
        if finding.get("type") == "condition_otc_caution":
            preferred_sources.add("otc_condition_guardrail")
            preferred_types.add("condition_guardrail")
        elif finding.get("type") == "drug_drug_interaction":
            preferred_sources.add("ddinter")
            preferred_types.add("interaction")
            left = normalize_text(str(finding.get("drug_a") or ""))
            right = normalize_text(str(finding.get("drug_b") or ""))
            if left and right:
                exact_interaction_pairs.append((left, right))

    exact_rows = []
    for row in ranked:
        if _source(row) != "ddinter":
            continue
        text = _row_text(row)
        for left, right in exact_interaction_pairs:
            if left in text and right in text:
                exact_rows.append(row)
                break
    if exact_rows:
        return exact_rows

    selected = [
        row
        for row in ranked
        if _source(row) in preferred_sources or str(_metadata(row).get("type") or "") in preferred_types
    ]
    return selected or ranked


def _citation_from_row(index: int, row: Dict[str, Any]) -> Citation:
    metadata = _metadata(row)
    return Citation(
        id=f"S{index}",
        source=_source(row) or "unknown",
        title=metadata.get("title") or metadata.get("drug_name"),
        url=metadata.get("source_url") or metadata.get("url"),
        page=metadata.get("page"),
        section=metadata.get("section") or metadata.get("type"),
        similarity=row.get("hybrid_score"),
    )


def _preview(row: Dict[str, Any], max_len: int = 280) -> str:
    text = (row.get("document_preview") or row.get("document") or "").strip()
    if len(text) > max_len:
        return text[:max_len].rstrip() + "..."
    return text


def _selected_agents(
    intent: str,
    graph_result: Dict[str, Any],
    alignment: Optional[Dict[str, Any]] = None,
) -> List[str]:
    agents = ["triage_risk_agent", "retrieval_agent", "final_response_builder"]
    if alignment and alignment.get("used"):
        agents.insert(1, "drug_name_alignment_agent")
    if graph_result.get("should_warn"):
        agents.insert(1, "graph_safety_agent")
    if intent == "dosage":
        agents.insert(1, "dosage_agent")
    elif intent == "interaction":
        agents.insert(1, "interaction_agent")
    elif intent == "pediatric_symptom":
        agents.insert(1, "pediatric_safety_agent")
    elif intent in {"high_risk_context", "emergency"}:
        agents.insert(1, "safety_monitor_agent")
    return list(dict.fromkeys(agents))


def _add_trace_step(
    trace: List[Dict[str, Any]],
    node: str,
    status: str = "completed",
    details: Optional[Dict[str, Any]] = None,
    started_at: Optional[float] = None,
) -> None:
    step = {
        "node": node,
        "status": status,
        "details": details or {},
    }
    if started_at is not None:
        step["duration_ms"] = round((time.perf_counter() - started_at) * 1000, 2)
    trace.append(step)


def _agent_pipeline(
    trace: List[Dict[str, Any]],
    graph_overrode_rag: bool = False,
) -> Dict[str, Any]:
    return {
        "name": "safe_rag_agent_pipeline_v1",
        "execution_mode": "graph_first_hybrid_rag_with_evidence_join",
        "graph_overrode_rag": graph_overrode_rag,
        "trace": trace,
    }


class SafeRagService:
    """Hybrid retrieval + evidence guardrail + deterministic answer builder."""

    def __init__(
        self,
        bm25_index_path: Path = DEFAULT_BM25_INDEX,
        chroma_dir: Path = DEFAULT_CHROMA_DIR,
        collection: str = DEFAULT_COLLECTION,
        model: str = DEFAULT_MODEL,
    ) -> None:
        self.bm25_index_path = bm25_index_path
        self.chroma_dir = chroma_dir
        self.collection = collection
        self.model = model
        self._bm25_index: Optional[Dict[str, Any]] = None
        self.graph_safety = GraphSafetyService()
        self.llm_answer = LLMAnswerService()
        self.name_alignment = DrugNameAlignmentService()

    def _load_bm25(self) -> Dict[str, Any]:
        if self._bm25_index is None:
            self._bm25_index = load_bm25_index(self.bm25_index_path)
        return self._bm25_index

    def retrieve(self, question: str, top_k: int = 5) -> List[Dict[str, Any]]:
        bm25_results = bm25_search(self._load_bm25(), question, top_k=500)
        chroma_results = chroma_search(
            question,
            str(self.chroma_dir),
            self.collection,
            "sentence-transformers",
            self.model,
            top_k=10,
        )
        return combine_results(
            question,
            bm25_results,
            chroma_results,
            bm25_weight=0.65,
            vector_weight=0.35,
            top_k=top_k,
        )

    async def answer(
        self,
        message: str,
        session_id: str,
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> ChatResponse:
        conversation = conversation_id or session_id
        trace: List[Dict[str, Any]] = []
        started_at = time.perf_counter()
        early_decision = evaluate_evidence(message, [])
        _add_trace_step(
            trace,
            "safety_router",
            details={
                "action": early_decision.action.value,
                "intent": early_decision.intent.value,
                "should_answer": early_decision.should_answer,
            },
            started_at=started_at,
        )
        if early_decision.action == EvidenceAction.EMERGENCY:
            selected_agents = _selected_agents(early_decision.intent.value, {})
            response_blocks = build_response_blocks(
                action=early_decision.action.value,
                intent=early_decision.intent.value,
                graph_result={},
                citations=[],
                selected_agents=selected_agents,
            )
            _add_trace_step(
                trace,
                "emergency_bypass",
                details={"retrieval_bypassed": True, "selected_agents": selected_agents},
            )
            return ChatResponse(
                message=format_response_blocks(response_blocks),
                conversation_id=conversation,
                agent_type=AgentType.SAFETY_MONITOR,
                confidence=1.0,
                warnings=early_decision.warnings,
                suggestions=["Gọi 115 hoặc đến cơ sở y tế gần nhất ngay."],
                metadata={
                    "rag_action": early_decision.action.value,
                    "intent": early_decision.intent.value,
                    "retrieval_bypassed": True,
                    "selected_agents": selected_agents,
                    "agent_pipeline": _agent_pipeline(trace),
                    "response_blocks": response_blocks,
                },
            )
        if early_decision.action == EvidenceAction.HANDOFF:
            selected_agents = _selected_agents(early_decision.intent.value, {})
            response_blocks = build_response_blocks(
                action=early_decision.action.value,
                intent=early_decision.intent.value,
                graph_result={},
                citations=[],
                selected_agents=selected_agents,
            )
            _add_trace_step(
                trace,
                "safety_handoff_bypass",
                details={"retrieval_bypassed": True, "selected_agents": selected_agents},
            )
            return ChatResponse(
                message=format_response_blocks(response_blocks),
                conversation_id=conversation,
                agent_type=AgentType.SAFETY_MONITOR,
                confidence=0.95,
                warnings=early_decision.warnings + [format_medical_disclaimer()],
                suggestions=self._suggestions(early_decision.action.value),
                metadata={
                    "rag_action": early_decision.action.value,
                    "intent": early_decision.intent.value,
                    "retrieval_bypassed": True,
                    "should_answer": early_decision.should_answer,
                    "llm_answer_enabled": self.llm_answer.enabled,
                    "llm_answer_used": False,
                    "llm_provider": self.llm_answer.provider if self.llm_answer.enabled else None,
                    "selected_agents": selected_agents,
                    "agent_pipeline": _agent_pipeline(trace),
                    "response_blocks": response_blocks,
                },
            )

        started_at = time.perf_counter()
        alignment = self.name_alignment.align(message)
        effective_message = alignment["augmented_query"] if alignment.get("used") else message
        _add_trace_step(
            trace,
            "drug_name_alignment_agent",
            details={
                "used": alignment.get("used"),
                "canonical_terms": alignment.get("canonical_terms") or [],
                "match_count": len(alignment.get("matches") or []),
            },
            started_at=started_at,
        )

        started_at = time.perf_counter()
        graph_result = self.graph_safety.check(effective_message)
        _add_trace_step(
            trace,
            "graph_safety_agent",
            details={
                "should_warn": graph_result.get("should_warn"),
                "highest_risk": graph_result.get("highest_risk"),
                "findings_count": len(graph_result.get("findings") or []),
                "detected_drugs": graph_result.get("detected_drugs") or [],
            },
            started_at=started_at,
        )

        started_at = time.perf_counter()
        results = self.retrieve(effective_message)
        _add_trace_step(
            trace,
            "hybrid_rag_retrieval_agent",
            details={
                "retrieved_count": len(results),
                "retriever": "hybrid_bm25_chroma_priority",
                "chroma_dir": str(self.chroma_dir),
            },
            started_at=started_at,
        )

        started_at = time.perf_counter()
        decision = evaluate_evidence(effective_message, results)
        _add_trace_step(
            trace,
            "evidence_guardrail_agent",
            details={
                "action": decision.action.value,
                "intent": decision.intent.value,
                "should_answer": decision.should_answer,
                "usable_sources": decision.usable_sources,
                "blocked_sources": decision.blocked_sources,
            },
            started_at=started_at,
        )
        ranked = _rank_for_answer(effective_message, results)
        answer_rows = _select_answer_rows(graph_result, ranked)
        citations = [_citation_from_row(index, row) for index, row in enumerate(answer_rows[:5], 1)]
        graph_overrode_rag = bool(graph_result.get("should_warn"))

        if decision.action in {EvidenceAction.HANDOFF, EvidenceAction.INSUFFICIENT_EVIDENCE}:
            answer = self._handoff_message(decision.message, citations)
            confidence = 0.25
            agent_type = AgentType.SAFETY_MONITOR
        else:
            answer = self._allowed_answer(decision.action, answer_rows[:3], citations[:3])
            confidence = 0.72 if decision.action == EvidenceAction.ALLOW else 0.55
            agent_type = self._agent_type(decision.intent.value)

        graph_warning = format_graph_warning(graph_result["findings"])
        if graph_warning:
            answer = graph_warning + "\n\n" + answer
            confidence = max(confidence, 0.78)
            agent_type = AgentType.SAFETY_MONITOR
        _add_trace_step(
            trace,
            "graph_rag_join_node",
            details={
                "graph_overrode_rag": graph_overrode_rag,
                "answer_rows": len(answer_rows[:5]),
                "citation_count": len(citations),
            },
        )

        deterministic_answer = answer
        selected_agents = _selected_agents(decision.intent.value, graph_result, alignment)
        response_blocks = build_response_blocks(
            action=decision.action.value,
            intent=decision.intent.value,
            graph_result=graph_result,
            citations=citations[:5],
            selected_agents=selected_agents,
        )
        answer = format_response_blocks(response_blocks)
        llm_answer = None
        _add_trace_step(
            trace,
            "final_response_builder",
            details={
                "schema_version": response_blocks.get("schema_version"),
                "selected_agents": selected_agents,
                "llm_answer_used": False,
            },
        )

        warnings = list(dict.fromkeys(decision.warnings + [format_medical_disclaimer()]))
        if graph_result["should_warn"]:
            warnings.insert(0, "Graph safety check found structured medication safety warnings.")
        suggestions = self._suggestions(decision.action.value)

        return ChatResponse(
            message=answer,
            conversation_id=conversation,
            agent_type=agent_type,
            confidence=confidence,
            sources=citations,
            suggestions=suggestions,
            warnings=warnings,
            metadata={
                "rag_action": decision.action.value,
                "intent": decision.intent.value,
                "should_answer": decision.should_answer,
                "usable_sources": decision.usable_sources,
                "blocked_sources": decision.blocked_sources,
                "retrieved_count": len(results),
                "retriever": "hybrid_bm25_chroma_priority",
                "original_query": message,
                "effective_query": effective_message,
                "entity_alignment": alignment,
                "graph_safety": graph_result,
                "selected_agents": selected_agents,
                "agent_pipeline": _agent_pipeline(trace, graph_overrode_rag=graph_overrode_rag),
                "llm_answer_enabled": self.llm_answer.enabled,
                "llm_answer_used": bool(llm_answer),
                "llm_provider": self.llm_answer.provider if self.llm_answer.enabled else None,
                "deterministic_answer": deterministic_answer,
                "response_blocks": response_blocks,
                "context_provided": bool(context),
            },
        )

    def _allowed_answer(
        self,
        action: EvidenceAction,
        rows: List[Dict[str, Any]],
        citations: List[Citation],
    ) -> str:
        lines = [
            "Mình tìm thấy bằng chứng phù hợp để trả lời ở mức thông tin tham khảo.",
            "Các điểm dựa trên nguồn đã truy xuất:",
        ]
        for index, row in enumerate(rows, 1):
            citation_id = citations[index - 1].id if index <= len(citations) else f"S{index}"
            metadata = _metadata(row)
            title = (
                metadata.get("title")
                or metadata.get("drug_name")
                or row.get("title_or_drug")
                or "Nguồn dữ liệu"
            )
            lines.append(f"- [{citation_id}] {title}: {_preview(row)}")

        if action == EvidenceAction.ALLOW_WITH_CAUTION:
            lines.append(
                "Vì có yếu tố cần thận trọng, chỉ nên xem đây là thông tin chung; "
                "không tự đổi liều, phối hợp thuốc hoặc ngưng thuốc trong toa."
            )
        lines.append(
            "Khi dùng thuốc thật, hãy đối chiếu toa/nhãn thuốc và hỏi dược sĩ nếu còn chưa chắc."
        )
        return "\n".join(lines)

    def _handoff_message(self, reason: str, citations: List[Citation]) -> str:
        lines = [
            "Mình chưa có đủ bằng chứng đã xác minh để trả lời an toàn cho câu hỏi này.",
            reason,
            (
                "Với câu hỏi về liều dùng, tương tác, thai kỳ, trẻ em, bệnh gan/thận "
                "hoặc thuốc kê đơn, bạn nên hỏi trực tiếp bác sĩ/dược sĩ."
            ),
        ]
        if citations:
            lines.append(
                "Các nguồn truy xuất hiện chỉ nên dùng để định danh hoặc kiểm tra lại, "
                "không dùng để kết luận liều/tương tác:"
            )
            for citation in citations[:3]:
                title = citation.title or citation.source
                lines.append(f"- [{citation.id}] {title} ({citation.source})")
        return "\n".join(lines)

    def _emergency_message(self) -> str:
        return (
            "Đây có thể là tình huống cấp cứu hoặc phản ứng nghiêm trọng sau dùng thuốc. "
            "Vui lòng gọi 115 hoặc đến cơ sở y tế gần nhất ngay. "
            "Bot không nên hướng dẫn dùng thuốc chi tiết trong tình huống này."
        )

    def _suggestions(self, action: str) -> List[str]:
        if action in {"handoff", "insufficient_evidence"}:
            return [
                "Cung cấp tên thuốc, hàm lượng, dạng dùng và toa thuốc nếu có.",
                "Cho biết tuổi, thai kỳ/cho con bú, dị ứng, bệnh gan/thận và thuốc đang dùng.",
                "Hỏi trực tiếp bác sĩ/dược sĩ trước khi dùng hoặc phối hợp thuốc.",
            ]
        return [
            "Đối chiếu tên thuốc, số đăng ký, hàm lượng trên bao bì/toa thuốc.",
            "Hỏi dược sĩ nếu cần liều dùng cá nhân hóa hoặc đang dùng nhiều thuốc.",
        ]

    def _agent_type(self, intent: str) -> AgentType:
        if intent == "dosage":
            return AgentType.DOSAGE_ADVISOR
        if intent == "interaction":
            return AgentType.INTERACTION_CHECK
        if intent in {"recall", "counterfeit", "general_safety", "high_risk_context"}:
            return AgentType.SAFETY_MONITOR
        return AgentType.DRUG_INFO


_safe_rag_service: Optional[SafeRagService] = None


def get_safe_rag_service() -> SafeRagService:
    global _safe_rag_service
    if _safe_rag_service is None:
        _safe_rag_service = SafeRagService()
    return _safe_rag_service
