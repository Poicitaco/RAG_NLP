"""Ingest prepared RAG JSONL chunks into a persistent ChromaDB collection."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List


DEFAULT_INPUTS = [
    "data/chunks/rag_corpus_parts",
]


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


def flatten_metadata(metadata: Dict[str, Any]) -> Dict[str, str | int | float | bool]:
    flat: Dict[str, str | int | float | bool] = {}
    for key, value in (metadata or {}).items():
        if value is None:
            flat[key] = ""
        elif isinstance(value, (str, int, float, bool)):
            flat[key] = value
        else:
            flat[key] = json.dumps(value, ensure_ascii=False)
    return flat


def load_embedding_model(provider: str, model: str):
    if provider == "sentence-transformers":
        from sentence_transformers import SentenceTransformer

        return SentenceTransformer(model)
    if provider == "openai":
        from openai import OpenAI

        return OpenAI()
    raise ValueError(f"Unsupported provider: {provider}")


def embed_texts(model: Any, provider: str, model_name: str, texts: List[str]) -> List[List[float]]:
    if provider == "sentence-transformers":
        vectors = model.encode(texts, batch_size=len(texts), normalize_embeddings=True, show_progress_bar=False)
        return [vector.tolist() for vector in vectors]
    if provider == "openai":
        response = model.embeddings.create(model=model_name, input=texts)
        return [item.embedding for item in response.data]
    raise ValueError(f"Unsupported provider: {provider}")


def batched(rows: Iterable[Dict[str, Any]], batch_size: int) -> Iterator[List[Dict[str, Any]]]:
    batch: List[Dict[str, Any]] = []
    for row in rows:
        batch.append(row)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="*", default=DEFAULT_INPUTS)
    parser.add_argument("--persist-dir", default="data/embeddings/chroma")
    parser.add_argument("--collection", default="pharmaceutical_knowledge")
    parser.add_argument("--provider", choices=["sentence-transformers", "openai"], default="sentence-transformers")
    parser.add_argument("--model", default="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()

    import chromadb

    Path(args.persist_dir).mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=args.persist_dir)
    if args.reset:
        try:
            client.delete_collection(args.collection)
            print(f"deleted existing collection: {args.collection}")
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name=args.collection,
        metadata={
            "description": "Vietnamese pharmaceutical RAG corpus",
            "embedding_provider": args.provider,
            "embedding_model": args.model,
        },
    )
    model = load_embedding_model(args.provider, args.model)

    total = 0
    for batch in batched(read_chunks(args.inputs, args.limit), args.batch_size):
        ids = [str(row.get("id")) for row in batch]
        docs = [str(row.get("document") or "") for row in batch]
        metadatas = [flatten_metadata(row.get("metadata") or {}) for row in batch]
        embeddings = embed_texts(model, args.provider, args.model, docs)
        collection.upsert(ids=ids, documents=docs, metadatas=metadatas, embeddings=embeddings)
        total += len(batch)
        print(f"ingested {total} chunks")

    print(
        json.dumps(
            {
                "collection": args.collection,
                "persist_dir": args.persist_dir,
                "provider": args.provider,
                "model": args.model,
                "ingested": total,
                "collection_count": collection.count(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
