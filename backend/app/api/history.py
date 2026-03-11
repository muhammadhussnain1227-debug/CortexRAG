from fastapi import APIRouter, HTTPException
from typing import List
from ..database.chat_history import chat_history
from ..database.models import ChatSession, ChatMessage

router = APIRouter(prefix="/history", tags=["history"])

@router.get("/sessions", response_model=List[ChatSession])
async def get_sessions():
    """Get all chat sessions"""
    return chat_history.get_all_sessions()

@router.get("/sessions/{session_id}", response_model=ChatSession)
async def get_session(session_id: str):
    """Get specific session"""
    session = chat_history.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    chat_history.delete_session(session_id)
    return {"message": "Session deleted"}

@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessage])
async def get_session_messages(session_id: str, limit: int = 50):
    """Get messages from session"""
    return chat_history.get_session_messages(session_id, limit)