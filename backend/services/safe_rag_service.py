"""Safe RAG service dieu phoi pipeline tra loi thuoc OTC.

Service nay lay evidence, ap guardrails va tra ve cau tra loi co trich dan.
LLM co the viet lai cau tra loi deterministic nhung khong la nguon su that y te.

Cac ham helper da duoc tach ra:
- backend.services.retrieval_pipeline  : filter/boost/rank ket qua retrieval
- backend.services.response_assembly   : citation/response_block/agent trace helpers
"""
from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from backend.config import settings
from backend.models import AgentType, ChatResponse, Citation
from backend.safety.evidence_guardrails import (
    EvidenceAction,
    QuestionIntent,
    evaluate_evidence,
    classify_question_intent,
    normalize_text,
)
from backend.services.confidence_scorer import compute_confidence
from backend.services.final_response_builder import build_response_blocks, format_response_blocks
from backend.services.graph_safety_service import GraphSafetyService, format_graph_warning
from backend.services.llm_answer_service import LLMAnswerService
from backend.services.llm_intent_planner_service import LLMIntentPlanner
from backend.services.drug_name_alignment_service import DrugNameAlignmentService
from backend.services.patient_context_service import PatientContextService
from backend.services.query_ambiguity_service import AmbiguityAssessment, QueryAmbiguityService
from backend.services.query_expander import QueryExpander
from backend.services.reranker_service import RerankerService
from backend.services.semantic_rule_mapper import SemanticRuleMapper
from backend.utils import format_medical_disclaimer

# Import cac ham da tach sang retrieval_pipeline.py
from backend.services.retrieval_pipeline import (
    la_interaction_fast_path as _looks_like_interaction_fast_path,
    la_query_chi_dinh as _is_indication_question,
    la_row_chi_dinh as _is_indication_row,
    co_finding_otc_benh_nen as _has_condition_otc_finding,
    loc_cung_ket_qua as _hard_filter_results,
    ap_dung_chinh_sach_chi_dinh as _apply_indication_retrieval_policy,
    ap_dung_chinh_sach_rule as _apply_rule_retrieval_policy,
    xep_hang_de_tra_loi as _rank_for_answer,
    chon_rows_cho_tra_loi as _select_answer_rows,
    bo_sung_rule_context_vao_tin_nhan as _augment_with_rule_context,
    xay_metadata_filter_tu_rule as _rule_metadata_filter,
    lay_preview as _preview,
    la_query_otc_context as _looks_like_otc_context_query,
    _lay_metadata as _metadata,
    _lay_nguon as _source,
)
# Import cac ham da tach sang response_assembly.py
from backend.services.response_assembly import (
    xay_citation_tu_row as _citation_from_row,
    xay_citations_tu_graph_findings as _citations_from_graph_findings,
    citation_an_toan_mac_dinh as _baseline_safety_citations,
    danh_so_lai_citations as _renumber_citations,
    citations_thanh_dict as _citation_dicts,
    them_citation_block_vao_response as _with_citation_block_sources,
    tao_response_blocks_lam_ro as _clarification_response_blocks,
    bo_sung_patient_context_vao_tin_nhan as _augment_with_patient_context,
    them_buoc_trace as _add_trace_step,
    tao_agent_pipeline as _agent_pipeline,
    lay_diem_reranker_tu_trace as _reranker_top_score_from_trace,
    chon_agents as _selected_agents,
)


ROOT_DIR = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = ROOT_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from hybrid_search_rag import chroma_search, combine_results, load_bm25_index  # noqa: E402
from smoke_search_bm25 import search as bm25_search  # noqa: E402


DEFAULT_BM25_INDEX = ROOT_DIR / "data" / "embeddings" / "bm25" / "rag_bm25.pkl.gz"
DEFAULT_CHROMA_DIR = ROOT_DIR / "data" / "embeddings" / "chroma_priority"
DEFAULT_COLLECTION = settings.LOCAL_CHROMA_COLLECTION
DEFAULT_MODEL = settings.LOCAL_EMBEDDING_MODEL


