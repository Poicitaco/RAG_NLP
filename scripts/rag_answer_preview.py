"""End-to-end safe RAG answer preview without an LLM call.

This script demonstrates the intended production flow:
hybrid retrieval -> evidence guardrail -> citation-aware answer skeleton.
It intentionally avoids free-form generation so the preview is deterministic
and useful for reports/evaluation.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.safety.evidence_guardrails import (
    EvidenceAction,
    evaluate_evidence,
    is_unverified_ocr,
    mentioned_common_drugs,
    normalize_text,
)
from hybrid_search_rag import chroma_search, combine_results, load_bm25_index
from smoke_search_bm25 import search as bm25_search


DEFAULT_BM25_INDEX = "data/embeddings/bm25/rag_bm25.pkl.gz"
DEFAULT_CHROMA_DIR = "data/embeddings/chroma_priority"
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


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def source_label(metadata: Dict[str, Any]) -> str:
    source = metadata.get("source") or metadata.get("source_dataset") or "unknown"
    title = metadata.get("title") or metadata.get("drug_name") or metadata.get("registration_number") or ""
    return f"{source}: {title}".strip(": ")


def row_text(row: Dict[str, Any]) -> str:
    metadata = row.get("metadata") or {}
    values = [
        row.get("document_preview"),
        row.get("document"),
        metadata.get("title"),
        metadata.get("drug_name"),
        metadata.get("active_ingredients"),
        metadata.get("main_ingredient"),
    ]
    return normalize_text(" ".join(str(value) for value in values if value))


def rank_evidence_for_prompt(question: str, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    question_drugs = mentioned_common_drugs(question)

    def key(row: Dict[str, Any]) -> tuple:
        metadata = row.get("metadata") or {}
        source = metadata.get("source") or metadata.get("source_dataset") or row.get("source") or ""
        text = row_text(row)
        drug_match = 0 if not question_drugs or any(term in text for term in question_drugs) else 1
        ocr_penalty = 1 if is_unverified_ocr(row) else 0
        source_rank = SOURCE_PRIORITY.get(str(source), 4)
        hybrid_rank = row.get("rank") or 999
        return (drug_match, ocr_penalty, source_rank, hybrid_rank)

    return sorted(results, key=key)


def make_citations(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    citations = []
    for index, row in enumerate(results, 1):
        metadata = row.get("metadata") or {}
        citations.append(
            {
                "id": f"S{index}",
                "source": metadata.get("source") or metadata.get("source_dataset"),
                "title": metadata.get("title") or metadata.get("drug_name"),
                "url": metadata.get("source_url") or metadata.get("url"),
                "type": metadata.get("type"),
                "trust_level": metadata.get("trust_level") or "official_registry",
            }
        )
    return citations


def should_show_citations(action: EvidenceAction) -> bool:
    return action not in {EvidenceAction.EMERGENCY, EvidenceAction.INSUFFICIENT_EVIDENCE}


def build_answer_preview(question: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
    decision = evaluate_evidence(question, results)
    prompt_results = rank_evidence_for_prompt(question, results)
    citations = make_citations(prompt_results[:5]) if should_show_citations(decision.action) else []

    if decision.action in {EvidenceAction.EMERGENCY, EvidenceAction.HANDOFF, EvidenceAction.INSUFFICIENT_EVIDENCE}:
        answer = decision.message
        if decision.warnings:
            answer += "\n\nLưu ý: " + " ".join(decision.warnings)
    else:
        top_lines = []
        for index, row in enumerate(prompt_results[:3], 1):
            metadata = row.get("metadata") or {}
            preview = (row.get("document_preview") or row.get("document") or "").strip()
            if len(preview) > 260:
                preview = preview[:260].rstrip() + "..."
            top_lines.append(f"- [S{index}] {source_label(metadata)}: {preview}")
        answer = (
            f"Evidence guardrail cho phép trả lời ở mức `{decision.action.value}`.\n"
            "Các bằng chứng nên đưa vào prompt sinh câu trả lời:\n"
            + "\n".join(top_lines)
        )
        if decision.warnings:
            answer += "\n\nCảnh báo khi sinh câu trả lời: " + " ".join(decision.warnings)

    return {
        "question": question,
        "decision": {
            "action": decision.action.value,
            "intent": decision.intent.value,
            "should_answer": decision.should_answer,
            "message": decision.message,
            "warnings": decision.warnings,
            "usable_sources": decision.usable_sources,
            "blocked_sources": decision.blocked_sources,
        },
        "answer_preview": answer,
        "citations": citations,
        "retrieved": [
            {
                "rank": row.get("rank"),
                "id": row.get("id"),
                "hybrid_score": row.get("hybrid_score"),
                "source": row.get("source"),
                "type": row.get("type"),
                "trust_level": row.get("trust_level"),
                "title_or_drug": row.get("title_or_drug"),
                "retrievers": row.get("sources"),
            }
            for row in results
        ],
    }


def run_preview(args: argparse.Namespace, question: str) -> Dict[str, Any]:
    early_decision = evaluate_evidence(question, [])
    if early_decision.action == EvidenceAction.EMERGENCY:
        return build_answer_preview(question, [])

    bm25_index = load_bm25_index(Path(args.bm25_index))
    bm25_results = bm25_search(bm25_index, question, args.bm25_k)
    chroma_results = chroma_search(
        question,
        args.chroma_dir,
        args.collection,
        args.provider,
        args.model,
        args.vector_k,
    )
    results = combine_results(
        question,
        bm25_results,
        chroma_results,
        args.bm25_weight,
        args.vector_weight,
        args.top_k,
    )
    return build_answer_preview(question, results)


def main() -> None:
    configure_stdout()
    parser = argparse.ArgumentParser()
    parser.add_argument("question", nargs="?")
    parser.add_argument("--questions-file")
    parser.add_argument("--bm25-index", default=DEFAULT_BM25_INDEX)
    parser.add_argument("--chroma-dir", default=DEFAULT_CHROMA_DIR)
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--provider", choices=["sentence-transformers", "openai"], default="sentence-transformers")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--bm25-k", type=int, default=500)
    parser.add_argument("--vector-k", type=int, default=10)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--bm25-weight", type=float, default=0.65)
    parser.add_argument("--vector-weight", type=float, default=0.35)
    parser.add_argument("--json-output", default=None)
    args = parser.parse_args()

    questions = []
    if args.questions_file:
        with Path(args.questions_file).open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                row = json.loads(line)
                questions.append(row.get("question") or row.get("message") or "")
    elif args.question:
        questions.append(args.question)
    else:
        raise SystemExit("Provide a question or --questions-file")

    payload = {"results": [run_preview(args, question) for question in questions if question]}
    if args.json_output:
        Path(args.json_output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_output).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
