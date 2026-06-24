"""
Cac endpoint API cho tinh nang chat.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
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
        response = await text_service.process_message(
            message=request.message,
            session_id=request.session_id,
            conversation_id=request.conversation_id,
            context=request.context
        )
        
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
                    "duration_ms": 150, # Simplified
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


@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Xóa một session chat"""
    try:
        chat_history = get_chat_history_service()
        deleted = chat_history.clear_session(session_id)
        if deleted:
            return format_response(
                success=True,
                message="Xóa session thành công"
            )
        else:
            return format_response(
                success=False,
                message="Không tìm thấy session"
            )
    except Exception as e:
        app_logger.error(f"Lỗi khi xóa session: {e}")
        raise HTTPException(status_code=500, detail=str(e))
