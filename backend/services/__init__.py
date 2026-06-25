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
    if name == "llm_patient_context_extractor":
        from . import llm_patient_context_extractor
        return llm_patient_context_extractor
    if name == "llm_answer_service":
        from . import llm_answer_service
        return llm_answer_service
    if name == "llm_intent_planner_service":
        from . import llm_intent_planner_service
        return llm_intent_planner_service
    if name == "query_ambiguity_service":
        from . import query_ambiguity_service
        return query_ambiguity_service
    raise AttributeError(name)


__all__ = ["SafeRagService", "TextService", "ChatHistoryService", "get_safe_rag_service", "get_text_service", "get_chat_history_service"]
