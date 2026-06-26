"""Ingest prepared RAG JSONL chunks into a persistent ChromaDB collection."""
from __future__ import annotations

import argparse
import functools
import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List

from dotenv import load_dotenv

load_dotenv()

try:
    from backend.config import settings
except Exception:
    settings = None


DEFAULT_INPUTS = [
    "data/chunks/rag_corpus_parts",
]
DEFAULT_COLLECTION = "pharmaceutical_local_bge_1024"
DEFAULT_PROVIDER = "sentence-transformers"
DEFAULT_MODEL = "BAAI/bge-m3"
KAGGLE_API_URL = (getattr(settings, "KAGGLE_API_URL", None) or os.getenv("KAGGLE_API_URL", "")).rstrip("/")


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


@functools.lru_cache(maxsize=1)
def load_embedding_model(provider: str, model: str):
    if provider == "sentence-transformers":
        endpoint = f"{KAGGLE_API_URL}/embed" if KAGGLE_API_URL else ""
        return {"provider": provider, "model": model, "endpoint": endpoint}
    if provider == "openai":
        from openai import OpenAI

        return OpenAI()
    raise ValueError(f"Unsupported provider: {provider}")


@functools.lru_cache(maxsize=1)
def load_local_sentence_transformer(model_name: str):
    from sentence_transformers import SentenceTransformer

    print(f"Loading local CPU embedding model: {model_name}")
    return SentenceTransformer(model_name, device="cpu")


def embed_texts_local_cpu(model_name: str, texts: List[str]) -> List[List[float]]:
    local_model = load_local_sentence_transformer(model_name)
    embeddings = local_model.encode(
        texts,
        batch_size=32,
        show_progress_bar=False,
        normalize_embeddings=True,
    )
    return embeddings.tolist() if hasattr(embeddings, "tolist") else embeddings


def _reload_kaggle_url() -> str:
    """Reload KAGGLE_API_URL từ .env để dùng URL mới khi cập nhật."""
    load_dotenv(override=True)
    return os.getenv("KAGGLE_API_URL", "").rstrip("/")


def embed_texts(model: Any, provider: str, model_name: str, texts: List[str]) -> List[List[float]]:
    if provider == "sentence-transformers":
        kaggle_url = _reload_kaggle_url()
        if not kaggle_url:
            print("KAGGLE_API_URL chua duoc cau hinh trong .env; fallback local CPU.")
            return embed_texts_local_cpu(model_name, texts)

        import time
        max_retries = 5
        for attempt in range(max_retries):
            kaggle_url = _reload_kaggle_url()  # reload mỗi lần retry để lấy URL mới
            endpoint = f"{kaggle_url}/embed"
            payload = json.dumps({"texts": texts}, ensure_ascii=False).encode("utf-8")
            request = urllib.request.Request(
                endpoint,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            try:
                with urllib.request.urlopen(request, timeout=180) as response:
                    data = json.loads(response.read().decode("utf-8"))
                embeddings = data.get("embeddings")
                if not isinstance(embeddings, list):
                    raise RuntimeError("Kaggle embedding API response is missing embeddings")
                if len(embeddings) != len(texts):
                    raise RuntimeError(
                        f"Kaggle embedding API returned {len(embeddings)} vectors for {len(texts)} texts"
                    )
                return embeddings
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
                print(f"[Attempt {attempt+1}/{max_retries}] Lỗi API Kaggle: {exc}")
                if attempt < max_retries - 1:
                    print("Đợi 100s... Cập nhật KAGGLE_API_URL trong .env nếu cần, script sẽ tự đọc lại.")
                    time.sleep(100)
                else:
                    print("Hết retry. Fallback local CPU cho batch này.")
            except RuntimeError as exc:
                print(f"Lỗi phản hồi API Kaggle: {exc}")
                break

        print("Fallback: dùng sentence-transformers local CPU để nhúng batch hiện tại.")
        return embed_texts_local_cpu(model_name, texts)
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


def existing_ids(collection: Any) -> set[str]:
    ids = collection.get(include=[]).get("ids") or []
    return {str(row_id) for row_id in ids}


def iter_missing_chunks(
    rows: Iterable[Dict[str, Any]],
    seen_ids: set[str],
    stats: Dict[str, int],
) -> Iterator[Dict[str, Any]]:
    for row in rows:
        chunk_id = str(row.get("id") or "")
        if not chunk_id:
            continue
        if chunk_id in seen_ids:
            stats["skipped_existing"] = stats.get("skipped_existing", 0) + 1
            print(f"Skipping existing chunk... {chunk_id}")
            continue
        yield row
        seen_ids.add(chunk_id)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="*", default=DEFAULT_INPUTS)
    parser.add_argument("--persist-dir", default="data/embeddings/chroma")
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--provider", choices=["sentence-transformers", "openai"], default=DEFAULT_PROVIDER)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--reset", action="store_true")
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Deprecated: existing chunks are skipped automatically.",
    )
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
    seen_ids = existing_ids(collection)
    if seen_ids:
        print(f"Found {len(seen_ids)} existing chunks in collection; skipping them automatically.")

    total = 0
    stats = {"skipped_existing": 0}
    rows = iter_missing_chunks(read_chunks(args.inputs, args.limit), seen_ids, stats)
    for batch in batched(rows, args.batch_size):
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
                "skipped_existing": stats["skipped_existing"],
                "collection_count": collection.count(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
