"""Service exports for the focused RAG backend."""


def get_text_service():
    from .text_service import get_text_service as factory

    return factory()


def get_safe_rag_service():
    from .safe_rag_service import get_safe_rag_service as factory

    return factory()


def get_chat_history_service():
    from .chat_history_service import get_chat_history_service as factory
    return factory()


def __getattr__(name):
    if name == "TextService":
        from .text_service import TextService
        return TextService
    if name == "SafeRagService":
        from .safe_rag_service import SafeRagService
        return SafeRagService
    if name == "ChatHistoryService":
        from .chat_history_service import ChatHistoryService
        return ChatHistoryService
    raise AttributeError(name)


__all__ = ["SafeRagService", "TextService", "ChatHistoryService", "get_safe_rag_service", "get_text_service", "get_chat_history_service"]
