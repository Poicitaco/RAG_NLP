"""Hybrid BM25 + Chroma retrieval for the pharmaceutical RAG corpus.

BM25 is strong for exact drug names, registration numbers, strengths, and active
ingredients. Chroma/vector search is useful for semantic phrasing. This script
combines both and applies small evidence-aware boosts/penalties so safety
sources are preferred for recall/counterfeit questions and unverified OCR is not
over-trusted for high-risk questions.
"""
from __future__ import annotations

import argparse
import gzip
import json
import pickle
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, List

from ingest_rag_corpus import embed_texts, load_embedding_model
from smoke_search_bm25 import search as bm25_search


DEFAULT_BM25_INDEX = "data/embeddings/bm25/rag_bm25.pkl.gz"
DEFAULT_CHROMA_DIR = "data/embeddings/chroma"
DEFAULT_COLLECTION = "pharmaceutical_knowledge"
DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

SAFETY_TERMS = {
    "thu hoi",
    "gia mao",
    "canh bao",
    "nguy hiem",
    "qua lieu",
    "di ung",
    "soc",
    "kho tho",
    "mang thai",
    "cho con bu",
    "tre em",
    "tuong tac",
}
HIGH_RISK_TERMS = {
    "lieu",
    "lieu dung",
    "cach dung",
    "mang thai",
    "cho con bu",
    "tre em",
    "qua lieu",
    "tuong tac",
}
SAFETY_SOURCES = {"dav_recall", "canhgiacduoc"}
SECONDARY_DUOCTHU_SOURCES = {"trungtamthuoc_duocthu"}
REGISTRY_SOURCES = {"dav_all", "dav_otc"}
CONDITION_GUARDRAIL_SOURCES = {"otc_condition_guardrail"}
COMMON_DRUG_TERMS = {
    "aceclofenac",
    "amoxicillin",
    "aspirin",
    "atorvastatin",
    "cefaclor",
    "cefixim",
    "clarithromycin",
    "codeine",
    "diclofenac",
    "fluconazole",
    "ibuprofen",
    "itraconazole",
    "loratadine",
    "methotrexate",
    "omeprazole",
    "paracetamol",
    "simvastatin",
    "tramadol",
    "warfarin",
}


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def normalize_text(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", (text or "").lower())
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def has_any_term(query: str, terms: set[str]) -> bool:
    normalized = normalize_text(query)
    return any(term in normalized for term in terms)


def query_drug_terms(query: str) -> List[str]:
    normalized = normalize_text(query)
    return [term for term in COMMON_DRUG_TERMS if term in normalized]


def metadata_source(metadata: Dict[str, Any]) -> str:
    return str(metadata.get("source") or metadata.get("source_dataset") or "")


def load_bm25_index(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Missing BM25 index: {path}")
    with gzip.open(path, "rb") as handle:
        return pickle.load(handle)


def chroma_search(
    query: str,
    persist_dir: str,
    collection_name: str,
    provider: str,
    model_name: str,
    top_k: int,
) -> List[Dict[str, Any]]:
    try:
        import chromadb
    except Exception as exc:
        print(f"Chroma unavailable, falling back to BM25 only: {exc}", file=sys.stderr)
        return []

    if not Path(persist_dir).exists():
        return []
    try:
        client = chromadb.PersistentClient(path=persist_dir)
        collection = client.get_collection(collection_name)
    except Exception:
        return []

    model = load_embedding_model(provider, model_name)
    query_embedding = embed_texts(model, provider, model_name, [query])[0]
    try:
        results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    except Exception as exc:
        print(f"Chroma query failed, falling back to BM25 only: {exc}", file=sys.stderr)
        return []

    rows: List[Dict[str, Any]] = []
    for index, doc_id in enumerate(results.get("ids", [[]])[0]):
        rows.append(
            {
                "rank": index + 1,
                "distance": results.get("distances", [[]])[0][index],
                "id": doc_id,
                "metadata": results.get("metadatas", [[]])[0][index],
                "document_preview": (results.get("documents", [[]])[0][index] or "")[:700],
            }
        )
    return rows


def rank_score(rank: int, weight: float) -> float:
    return weight / max(rank, 1)


def source_adjustment(query: str, metadata: Dict[str, Any], document_preview: str = "") -> float:
    source = metadata_source(metadata)
    doc_type = str(metadata.get("type") or "")
    trust_level = str(metadata.get("trust_level") or "official_registry")
    is_safety_query = has_any_term(query, SAFETY_TERMS)
    is_high_risk_query = has_any_term(query, HIGH_RISK_TERMS)
    is_condition_otc_query = has_any_term(query, {"tieu duong", "dai thao duong", "thuoc cam", "cam cum"})
    mentioned_drugs = query_drug_terms(query)
    row_text = normalize_text(
        " ".join(
            str(metadata.get(field) or "")
            for field in (
                "title",
                "drug_name",
                "main_ingredient",
                "active_ingredients",
                "section_title",
                "section",
                "slug",
            )
        )
        + " "
        + (document_preview or "")
    )
    title_text = normalize_text(
        " ".join(
            str(metadata.get(field) or "")
            for field in ("title", "drug_name", "main_ingredient", "active_ingredients", "slug")
        )
    )
    mentions_query_drug = bool(mentioned_drugs) and any(term in row_text for term in mentioned_drugs)
    title_mentions_query_drug = bool(mentioned_drugs) and any(term in title_text for term in mentioned_drugs)
    matched_drug_count = sum(1 for term in mentioned_drugs if term in row_text)
    normalized_query = normalize_text(query)
    wants_interaction = "tuong tac" in normalized_query

    score = 0.0
    if is_safety_query and source in SAFETY_SOURCES:
        score += 0.45
    if is_condition_otc_query and source in CONDITION_GUARDRAIL_SOURCES:
        score += 1.5
    if is_safety_query and source in SECONDARY_DUOCTHU_SOURCES:
        score += 0.3
    if is_safety_query and doc_type in {"safety_recall", "safety_article", "safety"}:
        score += 0.25
    if is_safety_query and doc_type in {"interaction", "dosage"}:
        score += 0.2
    if wants_interaction and doc_type == "interaction":
        score += 0.65
    if wants_interaction and source in SECONDARY_DUOCTHU_SOURCES and doc_type == "interaction":
        score += 0.35
    if source == "ddinter" and doc_type == "interaction" and len(mentioned_drugs) >= 2:
        score += 0.9
        if matched_drug_count >= 2:
            score += 0.9
    if wants_interaction and source in REGISTRY_SOURCES:
        score -= 0.45
    if wants_interaction and doc_type == "drug_info":
        score -= 0.25
    if mentioned_drugs and title_mentions_query_drug:
        score += 0.55
    elif mentioned_drugs and mentions_query_drug:
        score += 0.2
    if mentioned_drugs and is_high_risk_query and source in SECONDARY_DUOCTHU_SOURCES and not mentions_query_drug:
        score -= 0.45
    if not is_safety_query and source in REGISTRY_SOURCES:
        score += 0.1
    if is_high_risk_query and trust_level == "unverified_ocr":
        score -= 0.35
    return score


def combine_results(
    query: str,
    bm25_results: List[Dict[str, Any]],
    chroma_results: List[Dict[str, Any]],
    bm25_weight: float,
    vector_weight: float,
    top_k: int,
) -> List[Dict[str, Any]]:
    merged: Dict[str, Dict[str, Any]] = {}

    for result in bm25_results:
        doc_id = str(result["id"])
        metadata = result.get("metadata") or {}
        item = merged.setdefault(
            doc_id,
            {
                "id": doc_id,
                "metadata": metadata,
                "document_preview": result.get("document_preview") or "",
                "sources": [],
                "score": 0.0,
                "adjustment": 0.0,
            },
        )
        item["sources"].append({"retriever": "bm25", "rank": result["rank"], "score": result["score"]})
        item["score"] += rank_score(int(result["rank"]), bm25_weight)

    for result in chroma_results:
        doc_id = str(result["id"])
        metadata = result.get("metadata") or {}
        item = merged.setdefault(
            doc_id,
            {
                "id": doc_id,
                "metadata": metadata,
                "document_preview": result.get("document_preview") or "",
                "sources": [],
                "score": 0.0,
                "adjustment": 0.0,
            },
        )
        item["sources"].append(
            {
                "retriever": "chroma",
                "rank": result["rank"],
                "distance": round(float(result.get("distance") or 0.0), 6),
            }
        )
        item["score"] += rank_score(int(result["rank"]), vector_weight)
        if not item["document_preview"]:
            item["document_preview"] = result.get("document_preview") or ""
        if not item["metadata"]:
            item["metadata"] = metadata

    rows = []
    for item in merged.values():
        adjustment = source_adjustment(query, item["metadata"], item.get("document_preview") or "")
        item["adjustment"] = round(adjustment, 4)
        item["hybrid_score"] = round(item["score"] + adjustment, 6)
        rows.append(item)

    rows.sort(key=lambda row: row["hybrid_score"], reverse=True)
    for rank, row in enumerate(rows[:top_k], 1):
        row["rank"] = rank
        row["source"] = metadata_source(row["metadata"])
        row["type"] = row["metadata"].get("type")
        row["trust_level"] = row["metadata"].get("trust_level") or "official_registry"
        row["title_or_drug"] = row["metadata"].get("title") or row["metadata"].get("drug_name")
    return rows[:top_k]


def main() -> None:
    configure_stdout()

    parser = argparse.ArgumentParser()
    parser.add_argument("query")
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
    args = parser.parse_args()

    bm25_index = load_bm25_index(Path(args.bm25_index))
    bm25_results = bm25_search(bm25_index, args.query, args.bm25_k)
    chroma_results = chroma_search(
        args.query,
        args.chroma_dir,
        args.collection,
        args.provider,
        args.model,
        args.vector_k,
    )
    combined = combine_results(
        args.query,
        bm25_results,
        chroma_results,
        args.bm25_weight,
        args.vector_weight,
        args.top_k,
    )

    print(
        json.dumps(
            {
                "query": args.query,
                "bm25_results": len(bm25_results),
                "chroma_results": len(chroma_results),
                "results": combined,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
