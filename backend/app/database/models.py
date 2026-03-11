from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class Source(BaseModel):
    """Source citation model"""
    document_id: str
    document_name: str
    page: Optional[int] = None
    chunk_text: str
    relevance_score: float
    metadata: Dict[str, Any] = {}

class ChatMessage(BaseModel):
    """Chat message model"""
    id: str
    role: MessageRole
    content: str
    timestamp: datetime
    sources: Optional[List[Source]] = None
    tokens_used: Optional[int] = None

class ChatSession(BaseModel):
    """Chat session model"""
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[ChatMessage] = []
    document_ids: List[str] = []

class Document(BaseModel):
    """Document model"""
    id: str
    filename: str
    type: str  # pdf, url, txt, etc.
    size: int
    uploaded_at: datetime
    chunk_count: int
    metadata: Dict[str, Any] = {}

class UploadResponse(BaseModel):
    """Upload response model"""
    success: bool
    document_id: Optional[str] = None
    message: str
    chunk_count: Optional[int] = None

class ChatRequest(BaseModel):
    """Chat request model"""
    session_id: Optional[str] = None
    message: str
    document_ids: List[str] = []
    use_history: bool = True
    temperature: float = 0.7

class ChatResponse(BaseModel):
    """Chat response model"""
    session_id: str
    message: str
    sources: List[Source]
    tokens_used: int
    processing_time: float