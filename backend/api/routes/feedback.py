"""Feedback endpoints for evaluation and future supervised datasets."""
from datetime import datetime
import json
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.utils import app_logger


router = APIRouter(prefix="/feedback", tags=["feedback"])


class FeedbackCreate(BaseModel):
    query: str = Field(..., min_length=1)
    response: str = Field(..., min_length=1)
    rating: float = Field(..., ge=-1, le=1)
    feedback_type: str = "thumbs"
    metadata: Optional[Dict] = None
    text_feedback: Optional[str] = None


class FeedbackResponse(BaseModel):
    id: str
    query: str
    response: str
    rating: float
    feedback_type: str
    metadata: Optional[Dict]
    text_feedback: Optional[str]
    timestamp: str
    status: str = "received"


class FeedbackStats(BaseModel):
    total_feedback: int
    positive_count: int
    negative_count: int
    neutral_count: int
    satisfaction_rate: float
    avg_rating: float
    feedback_by_type: Dict[str, int]


class FeedbackStorage:
    def __init__(self, storage_path: str = "data/feedback"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.feedback_file = self.storage_path / "feedback.jsonl"
        app_logger.info(f"Feedback storage initialized: {self.feedback_file}")

    def save_feedback(self, feedback: FeedbackCreate) -> FeedbackResponse:
        feedback_response = FeedbackResponse(
            id=f"fb_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            query=feedback.query,
            response=feedback.response,
            rating=feedback.rating,
            feedback_type=feedback.feedback_type,
            metadata=feedback.metadata,
            text_feedback=feedback.text_feedback,
            timestamp=datetime.now().isoformat(),
        )

        with self.feedback_file.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(feedback_response.model_dump(), ensure_ascii=False) + "\n")

        return feedback_response

    def get_all_feedback(self) -> List[FeedbackResponse]:
        if not self.feedback_file.exists():
            return []

        rows: List[FeedbackResponse] = []
        with self.feedback_file.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    rows.append(FeedbackResponse(**json.loads(line)))
        return rows

    def get_statistics(self) -> FeedbackStats:
        rows = self.get_all_feedback()
        if not rows:
            return FeedbackStats(
                total_feedback=0,
                positive_count=0,
                negative_count=0,
                neutral_count=0,
                satisfaction_rate=0.0,
                avg_rating=0.0,
                feedback_by_type={},
            )

        positive = sum(1 for row in rows if row.rating > 0.3)
        negative = sum(1 for row in rows if row.rating < -0.3)
        neutral = len(rows) - positive - negative
        feedback_by_type: Dict[str, int] = {}
        for row in rows:
            feedback_by_type[row.feedback_type] = feedback_by_type.get(row.feedback_type, 0) + 1

        return FeedbackStats(
            total_feedback=len(rows),
            positive_count=positive,
            negative_count=negative,
            neutral_count=neutral,
            satisfaction_rate=positive / len(rows),
            avg_rating=sum(row.rating for row in rows) / len(rows),
            feedback_by_type=feedback_by_type,
        )

    def export_for_training(self, output_file: str) -> int:
        rows = self.get_all_feedback()
        training_data = [
            {
                "query": row.query,
                "response": row.response,
                "rating": row.rating,
                "metadata": row.metadata or {},
            }
            for row in rows
        ]
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(training_data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return len(training_data)


feedback_storage = FeedbackStorage()


@router.post("/submit", response_model=FeedbackResponse)
async def submit_feedback(feedback: FeedbackCreate):
    try:
        return feedback_storage.save_feedback(feedback)
    except Exception as exc:
        app_logger.error(f"Failed to save feedback: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/statistics", response_model=FeedbackStats)
async def get_statistics():
    return feedback_storage.get_statistics()


@router.get("/list", response_model=List[FeedbackResponse])
async def list_feedback(limit: int = 100, offset: int = 0):
    return feedback_storage.get_all_feedback()[offset : offset + limit]


@router.post("/export")
async def export_feedback(output_file: str = "data/feedback/training_data.json"):
    count = feedback_storage.export_for_training(output_file)
    return {"status": "success", "output_file": output_file, "count": count}


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "storage_path": str(feedback_storage.storage_path),
        "feedback_count": len(feedback_storage.get_all_feedback()),
    }
