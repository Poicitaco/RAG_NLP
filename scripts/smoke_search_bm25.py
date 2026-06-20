"""Search the local BM25 RAG index."""
from __future__ import annotations

import argparse
import gzip
import json
import math
import pickle
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List

from build_bm25_index import tokenize


def search(index: Dict[str, Any], query: str, top_k: int = 5, k1: float = 1.5, b: float = 0.75) -> List[Dict[str, Any]]:
    query_terms = Counter(tokenize(query))
    scores: Dict[int, float] = defaultdict(float)
    doc_count = index["doc_count"]
    avgdl = index["avg_doc_len"] or 1.0
    postings = index["postings"]
    doc_freq = index["doc_freq"]
    docs = index["docs"]

    for term, qf in query_terms.items():
        if term not in postings:
            continue
        df = doc_freq.get(term, 0)
        idf = math.log(1 + (doc_count - df + 0.5) / (df + 0.5))
        for doc_index, tf in postings[term]:
            doc_len = docs[doc_index].get("length") or avgdl
            denom = tf + k1 * (1 - b + b * doc_len / avgdl)
            scores[doc_index] += qf * idf * (tf * (k1 + 1) / denom)

    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:top_k]
    results = []
    for rank, (doc_index, score) in enumerate(ranked, 1):
        doc = docs[doc_index]
        results.append(
            {
                "rank": rank,
                "score": round(score, 4),
                "id": doc["id"],
                "metadata": doc["metadata"],
                "document_preview": doc["document"][:700],
            }
        )
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--index", default="data/embeddings/bm25/rag_bm25.pkl.gz")
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    path = Path(args.index)
    if not path.exists():
        raise SystemExit(f"Missing BM25 index: {path}")
    with gzip.open(path, "rb") as handle:
        index = pickle.load(handle)
    print(json.dumps(search(index, args.query, args.top_k), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
