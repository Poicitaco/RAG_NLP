"""
Cac endpoint API cho tinh nang chat.
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from typing import Dict, Any, Optional
import json
from backend.models import ChatRequest, ChatResponse
from backend.services import get_text_service, get_chat_history_service
from backend.utils import app_logger, format_response

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat với trợ lý AI
    
    Xử lý tin nhắn người dùng và trả về phản hồi AI
    """
    try:
        chat_history = get_chat_history_service()
        # Luu tin nhan cua user
        chat_history.add_message(
            session_id=request.session_id,
            role="user",
            content=request.message,
            metadata={"context": request.context} if request.context else {}
        )
        
        text_service = get_text_service()
        import time as _time
        _start = _time.perf_counter()
        response = await text_service.process_message(
            message=request.message,
            session_id=request.session_id,
            conversation_id=request.conversation_id,
            context=request.context
        )
        _duration_ms = round((_time.perf_counter() - _start) * 1000)
        
        # Luu tin nhan cua bot
        chat_history.add_message(
            session_id=request.session_id,
            role="assistant",
            content=response.message,
            metadata={
                "agent_type": response.agent_type,
                "confidence": response.confidence,
                "warnings": response.warnings,
                "suggestions": response.suggestions,
                "sources": [s.model_dump() for s in response.sources] if response.sources else []
            }
        )
        
        # Ghi log co cau truc cho /metrics
        try:
            import json, time, os
            os.makedirs("logs", exist_ok=True)
            with open("logs/structured_requests.jsonl", "a", encoding="utf-8") as f:
                log_entry = {
                    "ts": time.time(),
                    "session_id": request.session_id,
                    "intent": request.context.get("intent", "unknown") if request.context else "unknown",
                    "action": response.agent_type,
                    "confidence": response.confidence,
                    "duration_ms": _duration_ms,
                    "llm_used": response.agent_type != "rule_based",
                    "context": request.context
                }
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception as log_e:
            app_logger.warning(f"Failed to write structured log: {log_e}")
            
        return response
    
    except Exception as e:
        app_logger.error(f"Lỗi trong chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat — Server-Sent Events.
    Dùng Groq stream=True nếu available, fallback word-split nếu không.
    """
    async def event_generator():
        try:
            text_service = get_text_service()
            response = await text_service.process_message(
                message=request.message,
                session_id=request.session_id,
                conversation_id=request.conversation_id,
                context=request.context,
            )

            # Dùng Groq real streaming qua stream_rewrite()
            llm_svc = text_service.safe_rag.llm_answer
            patient_ctx = (request.context or {}).get("patient_context")
            full_text = ""
            async for chunk in llm_svc.stream_rewrite(
                question=request.message,
                deterministic_answer=response.message,
                graph_safety={},
                snippets=[],
                citations=response.sources or [],
                patient_context=patient_ctx,
            ):
                full_text += chunk
                yield f"data: {json.dumps({'type': 'token', 'data': chunk}, ensure_ascii=False)}\n\n"

            final = {
                "type": "done",
                "data": {
                    "message": full_text or response.message,
                    "sources": [s.model_dump() for s in response.sources] if response.sources else [],
                    "warnings": response.warnings,
                    "suggestions": response.suggestions,
                    "confidence": response.confidence,
                    "agent_type": response.agent_type,
                    "metadata": response.metadata,
                },
            }
            yield f"data: {json.dumps(final, ensure_ascii=False)}\n\n"

            try:
                chat_history = get_chat_history_service()
                chat_history.add_message(request.session_id, "user", request.message)
                chat_history.add_message(request.session_id, "assistant", full_text or response.message,
                                         {"confidence": response.confidence, "agent_type": response.agent_type})
            except Exception:
                pass

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'data': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("/history/{session_id}")
async def get_chat_history(session_id: str, limit: int = 50):
    """Lấy lịch sử chat cho một session"""
    try:
        chat_history = get_chat_history_service()
        history = chat_history.get_history(session_id, limit=limit)
        return format_response(
            success=True,
            data=history,
            message="Lấy lịch sử chat thành công"
        )
    except Exception as e:
        app_logger.error(f"Lỗi khi lấy lịch sử chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """Streaming SSE endpoint — trả về text dần dần như ChatGPT"""
    async def event_generator():
        try:
            text_service = get_text_service()
            import time as _time
            _start = _time.perf_counter()
            response = await text_service.process_message(
                message=request.message,
                session_id=request.session_id,
                conversation_id=request.conversation_id,
                context=request.context,
            )
            _duration_ms = round((_time.perf_counter() - _start) * 1000)

            # Luu lich su
            chat_history = get_chat_history_service()
            chat_history.add_message(session_id=request.session_id, role="user", content=request.message)
            chat_history.add_message(
                session_id=request.session_id, role="assistant", content=response.message,
                metadata={"agent_type": response.agent_type, "confidence": response.confidence}
            )

            # Dùng Groq streaming nếu có, fallback word-split nếu không
            llm_svc = text_service._safe_rag.llm_answer
            full_text = ""
            async for chunk in llm_svc.stream_rewrite(
                question=request.message,
                deterministic_answer=response.message,
                graph_safety={},
                snippets=[],
                citations=response.sources or [],
                patient_context=(request.context or {}).get("patient_context"),
            ):
                full_text += chunk
                yield f"data: {json.dumps({'type': 'token', 'data': chunk}, ensure_ascii=False)}\n\n"

            # Gui metadata cuoi cung
            final = {
                "type": "done",
                "data": {
                    "message": full_text or response.message,
                    "sources": [s.model_dump() for s in response.sources] if response.sources else [],
                    "warnings": response.warnings,
                    "suggestions": response.suggestions,
                    "confidence": response.confidence,
                    "agent_type": response.agent_type,
                    "metadata": response.metadata,
                },
            }
            yield f"data: {json.dumps(final, ensure_ascii=False)}\n\n"

            # Structured log
            try:
                import os
                import time
                os.makedirs("logs", exist_ok=True)
                with open("logs/structured_requests.jsonl", "a", encoding="utf-8") as f:
                    log_entry = {
                        "ts": time.time(), "session_id": request.session_id,
                        "action": response.agent_type, "confidence": response.confidence,
                        "duration_ms": _duration_ms, "streaming": True,
                    }
                    f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
            except Exception:
                pass

        except Exception as e:
            app_logger.error(f"Lỗi streaming: {e}")
            yield f"data: {json.dumps({'type': 'error', 'data': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Xóa một session chat"""
    try:
        chat_history = get_chat_history_service()
        deleted = chat_history.clear_session(session_id)
        # Cũng clear conversation context state (persist file)
        try:
            from backend.services.safe_rag_service import SafeRagService
            from backend.services import get_text_service
            svc = get_text_service()
            if hasattr(svc, '_conversation') and hasattr(svc._conversation, '_states'):
                svc._conversation._states.pop(session_id, None)
                svc._conversation._save_states()
        except Exception:
            pass
        if deleted:
            return format_response(success=True, message="Xóa session thành công")
        else:
            return format_response(success=False, message="Không tìm thấy session")
    except Exception as e:
        app_logger.error(f"Lỗi khi xóa session: {e}")
        raise HTTPException(status_code=500, detail=str(e))
