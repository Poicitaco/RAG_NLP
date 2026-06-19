"""Service exports for the focused RAG backend."""


def get_text_service():
    from .text_service import get_text_service as factory

    return factory()


def __getattr__(name):
    if name == "TextService":
        from .text_service import TextService

        return TextService
    raise AttributeError(name)


__all__ = ["TextService", "get_text_service"]
