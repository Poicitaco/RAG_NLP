"""
Lazy RAG exports.

Importing backend modules should not require OpenAI, ChromaDB or LangChain until
retrieval/generation is actually used.
"""


def get_embedding_service():
    from .embeddings import get_embedding_service as factory

    return factory()


async def generate_embedding(text: str):
    from .embeddings import generate_embedding as factory

    return await factory(text)


async def generate_embeddings(texts):
    from .embeddings import generate_embeddings as factory

    return await factory(texts)


def get_vector_store(*args, **kwargs):
    from .vector_store import get_vector_store as factory

    return factory(*args, **kwargs)


def get_default_vector_store():
    from .vector_store import get_default_vector_store as factory

    return factory()


def get_retriever():
    from .retriever import get_retriever as factory

    return factory()


def get_generator():
    from .generator import get_generator as factory

    return factory()


def __getattr__(name):
    if name in {"EmbeddingService", "HuggingFaceEmbeddings"}:
        from . import embeddings

        return getattr(embeddings, name)
    if name in {"VectorStore", "ChromaVectorStore", "FAISSVectorStore"}:
        from . import vector_store

        return getattr(vector_store, name)
    if name == "Retriever":
        from .retriever import Retriever

        return Retriever
    if name == "ResponseGenerator":
        from .generator import ResponseGenerator

        return ResponseGenerator
    raise AttributeError(name)


__all__ = [
    "EmbeddingService",
    "get_embedding_service",
    "generate_embedding",
    "generate_embeddings",
    "VectorStore",
    "ChromaVectorStore",
    "get_vector_store",
    "get_default_vector_store",
    "Retriever",
    "get_retriever",
    "ResponseGenerator",
    "get_generator",
]
