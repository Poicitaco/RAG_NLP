"""
Tiện ích ghi log cho ứng dụng
"""
import sys
import logging
from pathlib import Path
from typing import Optional

try:
    from loguru import logger
except ModuleNotFoundError:
    logger = logging.getLogger("PharmaAI")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    def _noop(*args, **kwargs):
        return None

    def _bind(**kwargs):
        return logger

    logger.remove = _noop
    logger.add = _noop
    logger.bind = _bind


class LoggerSetup:
    """Thiết lập và cấu hình logger ứng dụng"""
    
    def __init__(self, log_level: str = "INFO", log_dir: str = "./logs"):
        self.log_level = log_level
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._setup_logger()
    
    def _setup_logger(self) -> None:
        """Cấu hình logger với file và console handlers"""
        # Xoa handler mac dinh
        logger.remove()
        
        # Handler console co mau sac
        logger.add(
            sys.stdout,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{message}</level>"
            ),
            level=self.log_level,
            colorize=True,
        )
        
        # File handler cho tất cả logs
        logger.add(
            self.log_dir / "app.log",
            format=(
                "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
                "{name}:{function}:{line} | {message}"
            ),
            level="DEBUG",
            rotation="10 MB",
            retention="30 days",
            compression="zip",
        )
        
        # File handler chỉ cho errors
        logger.add(
            self.log_dir / "error.log",
            format=(
                "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
                "{name}:{function}:{line} | {message}"
            ),
            level="ERROR",
            rotation="10 MB",
            retention="90 days",
            compression="zip",
        )
        
        # Handler file chi ghi log API request
        logger.add(
            self.log_dir / "api.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {message}",
            level="INFO",
            rotation="10 MB",
            retention="30 days",
            filter=lambda record: "API" in record["extra"].get("type", ""),
        )
    
    @staticmethod
    def get_logger(name: Optional[str] = None):
        """Lấy logger instance"""
        if name:
            return logger.bind(name=name)
        return logger


# Khoi tao logger toan cuc
log_setup = LoggerSetup()
app_logger = log_setup.get_logger("PharmaAI")


def log_api_request(
    method: str,
    path: str,
    status_code: int,
    duration: float,
    user_id: Optional[str] = None
) -> None:
    """Ghi log chi tiết API request"""
    logger.bind(type="API").info(
        f"{method} {path} - Status: {status_code} - "
        f"Duration: {duration:.3f}s - User: {user_id or 'anonymous'}"
    )


def log_hanh_dong_agent(ten_agent: str, hanh_dong: str, chi_tiet: str = "") -> None:
    """Ghi log hanh dong cua agent."""
    logger.bind(type="AGENT").info(
        f"Agent: {ten_agent} | Hanh dong: {hanh_dong} | {chi_tiet}"
    )


def log_truy_van_rag(truy_van: str, so_ket_qua: int, thoi_gian: float) -> None:
    """Ghi log chi tiet truy van RAG."""
    logger.bind(type="RAG").info(
        f"Truy van: {truy_van[:100]}... | Ket qua: {so_ket_qua} | Thoi gian: {thoi_gian:.3f}s"
    )


def log_agent_action(agent_name: str, action: str, details: str = "") -> None:
    """Backward-compatible alias for older imports."""
    log_hanh_dong_agent(agent_name, action, details)


def log_rag_query(query: str, result_count: int, duration: float) -> None:
    """Backward-compatible alias for older imports."""
    log_truy_van_rag(query, result_count, duration)
