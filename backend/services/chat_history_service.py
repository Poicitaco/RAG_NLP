"""Service luu tru va truy xuat lich su chat su dung file JSON don gian."""
import json
import os
import threading
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
HISTORY_FILE = DATA_DIR / "chat_history.json"

class ChatHistoryService:
    def __init__(self, file_path: Path = HISTORY_FILE):
        self.file_path = file_path
        self._lock = threading.Lock()
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Kiem tra va tao file JSON neu chua ton tai."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def _load_history(self) -> Dict[str, List[Dict[str, Any]]]:
        """Doc lich su tu file."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_history(self, history: Dict[str, List[Dict[str, Any]]]) -> None:
        """Ghi lich su vao file."""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    def get_history(self, session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Lay lich su chat cua mot session_id."""
        history = self._load_history()
        session_history = history.get(session_id, [])
        # Tra ve cac tin nhan moi nhat (cat theo limit)
        return session_history[-limit:] if limit > 0 else session_history

    def add_message(self, session_id: str, role: str, content: str, metadata: Dict[str, Any] = None) -> None:
        """Them mot tin nhan vao lich su cua session_id."""
        with self._lock:
            history = self._load_history()
            if session_id not in history:
                history[session_id] = []
            
            message = {
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            history[session_id].append(message)
            # Giới hạn mỗi session tối đa 100 messages (50 turns)
            MAX_MESSAGES_PER_SESSION = 100
            if len(history[session_id]) > MAX_MESSAGES_PER_SESSION:
                history[session_id] = history[session_id][-MAX_MESSAGES_PER_SESSION:]
            self._save_history(history)

    def clear_session(self, session_id: str) -> bool:
        """Xoa lich su cua mot session_id."""
        with self._lock:
            history = self._load_history()
            if session_id in history:
                del history[session_id]
                self._save_history(history)
                return True
            return False

# Singleton instance
_chat_history_service = None

def get_chat_history_service() -> ChatHistoryService:
    global _chat_history_service
    if _chat_history_service is None:
        _chat_history_service = ChatHistoryService()
    return _chat_history_service
