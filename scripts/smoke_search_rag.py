"""Smoke-test retrieval from the local ChromaDB RAG collection."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, List

from ingest_rag_corpus import embed_texts, load_embedding_model


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--persist-dir", default="data/embeddings/chroma")
    parser.add_argument("--collection", default="pharmaceutical_knowledge")
    parser.add_argument("--provider", choices=["sentence-transformers", "openai"], default="sentence-transformers")
    parser.add_argument("--model", default="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    import chromadb

    if not Path(args.persist_dir).exists():
        raise SystemExit(f"Missing persist directory: {args.persist_dir}")
    client = chromadb.PersistentClient(path=args.persist_dir)
    collection = client.get_collection(args.collection)
    model = load_embedding_model(args.provider, args.model)
    query_embedding = embed_texts(model, args.provider, args.model, [args.query])[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=args.top_k)

    rows: List[dict[str, Any]] = []
    for index, doc_id in enumerate(results.get("ids", [[]])[0]):
        rows.append(
            {
                "rank": index + 1,
                "id": doc_id,
                "distance": results.get("distances", [[]])[0][index],
                "metadata": results.get("metadatas", [[]])[0][index],
                "document_preview": (results.get("documents", [[]])[0][index] or "")[:500],
            }
        )
    print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