def _decision_subtype(decision: Any) -> str:
    metadata = getattr(decision, "metadata", {}) or {}
    return str(getattr(decision, "subtype", "") or metadata.get("subtype") or "")


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
        self.intent_planner = LLMIntentPlanner()
        self.name_alignment = DrugNameAlignmentService()
        self.patient_context = PatientContextService()
        self.query_expander = QueryExpander()
        self.ambiguity_checker = QueryAmbiguityService(
            intent_planner=self.intent_planner,
            query_expander=self.query_expander,
        )
        self.reranker = RerankerService()
        self.rule_mapper = SemanticRuleMapper()

    def _load_bm25(self) -> Dict[str, Any]:
        if self._bm25_index is None:
            self._bm25_index = load_bm25_index(self.bm25_index_path)
        return self._bm25_index

    def _quick_supporting_citations(self, subtype: str, message: str) -> List[Citation]:
        if subtype != "paracetamol_overdose":
            return []
        try:
            rows = bm25_search(
                self._load_bm25(),
                "Paracetamol quÃ¡ liá»u tá»•n thÆ°Æ¡ng gan overdose",
                top_k=20,
            )
        except Exception:
            return []

        selected: List[Citation] = []
        for row in rows:
            text = normalize_text(
                " ".join(
                    [
                        row.get("document_preview") or "",
                        str(_metadata(row).get("title") or ""),
                        str(_metadata(row).get("drug_name") or ""),
                    ]
                )
            )
            if "paracetamol" not in text:
                continue
            if not any(term in text for term in ("qua lieu", "ton thuong gan", "doc gan", "suy gan")):
                continue
            selected.append(_citation_from_row(len(selected) + 1, row))
            if len(selected) >= 2:
                break
        return selected

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
        rule_context: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        retrieval_query = (
            str(rule_context.get("retrieval_query") or "")
            if rule_context and rule_context.get("matched")
            else ""
        ).strip() or question
        metadata_filter = _rule_metadata_filter(rule_context)
        indication_query = _is_indication_question(retrieval_query)
        effective_top_k = max(top_k, 20) if indication_query else top_k
        vector_top_k = 20 if rule_context and rule_context.get("matched") else 10
        if indication_query:
            vector_top_k = max(vector_top_k, 30)
        expanded_query = self.query_expander.expand_query(retrieval_query)
        if indication_query:
            expanded_query = f"{expanded_query} chá»‰ Ä‘á»‹nh cÃ´ng dá»¥ng háº¡ sá»‘t giáº£m Ä‘au"
        bm25_results = bm25_search(self._load_bm25(), expanded_query, top_k=500)
        chroma_results = chroma_search(
            expanded_query,
            str(self.chroma_dir),
            self.collection,
            "sentence-transformers",
            self.model,
            top_k=vector_top_k,
            metadata_filter=metadata_filter,
        )
        bm25_results = _hard_filter_results(bm25_results, rule_context, retrieval_query)
        chroma_results = _hard_filter_results(chroma_results, rule_context, retrieval_query)
        combined = combine_results(
            retrieval_query,
            bm25_results,
            chroma_results,
            bm25_weight=0.65,
            vector_weight=0.35,
            top_k=max(effective_top_k, 20) if rule_context and rule_context.get("matched") else effective_top_k,
        )
        combined = _apply_indication_retrieval_policy(retrieval_query, combined)
        return _apply_rule_retrieval_policy(combined, rule_context)[:effective_top_k]

    async def _handle_emergency(
        self,
        message: str,
        early_decision: Any,
        early_subtype: str,
        conversation: str,
        trace: List[Dict[str, Any]],
    ) -> ChatResponse:
        selected_agents = _selected_agents(early_decision.intent.value, {})
        bypass_citations = _renumber_citations(
            _baseline_safety_citations(early_decision.action.value, early_subtype)
            + self._quick_supporting_citations(early_subtype, message)
        )
        response_blocks = build_response_blocks(
            action=early_decision.action.value,
            intent=early_decision.intent.value,
            graph_result={},
            citations=bypass_citations,
            selected_agents=selected_agents,
            subtype=early_subtype,
        )
        response_blocks = _with_citation_block_sources(response_blocks, bypass_citations)
        confidence_score = compute_confidence(
            action=early_decision.action.value,
            intent=early_decision.intent.value,
            citations=_citation_dicts(bypass_citations),
            graph_result={},
            reranker_top_score=_reranker_top_score_from_trace(trace),
            planner_confidence=None,
        )
        _add_trace_step(
            trace,
            "emergency_bypass",
            details={
                "retrieval_bypassed": True,
                "selected_agents": selected_agents,
                "subtype": early_subtype,
                "confidence_score": confidence_score,
            },
        )
        deterministic_answer = format_response_blocks(response_blocks)
        llm_answer_text = await self.llm_answer.rewrite(
            question=message,
            deterministic_answer=deterministic_answer,
            graph_safety={},
            snippets=[],
            citations=bypass_citations
        )
        final_answer = llm_answer_text if llm_answer_text else deterministic_answer

        return ChatResponse(
            message=final_answer,
            conversation_id=conversation,
            agent_type=AgentType.SAFETY_MONITOR,
            confidence=confidence_score,
            sources=bypass_citations,
            warnings=early_decision.warnings,
            suggestions=["Gá»i 115 hoáº·c Ä‘áº¿n cÆ¡ sá»Ÿ y táº¿ gáº§n nháº¥t ngay."],
            metadata={
                "confidence": confidence_score,
                "rag_action": early_decision.action.value,
                "intent": early_decision.intent.value,
                "subtype": early_subtype,
                "original_query": message,
                "retrieval_bypassed": True,
                "selected_agents": selected_agents,
                "agent_pipeline": _agent_pipeline(trace),
                "response_blocks": response_blocks,
                "llm_answer_enabled": self.llm_answer.enabled,
                "llm_answer_used": bool(llm_answer_text),
                "llm_provider": self.llm_answer.provider if self.llm_answer.enabled else None,
            },
        )

    async def _handle_clarification(
        self,
        message: str,
        conversation: str,
        context_assessment: Any,
        rule_context: Dict[str, Any],
        planner_context: Dict[str, Any],
        planned_intent: str,
        early_decision: Any,
        early_subtype: str,
        trace: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None,
    ) -> ChatResponse:
        selected_agents = list(
            dict.fromkeys(
                [
                    "triage_risk_agent",
                    "llm_intent_planner",
                    "semantic_rule_mapper_agent",
                    "patient_context_collector",
                    "safety_monitor_agent",
                    "final_response_builder",
                ]
            )
        )
        bypass_citations = _baseline_safety_citations("needs_clarification", early_subtype)
        response_blocks = _clarification_response_blocks(
            intent=early_decision.intent.value,
            questions=context_assessment.questions,
            selected_agents=selected_agents,
            reason=context_assessment.reason,
        )
        response_blocks = _with_citation_block_sources(response_blocks, bypass_citations)
        confidence_score = compute_confidence(
            action="needs_clarification",
            intent=early_decision.intent.value,
            citations=_citation_dicts(bypass_citations),
            graph_result={},
            reranker_top_score=_reranker_top_score_from_trace(trace),
            planner_confidence=planner_context.get("confidence"),
        )
        _add_trace_step(
            trace,
            "clarification_bypass",
            details={
                "retrieval_bypassed": True,
                "selected_agents": selected_agents,
                "question_count": len(context_assessment.questions),
                "confidence_score": confidence_score,
            },
        )
        _add_trace_step(
            trace,
            "final_response_builder",
            details={
                "schema_version": response_blocks.get("schema_version"),
                "selected_agents": selected_agents,
                "llm_answer_used": False,
                "confidence_score": confidence_score,
            },
        )
        final_answer = format_response_blocks(response_blocks)

        return ChatResponse(
            message=final_answer,
            conversation_id=conversation,
            agent_type=AgentType.SAFETY_MONITOR,
            confidence=confidence_score,
            sources=bypass_citations,
            warnings=[
                "Patient context is required before giving medication advice.",
                format_medical_disclaimer(),
            ],
            suggestions=context_assessment.questions,
            metadata={
                "confidence": confidence_score,
                "rag_action": "needs_clarification",
                "intent": early_decision.intent.value,
                "planned_intent": planned_intent,
                "subtype": early_subtype,
                "original_query": message,
                "retrieval_bypassed": True,
                "should_answer": False,
                "patient_context": context_assessment.patient_context,
                "semantic_rule_context": rule_context,
                "llm_intent_planner": planner_context,
                "missing_context": context_assessment.missing_context,
                "clarification_questions": context_assessment.questions,
                "selected_agents": selected_agents,
                "agent_pipeline": _agent_pipeline(trace),
                "llm_answer_enabled": self.llm_answer.enabled,
                "llm_answer_used": False,
                "llm_provider": self.llm_answer.provider if self.llm_answer.enabled else None,
                "llm_planner_enabled": self.intent_planner.enabled,
                "llm_planner_used": bool(planner_context.get("used")),
                "response_blocks": response_blocks,
                "context_provided": bool(context),
            },
        )

    async def _handle_graph_fast_path(
        self,
        message: str,
        conversation: str,
        effective_message: str,
        context_message: str,
        context_assessment: Any,
        rule_context: Dict[str, Any],
        alignment: Any,
        graph_result: Dict[str, Any],
        planner_context: Dict[str, Any],
        planned_intent: str,
        early_decision: Any,
        early_subtype: str,
        trace: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None,
    ) -> ChatResponse:
        selected_agents = _selected_agents(early_decision.intent.value, graph_result, alignment)
        if rule_context.get("matched"):
            selected_agents.insert(1, "semantic_rule_mapper_agent")
        if context_assessment.risk_flags:
            selected_agents.insert(1, "patient_context_collector")
        selected_agents = list(dict.fromkeys(selected_agents))
        final_action = EvidenceAction.ALLOW_WITH_CAUTION
        response_blocks = build_response_blocks(
            action=final_action.value,
            intent=early_decision.intent.value,
            graph_result=graph_result,
            citations=graph_citations[:5],
            selected_agents=selected_agents,
            subtype=early_subtype,
        )
        answer = format_response_blocks(response_blocks)
        llm_answer = await self.llm_answer.rewrite(
            question=effective_message,
            deterministic_answer=answer,
            graph_safety=graph_result,
            snippets=[],
            citations=graph_citations[:5],
        )
        if llm_answer:
            answer = llm_answer
        confidence_score = compute_confidence(
            action=final_action.value,
            intent=early_decision.intent.value,
            citations=_citation_dicts(graph_citations[:5]),
            graph_result=graph_result,
            reranker_top_score=_reranker_top_score_from_trace(trace),
            planner_confidence=planner_context.get("confidence"),
        )
        _add_trace_step(
            trace,
            "graph_fast_path_bypass_retrieval",
            details={
                "retrieval_bypassed": True,
                "reason": "graph_safety_has_structured_citations",
                "citation_count": len(graph_citations),
                "selected_agents": selected_agents,
                "confidence_score": confidence_score,
            },
        )
        _add_trace_step(
            trace,
            "final_response_builder",
            details={
                    "schema_version": response_blocks.get("schema_version"),
                    "selected_agents": selected_agents,
                    "llm_answer_used": bool(llm_answer),
                    "confidence_score": confidence_score,
                },
            )
        warnings = ["Graph safety check found structured medication safety warnings."]
        warnings.extend(early_decision.warnings)
        warnings.append(format_medical_disclaimer())
        return ChatResponse(
            message=answer,
            conversation_id=conversation,
            agent_type=AgentType.SAFETY_MONITOR,
            confidence=confidence_score,
            sources=graph_citations[:5],
            suggestions=self._suggestions(final_action.value),
            warnings=list(dict.fromkeys(warnings)),
            metadata={
                "confidence": confidence_score,
                "rag_action": final_action.value,
                "intent": early_decision.intent.value,
                "subtype": early_subtype,
                "should_answer": True,
                "retrieval_bypassed": True,
                "retriever": "graph_fast_path",
                "original_query": message,
                "context_augmented_query": context_message,
                "effective_query": effective_message,
                "entity_alignment": alignment,
                "patient_context": context_assessment.patient_context,
                "semantic_rule_context": rule_context,
                "llm_intent_planner": planner_context,
                "missing_context": context_assessment.missing_context,
                "clarification_questions": context_assessment.questions,
                "graph_safety": graph_result,
                "selected_agents": selected_agents,
                "agent_pipeline": _agent_pipeline(trace),
                "llm_answer_enabled": self.llm_answer.enabled,
                "llm_answer_used": bool(llm_answer),
                "llm_provider": self.llm_answer.provider if self.llm_answer.enabled else None,
                "response_blocks": response_blocks,
                "context_provided": bool(context),
            },
    )

    async def _handle_rag_full_pipeline(
        self,
        message: str,
        conversation: str,
        effective_message: str,
        context_message: str,
        context_assessment: Any,
        rule_context: Dict[str, Any],
        alignment: Any,
        graph_result: Dict[str, Any],
        planner_context: Dict[str, Any],
        planned_intent: str,
        early_decision: Any,
        early_subtype: str,
        trace: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None,
    ) -> ChatResponse:
        started_at = time.perf_counter()
        retrieved_results = self.retrieve(effective_message, rule_context=rule_context)
        results = retrieved_results
        _add_trace_step(
            trace,
            "hybrid_rag_retrieval_agent",
            details={
                "retrieved_count": len(results),
                "retriever": "hybrid_bm25_chroma_priority",
                "matrix_rule_id": rule_context.get("rule_id"),
                "matrix_retrieval_query": rule_context.get("retrieval_query"),
                "chroma_dir": str(self.chroma_dir),
            },
            started_at=started_at,
        )

        started_at = time.perf_counter()
        results = self.reranker.rerank(effective_message, results)
        if _is_indication_question(effective_message):
            merged_by_id = {str(row.get("id") or index): row for index, row in enumerate(results)}
            for row in retrieved_results:
                if _is_indication_row(row):
                    merged_by_id.setdefault(str(row.get("id") or len(merged_by_id)), row)
            results = _apply_indication_retrieval_policy(effective_message, list(merged_by_id.values()))[:20]
        _add_trace_step(
            trace,
            "reranker_agent",
            details={
                "reranked_count": self.reranker.last_reranked_count,
                "top_score": self.reranker.last_top_score,
                "fallback_used": self.reranker.fallback_used,
            },
            started_at=started_at,
        )

        started_at = time.perf_counter()
        try:
            decision_intent = QuestionIntent(planned_intent)
        except ValueError:
            decision_intent = early_decision.intent
        decision = evaluate_evidence(effective_message, decision_intent, results)
        decision_subtype = _decision_subtype(decision)
        if _is_indication_question(effective_message):
            decision_subtype = "indication"
        _add_trace_step(
            trace,
            "evidence_guardrail_agent",
            details={
                "action": decision.action.value,
                "intent": decision.intent.value,
                "subtype": decision_subtype,
                "planned_intent": planned_intent,
                "should_answer": decision.should_answer,
                "usable_sources": decision.usable_sources,
                "blocked_sources": decision.blocked_sources,
            },
            started_at=started_at,
        )
        ranked = _rank_for_answer(effective_message, results)
        answer_rows = _select_answer_rows(graph_result, ranked)
        citations = [_citation_from_row(index, row) for index, row in enumerate(answer_rows[:5], 1)]
        public_answer_rows = answer_rows
        public_citations = citations
        if decision.action in {EvidenceAction.HANDOFF, EvidenceAction.INSUFFICIENT_EVIDENCE}:
            public_answer_rows = []
            public_citations = []
        graph_overrode_rag = bool(graph_result.get("should_warn"))
        if graph_result.get("should_warn"):
            graph_citations = _citations_from_graph_findings(graph_result.get("findings") or [])
            if graph_citations:
                public_citations = graph_citations
        if not public_citations:
            public_citations = _baseline_safety_citations(decision.action.value, decision_subtype)
        public_citations = _renumber_citations(public_citations)

        if decision.action in {EvidenceAction.HANDOFF, EvidenceAction.INSUFFICIENT_EVIDENCE}:
            answer = self._handoff_message(decision.message, public_citations)
            agent_type = AgentType.SAFETY_MONITOR
        else:
            answer = self._allowed_answer(decision.action, answer_rows[:3], citations[:3])
            agent_type = self._agent_type(decision.intent.value)

        graph_warning = format_graph_warning(graph_result["findings"])
        if graph_warning:
            answer = graph_warning + "\n\n" + answer
            agent_type = AgentType.SAFETY_MONITOR
        final_action = decision.action
        if graph_result["should_warn"] and final_action in {
            EvidenceAction.ALLOW,
            EvidenceAction.HANDOFF,
            EvidenceAction.INSUFFICIENT_EVIDENCE,
        }:
            final_action = EvidenceAction.ALLOW_WITH_CAUTION
        _add_trace_step(
            trace,
            "graph_rag_join_node",
            details={
                "graph_overrode_rag": graph_overrode_rag,
                "answer_rows": len(public_answer_rows[:5]),
                "citation_count": len(public_citations),
            },
        )

        deterministic_answer = answer
        response_subtype = "indication" if _is_indication_question(effective_message) else decision_subtype
        selected_agents = _selected_agents(decision.intent.value, graph_result, alignment)
        if rule_context.get("matched"):
            selected_agents.insert(1, "semantic_rule_mapper_agent")
        if context_assessment.risk_flags:
            selected_agents.insert(1, "patient_context_collector")
            selected_agents = list(dict.fromkeys(selected_agents))
        response_blocks = build_response_blocks(
            action=final_action.value,
            intent=decision.intent.value,
            graph_result=graph_result,
            citations=public_citations[:5],
            selected_agents=selected_agents,
            subtype=response_subtype,
            snippets=public_answer_rows[:5] if public_answer_rows else None,
        )
        answer = format_response_blocks(response_blocks)
        llm_answer = await self.llm_answer.rewrite(
            question=effective_message,
            deterministic_answer=answer,
            graph_safety=graph_result,
            snippets=public_answer_rows[:5],
            citations=public_citations[:5],
            patient_context=context_assessment.patient_context,
        )
        if llm_answer:
            answer = llm_answer

        confidence_score = compute_confidence(
            action=final_action.value,
            intent=decision.intent.value,
            citations=_citation_dicts(public_citations),
            graph_result=graph_result,
            reranker_top_score=_reranker_top_score_from_trace(trace),
            planner_confidence=planner_context.get("confidence"),
        )
        _add_trace_step(
            trace,
            "final_response_builder",
            details={
                "schema_version": response_blocks.get("schema_version"),
                "selected_agents": selected_agents,
                "llm_answer_used": bool(llm_answer),
                "confidence_score": confidence_score,
            },
        )

        warnings = list(dict.fromkeys(decision.warnings + [format_medical_disclaimer()]))
        if context_assessment.should_ask:
            warnings.extend(context_assessment.questions)
        if graph_result["should_warn"]:
            warnings.insert(0, "Graph safety check found structured medication safety warnings.")
        suggestions = self._suggestions(decision.action.value)

        return ChatResponse(
            message=answer,
            conversation_id=conversation,
            agent_type=agent_type,
            confidence=confidence_score,
            sources=public_citations,
            suggestions=suggestions,
            warnings=warnings,
            metadata={
                "confidence": confidence_score,
                "rag_action": final_action.value,
                "intent": decision.intent.value,
                "subtype": decision_subtype,
                "should_answer": decision.should_answer,
                "usable_sources": decision.usable_sources,
                "blocked_sources": decision.blocked_sources,
                "retrieved_count": len(results),
                "retriever": "hybrid_bm25_chroma_priority",
                "original_query": message,
                "context_augmented_query": context_message,
                "effective_query": effective_message,
                "entity_alignment": alignment,
                    "patient_context": context_assessment.patient_context,
                    "semantic_rule_context": rule_context,
                    "llm_intent_planner": planner_context,
                    "missing_context": context_assessment.missing_context,
                "clarification_questions": context_assessment.questions,
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
        intent_value = classify_question_intent(message)
        early_decision = evaluate_evidence(message, intent_value, [])
        early_subtype = _decision_subtype(early_decision)
        _add_trace_step(
            trace,
            "safety_router",
            details={
                "action": early_decision.action.value,
                "intent": early_decision.intent.value,
                "subtype": early_subtype,
                "should_answer": early_decision.should_answer,
            },
            started_at=started_at,
        )
        if early_decision.action != EvidenceAction.EMERGENCY:
            started_at = time.perf_counter()
            skip_ambiguity = _looks_like_otc_context_query(message) or bool(
                (context or {}).get("resume_pending_question") or (context or {}).get("resume_last_question")
            )
            if skip_ambiguity:
                ambiguity = AmbiguityAssessment(False, "clear", [], message)
            else:
                ambiguity = await self.ambiguity_checker.assess(message)
            _add_trace_step(
                trace,
                "ambiguity_checker",
                details={
                    "is_ambiguous": ambiguity.is_ambiguous,
                    "type": ambiguity.ambiguity_type,
                    "skipped_for_otc_context": skip_ambiguity,
                },
                started_at=started_at,
            )
            # Tạm tắt Ambiguity Checker cứng nhắc để nhường cho LLM xử lý thông minh hơn.
            if False and ambiguity.is_ambiguous:
                selected_agents = ["triage_risk_agent", "ambiguity_checker", "final_response_builder"]
                bypass_citations = _baseline_safety_citations("needs_clarification", "ambiguous_query")
                response_blocks = _clarification_response_blocks(
                    intent=early_decision.intent.value,
                    questions=ambiguity.questions,
                    selected_agents=selected_agents,
                    reason=ambiguity.ambiguity_type,
                )
                response_blocks = _with_citation_block_sources(response_blocks, bypass_citations)
                deterministic_answer = format_response_blocks(response_blocks)
                llm_answer_text = await self.llm_answer.rewrite(
                    question=message,
                    deterministic_answer=deterministic_answer,
                    graph_safety={},
                    snippets=[],
                    citations=bypass_citations,
                    patient_context=context_assessment.patient_context,
                )
                final_answer = llm_answer_text if llm_answer_text else deterministic_answer
                confidence_score = compute_confidence(
                    action="needs_clarification",
                    intent=early_decision.intent.value,
                    citations=_citation_dicts(bypass_citations),
                    graph_result={},
                )
                return ChatResponse(
                    message=final_answer,
                    conversation_id=conversation,
                    agent_type=AgentType.SAFETY_MONITOR,
                    confidence=confidence_score,
                    sources=bypass_citations,
                    warnings=["Câu hỏi chưa đủ thông tin để tra cứu thuốc an toàn."],
                    suggestions=ambiguity.questions,
                    metadata={
                        "confidence": confidence_score,
                        "rag_action": "needs_clarification",
                        "intent": early_decision.intent.value,
                        "ambiguity_type": ambiguity.ambiguity_type,
                        "retrieval_bypassed": True,
                        "selected_agents": selected_agents,
                        "agent_pipeline": _agent_pipeline(trace),
                        "llm_answer_used": bool(llm_answer_text),
                        "response_blocks": response_blocks,
                    },
                )
        if early_decision.action == EvidenceAction.EMERGENCY:
            return await self._handle_emergency(message, early_decision, early_subtype, conversation, trace)

        started_at = time.perf_counter()
        planner_context = await self.intent_planner.plan(
            question=message,
            fallback_intent=early_decision.intent.value,
            fallback_subtype=early_subtype,
        )
        planned_intent = str(planner_context.get("intent") or early_decision.intent.value)
        if planned_intent not in {intent.value for intent in QuestionIntent}:
            planned_intent = early_decision.intent.value
        _add_trace_step(
            trace,
            "llm_intent_planner",
            details={
                "used": planner_context.get("used"),
                "provider": planner_context.get("provider"),
                "intent": planned_intent,
                "subject": planner_context.get("subject"),
                "is_pediatric": planner_context.get("is_pediatric"),
                "missing_context_focus": planner_context.get("missing_context_focus") or [],
                "agents": planner_context.get("agents") or [],
                "confidence": planner_context.get("confidence"),
            },
            started_at=started_at,
        )

        interaction_fast_path = (
            early_decision.intent == QuestionIntent.INTERACTION
            or planned_intent == QuestionIntent.INTERACTION.value
            or _looks_like_interaction_fast_path(message, self.graph_safety)
        )
        if interaction_fast_path:
            graph_intent = QuestionIntent.INTERACTION
            started_at = time.perf_counter()
            graph_result = self.graph_safety.check(message)
            _add_trace_step(
                trace,
                "graph_safety_agent",
                details={
                    "should_warn": graph_result.get("should_warn"),
                    "highest_risk": graph_result.get("highest_risk"),
                    "findings_count": len(graph_result.get("findings") or []),
                    "detected_drugs": graph_result.get("detected_drugs") or [],
                    "fast_path_candidate": True,
                },
                started_at=started_at,
            )
            graph_citations = _renumber_citations(
                _citations_from_graph_findings(graph_result.get("findings") or [])
            )
            if graph_result.get("should_warn") and graph_citations:
                selected_agents = _selected_agents(
                    graph_intent.value,
                    graph_result,
                    {"used": False, "skipped": True, "reason": "graph_fast_path_before_alignment"},
                )
                selected_agents = list(dict.fromkeys(selected_agents))
                final_action = EvidenceAction.ALLOW_WITH_CAUTION
                response_blocks = build_response_blocks(
                    action=final_action.value,
                    intent=graph_intent.value,
                    graph_result=graph_result,
                    citations=graph_citations[:5],
                    selected_agents=selected_agents,
                    subtype=early_subtype,
                )
                answer = format_response_blocks(response_blocks)
                confidence_score = compute_confidence(
                    action=final_action.value,
                    intent=graph_intent.value,
                    citations=_citation_dicts(graph_citations[:5]),
                    graph_result=graph_result,
                    reranker_top_score=_reranker_top_score_from_trace(trace),
                    planner_confidence=planner_context.get("confidence"),
                )
                _add_trace_step(
                    trace,
                    "graph_fast_path_bypass_retrieval",
                    details={
                        "retrieval_bypassed": True,
                        "preprocessing_bypassed": [
                            "semantic_rule_mapper_agent",
                            "patient_context_collector",
                            "drug_name_alignment_agent",
                        ],
                        "reason": "interaction_intent_has_structured_graph_citations",
                        "citation_count": len(graph_citations),
                        "selected_agents": selected_agents,
                        "original_intent": early_decision.intent.value,
                        "effective_intent": graph_intent.value,
                        "confidence_score": confidence_score,
                    },
                )
                _add_trace_step(
                    trace,
                    "final_response_builder",
                    details={
                        "schema_version": response_blocks.get("schema_version"),
                        "selected_agents": selected_agents,
                        "llm_answer_used": False,
                        "confidence_score": confidence_score,
                    },
                )
                warnings = ["Graph safety check found structured medication safety warnings."]
                warnings.extend(early_decision.warnings)
                warnings.append(format_medical_disclaimer())
                return ChatResponse(
                    message=answer,
                    conversation_id=conversation,
                    agent_type=AgentType.SAFETY_MONITOR,
                    confidence=confidence_score,
                    sources=graph_citations[:5],
                    suggestions=self._suggestions(final_action.value),
                    warnings=list(dict.fromkeys(warnings)),
                    metadata={
                        "confidence": confidence_score,
                        "rag_action": final_action.value,
                        "intent": graph_intent.value,
                        "subtype": early_subtype,
                        "should_answer": True,
                        "retrieval_bypassed": True,
                        "retriever": "graph_fast_path",
                        "original_query": message,
                        "context_augmented_query": message,
                        "effective_query": message,
                        "entity_alignment": {
                            "used": False,
                            "skipped": True,
                            "reason": "graph_fast_path_before_alignment",
                        },
                        "patient_context": {},
                        "semantic_rule_context": {
                            "matched": False,
                            "skipped": True,
                            "reason": "interaction_intent_graph_fast_path",
                        },
                        "llm_intent_planner": planner_context,
                        "missing_context": [],
                        "clarification_questions": [],
                        "graph_safety": graph_result,
                        "selected_agents": selected_agents,
                        "agent_pipeline": _agent_pipeline(trace),
                        "llm_answer_enabled": self.llm_answer.enabled,
                        "llm_answer_used": False,
                        "llm_provider": self.llm_answer.provider if self.llm_answer.enabled else None,
                        "response_blocks": response_blocks,
                        "context_provided": bool(context),
                    },
                )

        started_at = time.perf_counter()
        rule_context = self.rule_mapper.map(message)
        _add_trace_step(
            trace,
            "semantic_rule_mapper_agent",
            details={
                "matched": rule_context.get("matched"),
                "rule_id": rule_context.get("rule_id"),
                "primary_intent": rule_context.get("primary_intent"),
                "target_otc_group": rule_context.get("target_otc_group"),
                "score": rule_context.get("score") or rule_context.get("best_score"),
                "method": rule_context.get("method"),
            },
            started_at=started_at,
        )

        fast_path_context_assessment = await self.patient_context.assess_hybrid(
            message=message,
            intent="otc_recommendation" if rule_context.get("matched") else planned_intent,
            context=context,
        )
        fast_path_patient_context = fast_path_context_assessment.patient_context
        pre_context_message = _augment_with_patient_context(
            message,
            fast_path_patient_context,
        )
        started_at = time.perf_counter()
        otc_graph_result = self.graph_safety.check(pre_context_message)
        _add_trace_step(
            trace,
            "graph_safety_agent",
            details={
                "should_warn": otc_graph_result.get("should_warn"),
                "highest_risk": otc_graph_result.get("highest_risk"),
                "findings_count": len(otc_graph_result.get("findings") or []),
                "detected_drugs": otc_graph_result.get("detected_drugs") or [],
                "otc_context_fast_path_candidate": True,
            },
            started_at=started_at,
        )
        if (
            rule_context.get("matched")
            and otc_graph_result.get("should_warn")
            and _has_condition_otc_finding(otc_graph_result)
            and not fast_path_context_assessment.should_ask
        ):
            selected_agents = list(
                dict.fromkeys(
                    [
                        "triage_risk_agent",
                        "semantic_rule_mapper_agent",
                        "graph_safety_agent",
                        "otc_recommendation_agent",
                        "final_response_builder",
                    ]
                )
            )
            graph_citations = _renumber_citations(
                _citations_from_graph_findings(otc_graph_result.get("findings") or [])
            )
            final_action = EvidenceAction.ALLOW_WITH_CAUTION
            response_blocks = build_response_blocks(
                action=final_action.value,
                intent=QuestionIntent.OTC_RECOMMENDATION.value,
                graph_result=otc_graph_result,
                citations=graph_citations[:5],
                selected_agents=selected_agents,
                subtype=early_subtype,
            )
            answer = format_response_blocks(response_blocks)
            confidence_score = compute_confidence(
                action=final_action.value,
                intent=QuestionIntent.OTC_RECOMMENDATION.value,
                citations=_citation_dicts(graph_citations[:5]),
                graph_result=otc_graph_result,
                reranker_top_score=_reranker_top_score_from_trace(trace),
                planner_confidence=planner_context.get("confidence"),
            )
            _add_trace_step(
                trace,
                "otc_graph_fast_path_bypass_clarification",
                details={
                    "retrieval_bypassed": True,
                    "reason": "condition_otc_structured_warning",
                    "citation_count": len(graph_citations),
                    "selected_agents": selected_agents,
                    "confidence_score": confidence_score,
                },
            )
            _add_trace_step(
                trace,
                "final_response_builder",
                details={
                    "schema_version": response_blocks.get("schema_version"),
                    "selected_agents": selected_agents,
                    "llm_answer_used": False,
                    "confidence_score": confidence_score,
                },
            )
            warnings = ["CÃ³ bá»‡nh ná»n liÃªn quan Ä‘áº¿n lá»±a chá»n thuá»‘c OTC; nÃªn trÃ¡nh nhÃ³m thuá»‘c nguy cÆ¡ vÃ  há»i dÆ°á»£c sÄ© khi mua."]
            warnings.extend(early_decision.warnings)
            warnings.append(format_medical_disclaimer())
            return ChatResponse(
                message=answer,
                conversation_id=conversation,
                agent_type=AgentType.SAFETY_MONITOR,
                confidence=confidence_score,
                sources=graph_citations[:5],
                suggestions=self._suggestions(final_action.value),
                warnings=list(dict.fromkeys(warnings)),
                metadata={
                    "confidence": confidence_score,
                    "rag_action": final_action.value,
                    "intent": QuestionIntent.OTC_RECOMMENDATION.value,
                    "subtype": early_subtype,
                    "should_answer": True,
                    "retrieval_bypassed": True,
                    "retriever": "otc_graph_fast_path",
                    "original_query": message,
                    "context_augmented_query": pre_context_message,
                    "effective_query": pre_context_message,
                    "entity_alignment": {"used": False, "skipped": True, "reason": "otc_graph_fast_path_before_alignment"},
                    "patient_context": fast_path_patient_context,
                    "semantic_rule_context": rule_context,
                    "llm_intent_planner": planner_context,
                    "missing_context": [],
                    "clarification_questions": [],
                    "graph_safety": otc_graph_result,
                    "selected_agents": selected_agents,
                    "agent_pipeline": _agent_pipeline(trace),
                    "llm_answer_enabled": self.llm_answer.enabled,
                    "llm_answer_used": False,
                    "llm_provider": self.llm_answer.provider if self.llm_answer.enabled else None,
                    "response_blocks": response_blocks,
                    "context_provided": bool(context),
                },
            )

        # Tai dung ket qua da danh gia o buoc fast_path phia tren
        # (cung message + cung intent + cung context) - tranh goi 2 lan
        context_assessment = fast_path_context_assessment
        _add_trace_step(
            trace,
            "patient_context_collector",
            details={
                "should_ask": context_assessment.should_ask,
                "missing_context": context_assessment.missing_context,
                "risk_flags": context_assessment.risk_flags,
                "reused_from_fast_path": True,
            },
            started_at=started_at,
        )
        if context_assessment.should_ask:
            return await self._handle_clarification(message, conversation, context_assessment, rule_context, planner_context, planned_intent, early_decision, early_subtype, trace, context)
#         if context_assessment.should_ask:
#             selected_agents = list(
#                 dict.fromkeys(
#                     [
#                         "triage_risk_agent",
#                         "llm_intent_planner",
#                         "semantic_rule_mapper_agent",
#                         "patient_context_collector",
#                         "safety_monitor_agent",
#                         "final_response_builder",
#                     ]
#                 )
#             )
#             bypass_citations = _baseline_safety_citations("needs_clarification", early_subtype)
#             response_blocks = _clarification_response_blocks(
#                 intent=early_decision.intent.value,
#                 questions=context_assessment.questions,
#                 selected_agents=selected_agents,
#                 reason=context_assessment.reason,
#             )
#             response_blocks = _with_citation_block_sources(response_blocks, bypass_citations)
#             confidence_score = compute_confidence(
#                 action="needs_clarification",
#                 intent=early_decision.intent.value,
#                 citations=_citation_dicts(bypass_citations),
#                 graph_result={},
#                 reranker_top_score=_reranker_top_score_from_trace(trace),
#                 planner_confidence=planner_context.get("confidence"),
#             )
#             _add_trace_step(
#                 trace,
#                 "clarification_bypass",
#                 details={
#                     "retrieval_bypassed": True,
#                     "selected_agents": selected_agents,
#                     "question_count": len(context_assessment.questions),
#                     "confidence_score": confidence_score,
#                 },
#             )
#             deterministic_answer = format_response_blocks(response_blocks)
#             llm_answer_text = await self.llm_answer.rewrite(
#                 question=message,
#                 deterministic_answer=deterministic_answer,
#                 graph_safety={},
#                 snippets=[],
#                 citations=bypass_citations
#             )
#             final_answer = llm_answer_text if llm_answer_text else deterministic_answer
# 
#             return ChatResponse(
#                 message=final_answer,
#                 conversation_id=conversation,
#                 agent_type=AgentType.SAFETY_MONITOR,
#                 confidence=confidence_score,
#                 sources=bypass_citations,
#                 warnings=[
#                     "Patient context is required before giving medication advice.",
#                     format_medical_disclaimer(),
#                 ],
#                 suggestions=context_assessment.questions,
#                 metadata={
#                     "confidence": confidence_score,
#                     "rag_action": "needs_clarification",
#                     "intent": early_decision.intent.value,
#                     "planned_intent": planned_intent,
#                     "subtype": early_subtype,
#                     "original_query": message,
#                     "retrieval_bypassed": True,
#                     "should_answer": False,
#                     "patient_context": context_assessment.patient_context,
#                     "llm_intent_planner": planner_context,
#                     "missing_context": context_assessment.missing_context,
#                     "clarification_questions": context_assessment.questions,
#                     "selected_agents": selected_agents,
#                     "agent_pipeline": _agent_pipeline(trace),
#                     "llm_answer_enabled": self.llm_answer.enabled,
#                     "llm_answer_used": bool(llm_answer_text),
#                     "llm_provider": self.llm_answer.provider if self.llm_answer.enabled else None,
#                     "llm_planner_enabled": self.intent_planner.enabled,
#                     "llm_planner_used": bool(planner_context.get("used")),
#                     "response_blocks": response_blocks,
#                     "context_provided": bool(context),
#                 },
#             )
        if early_decision.action == EvidenceAction.HANDOFF:
            selected_agents = _selected_agents(early_decision.intent.value, {})
            if context_assessment.risk_flags:
                selected_agents.insert(1, "patient_context_collector")
                selected_agents = list(dict.fromkeys(selected_agents))
            bypass_citations = _baseline_safety_citations(
                early_decision.action.value,
                early_subtype,
            )
            response_blocks = build_response_blocks(
                action=early_decision.action.value,
                intent=early_decision.intent.value,
                graph_result={},
                citations=bypass_citations,
                selected_agents=selected_agents,
                subtype=early_subtype,
            )
            response_blocks = _with_citation_block_sources(response_blocks, bypass_citations)
            confidence_score = compute_confidence(
                action=early_decision.action.value,
                intent=early_decision.intent.value,
                citations=_citation_dicts(bypass_citations),
                graph_result={},
                reranker_top_score=_reranker_top_score_from_trace(trace),
                planner_confidence=planner_context.get("confidence"),
            )
            _add_trace_step(
                trace,
                "safety_handoff_bypass",
                details={
                    "retrieval_bypassed": True,
                    "selected_agents": selected_agents,
                    "subtype": early_subtype,
                    "confidence_score": confidence_score,
                },
            )
            deterministic_answer = format_response_blocks(response_blocks)
            llm_answer_text = await self.llm_answer.rewrite(
                question=message,
                deterministic_answer=deterministic_answer,
                graph_safety={},
                snippets=[],
                citations=bypass_citations
            )
            final_answer = llm_answer_text if llm_answer_text else deterministic_answer

            return ChatResponse(
                message=final_answer,
                conversation_id=conversation,
                agent_type=AgentType.SAFETY_MONITOR,
                confidence=confidence_score,
                sources=bypass_citations,
                warnings=early_decision.warnings + [format_medical_disclaimer()],
                suggestions=self._suggestions(early_decision.action.value),
                metadata={
                    "confidence": confidence_score,
                    "rag_action": early_decision.action.value,
                    "intent": early_decision.intent.value,
                    "subtype": early_subtype,
                    "planned_intent": planned_intent,
                    "retrieval_bypassed": True,
                    "should_answer": early_decision.should_answer,
                    "llm_answer_enabled": self.llm_answer.enabled,
                    "llm_answer_used": bool(llm_answer_text),
                    "llm_provider": self.llm_answer.provider if self.llm_answer.enabled else None,
                    "patient_context": context_assessment.patient_context,
                    "llm_intent_planner": planner_context,
                    "missing_context": context_assessment.missing_context,
                    "clarification_questions": context_assessment.questions,
                    "selected_agents": selected_agents,
                    "agent_pipeline": _agent_pipeline(trace),
                    "response_blocks": response_blocks,
                },
            )

        started_at = time.perf_counter()
        context_message = _augment_with_patient_context(message, context_assessment.patient_context)
        if planner_context.get("retrieval_focus"):
            context_message += "\nPlanner focus: " + str(planner_context["retrieval_focus"])
        context_message = _augment_with_rule_context(context_message, rule_context)
        alignment = self.name_alignment.align(context_message)
        effective_message = alignment["augmented_query"] if alignment.get("used") else context_message
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

        graph_citations = _renumber_citations(
            _citations_from_graph_findings(graph_result.get("findings") or [])
        )
        if graph_result.get("should_warn") and graph_citations:
            return await self._handle_graph_fast_path(message, conversation, effective_message, context_message, context_assessment, rule_context, alignment, graph_result, planner_context, planned_intent, early_decision, early_subtype, trace, context)

        return await self._handle_rag_full_pipeline(
            message, conversation, effective_message, context_message, context_assessment,
            rule_context, alignment, graph_result, planner_context, planned_intent, early_decision, early_subtype, trace, context
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
        if intent in {"recall", "counterfeit", "general_safety", "high_risk_context", "otc_recommendation"}:
            return AgentType.SAFETY_MONITOR
        return AgentType.DRUG_INFO



_safe_rag_service: Optional[SafeRagService] = None


def get_safe_rag_service() -> SafeRagService:
    global _safe_rag_service
    if _safe_rag_service is None:
        _safe_rag_service = SafeRagService()
    return _safe_rag_service
