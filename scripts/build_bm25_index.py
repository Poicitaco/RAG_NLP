"""Build a pure-Python BM25 retrieval index for the RAG corpus.

This is the dependency-light baseline index. It is especially useful for drug
retrieval because drug names, active ingredients, registration numbers, and dose
units often need exact lexical matching.
"""
from __future__ import annotations

import argparse
import gzip
import json
import math
import pickle
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterator, List


DEFAULT_INPUTS = [
    "data/chunks/rag_corpus_parts",
    "data/chunks/trungtamthuoc_duocthu_chunks.jsonl",
    "data/chunks/ddinter_interaction_chunks.jsonl",
    "data/chunks/otc_condition_guardrail_chunks.jsonl",
]
TOKEN_RE = re.compile(r"[a-z0-9]+")


def iter_jsonl_paths(inputs: List[str]) -> Iterator[Path]:
    for input_name in inputs:
        path = Path(input_name)
        if path.is_dir():
            yield from sorted(path.glob("*.jsonl"))
        elif path.exists():
            yield path


def read_chunks(inputs: List[str], limit: int | None = None) -> Iterator[Dict[str, Any]]:
    count = 0
    for path in iter_jsonl_paths(inputs):
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                yield json.loads(line)
                count += 1
                if limit is not None and count >= limit:
                    return


def strip_accents(text: str) -> str:
    value = (text or "").replace("Đ", "D").replace("đ", "d")
    decomposed = unicodedata.normalize("NFD", value)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def tokenize(text: str) -> List[str]:
    normalized = strip_accents((text or "").lower())
    tokens = TOKEN_RE.findall(normalized)
    compact_tokens = []
    for token in tokens:
        compact_tokens.append(token)
        if any(ch.isdigit() for ch in token):
            compact_tokens.append(re.sub(r"[^a-z0-9]+", "", token))
    return [token for token in compact_tokens if len(token) >= 2]


def build_index(inputs: List[str], limit: int | None = None) -> Dict[str, Any]:
    docs = []
    postings: Dict[str, List[tuple[int, int]]] = defaultdict(list)
    doc_freq: Counter[str] = Counter()
    total_len = 0

    for doc_index, row in enumerate(read_chunks(inputs, limit)):
        text = str(row.get("document") or "")
        metadata = row.get("metadata") or {}
        tokens = tokenize(
            " ".join(
                [
                    text,
                    str(metadata.get("drug_name") or ""),
                    str(metadata.get("active_ingredient") or ""),
                    str(metadata.get("registration_number") or ""),
                    str(metadata.get("title") or ""),
                ]
            )
        )
        counts = Counter(tokens)
        doc_len = sum(counts.values())
        total_len += doc_len
        docs.append(
            {
                "id": row.get("id") or f"doc:{doc_index}",
                "document": text,
                "metadata": metadata,
                "length": doc_len,
            }
        )
        for token, tf in counts.items():
            postings[token].append((doc_index, tf))
            doc_freq[token] += 1
        if (doc_index + 1) % 10000 == 0:
            print(f"indexed {doc_index + 1} chunks")

    return {
        "version": 1,
        "type": "bm25",
        "docs": docs,
        "postings": dict(postings),
        "doc_freq": dict(doc_freq),
        "avg_doc_len": total_len / len(docs) if docs else 0,
        "doc_count": len(docs),
        "inputs": inputs,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="*", default=DEFAULT_INPUTS)
    parser.add_argument("--output", default="data/embeddings/bm25/rag_bm25.pkl.gz")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    index = build_index(args.inputs, args.limit)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(output, "wb") as handle:
        pickle.dump(index, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print(
        json.dumps(
            {
                "output": args.output,
                "doc_count": index["doc_count"],
                "vocab_size": len(index["postings"]),
                "avg_doc_len": round(index["avg_doc_len"], 2),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
