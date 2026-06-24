"""
Cac schema Pydantic dung cho API duoc pham RAG.
"""
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class AgentType(str, Enum):
    GENERAL = "general"
    DRUG_INFO = "drug_info"
    INTERACTION_CHECK = "interaction_check"
    DOSAGE_ADVISOR = "dosage_advisor"
    SAFETY_MONITOR = "safety_monitor"


class InteractionSeverity(str, Enum):
    NONE = "none"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class Citation(BaseModel):
    id: str
    source: str = "Unknown"
    title: Optional[str] = None
    url: Optional[str] = None
    page: Optional[Union[int, str]] = None
    section: Optional[str] = None
    updated_at: Optional[str] = None
    similarity: Optional[float] = None


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    session_id: str = Field(default="default")
    conversation_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    agent_type: AgentType = AgentType.GENERAL
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    sources: List[Union[str, Citation, Dict[str, Any]]] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DrugQuery(BaseModel):
    query: str = Field(..., min_length=1)
    limit: int = Field(default=10, ge=1, le=50)


class DrugResponse(BaseModel):
    drug_id: Optional[str] = None
    name: str
    active_ingredient: Optional[str] = None
    dosage_form: Optional[str] = None
    source: Optional[str] = None


class DrugInteractionCheck(BaseModel):
    drugs: List[str] = Field(..., min_length=2, max_length=10)
    patient_context: Optional[Dict[str, Any]] = None


class DrugInteractionResponse(BaseModel):
    has_interactions: bool
    severity: InteractionSeverity = InteractionSeverity.NONE
    interactions: List[Dict[str, Any]] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class DosageRequest(BaseModel):
    drug_name: str = Field(..., min_length=1)
    age: Optional[int] = Field(default=None, ge=0, le=120)
    weight: Optional[float] = Field(default=None, gt=0, le=300)
    prescription_text: Optional[str] = None


class DosageResponse(BaseModel):
    drug_name: str
    recommended_dosage: str
    frequency: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)
    sources: List[Citation] = Field(default_factory=list)


class DrugRecognitionRequest(BaseModel):
    image_data: str = Field(..., min_length=1)
    image_format: str = "jpg"


class DrugRecognitionResponse(BaseModel):
    drug_name: Optional[str] = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    message: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)


class VoiceInputRequest(BaseModel):
    audio_data: str = Field(..., min_length=1)
    audio_format: str = "wav"
    session_id: str = "default"
    language: str = "vi"


class VoiceInputResponse(BaseModel):
    transcript: str = ""
    response: Optional[ChatResponse] = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)
