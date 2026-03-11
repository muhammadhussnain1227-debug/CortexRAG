from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import List
import tempfile
import os
import logging
from ..database.models import UploadResponse
from ..services.document_processor import doc_processor
from ..services.rag_engine import rag_engine
from ..config import settings

router = APIRouter(prefix="/documents", tags=["documents"])
logger = logging.getLogger(__name__)

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    
    # Check file extension
    ext = file.filename.split('.')[-1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed: {settings.ALLOWED_EXTENSIONS}"
        )
    
    # Check file size
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    
    if size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE/1024/1024}MB"
        )
    
    try:
        # Save temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Process based on file type
        if ext == "pdf":
            chunks, metadatas = doc_processor.process_pdf(tmp_path, file.filename)
        else:
            # For text files
            with open(tmp_path, 'r', encoding='utf-8') as f:
                text = f.read()
            chunks, metadatas = doc_processor.process_text(text, file.filename)
        
        # Add to RAG engine
        await rag_engine.add_documents(chunks, metadatas)
        
        # Clean up
        os.unlink(tmp_path)
        
        return UploadResponse(
            success=True,
            document_id=file.filename,
            message="Document processed successfully",
            chunk_count=len(chunks)
        )
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/url")
async def upload_url(url: str = Form(...)):
    """Process a website URL"""
    try:
        chunks, metadatas = doc_processor.process_website(url)
        await rag_engine.add_documents(chunks, metadatas)
        
        return UploadResponse(
            success=True,
            document_id=url,
            message="Website processed successfully",
            chunk_count=len(chunks)
        )
    except Exception as e:
        logger.error(f"URL processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))