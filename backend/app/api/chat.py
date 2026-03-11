from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
import logging
from ..database.models import ChatRequest, ChatResponse
from ..services.rag_engine import rag_engine

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process chat message"""
    try:
        response = await rag_engine.process_query(
            query=request.message,
            session_id=request.session_id,
            document_ids=request.document_ids,
            use_history=request.use_history,
            temperature=request.temperature
        )
        return response
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat response"""
    # Implement streaming if needed
    pass