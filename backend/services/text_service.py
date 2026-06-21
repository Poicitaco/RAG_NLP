"""
Text processing service - Dịch vụ xử lý văn bản
"""
from typing import Dict, Any, Optional
from backend.models import ChatResponse
from backend.services.conversation_context_service import ConversationContextService
from backend.services.safe_rag_service import get_safe_rag_service
from backend.utils import app_logger, sanitize_input
import time


class TextService:
    """Dịch vụ xử lý hội thoại dựa trên văn bản"""
    
    def __init__(self):
        """Khởi tạo text service"""
        self.safe_rag = get_safe_rag_service()
        self.conversation_context = ConversationContextService()
        app_logger.info("Initialized text service")
    
    async def process_message(
        self,
        message: str,
        session_id: str,
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> ChatResponse:
        """
        Xử lý tin nhắn văn bản
        
        Args:
            message: Tin nhắn của người dùng
            session_id: ID phiên
            conversation_id: ID hội thoại tùy chọn
            context: Dữ liệu context tùy chọn
            
        Returns:
            Phản hồi chat
        """
        start_time = time.time()
        
        try:
            # Làm sạch input
            clean_message = sanitize_input(message)
            
            if not clean_message:
                return ChatResponse(
                    message="Vui lòng nhập câu hỏi của bạn.",
                    conversation_id=conversation_id or session_id,
                    agent_type="general",
                    confidence=0.0
                )
            
            session_context = self.conversation_context.build_context(
                session_id=session_id,
                message=clean_message,
                incoming_context=context,
            )
            processing_message = self.conversation_context.message_for_processing(
                session_id=session_id,
                message=clean_message,
                context=session_context,
            )

            response = await self.safe_rag.answer(
                message=processing_message,
                session_id=session_id,
                conversation_id=conversation_id,
                context=session_context,
            )
            if session_context.get("resume_pending_question"):
                response.metadata["resumed_from_pending_question"] = True
                response.metadata["resumed_from_user_message"] = clean_message
            self.conversation_context.update_from_response(
                session_id=session_id,
                user_message=processing_message,
                response_metadata=response.metadata,
            )
            
            duration = time.time() - start_time
            app_logger.info(f"Processed text message in {duration:.3f}s")
            
            return response
            
        except Exception as e:
            app_logger.error(f"Lỗi khi xử lý tin nhắn văn bản: {e}")
            raise


# Global instance
_text_service: Optional[TextService] = None


def get_text_service() -> TextService:
    """Lấy hoặc tạo text service toàn cục"""
    global _text_service
    if _text_service is None:
        _text_service = TextService()
    return _text_service
