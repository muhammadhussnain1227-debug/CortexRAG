from typing import List, Optional
import time
from datetime import datetime
import uuid
from ..database.vector_store import vector_store
from ..database.chat_history import chat_history
from ..database.models import ChatMessage, MessageRole, Source, ChatResponse
from ..services.embedding_service import embedding_service
from ..services.llm_service import llm_service
import logging

logger = logging.getLogger(__name__)

class RAGEngine:
    """Main RAG orchestration engine"""
    
    def __init__(self):
        self.vector_store = vector_store
        self.chat_history = chat_history
        self.embedding_service = embedding_service
        self.llm_service = llm_service
    
    async def process_query(self,
                           query: str,
                           session_id: Optional[str] = None,
                           document_ids: List[str] = [],
                           use_history: bool = True,
                           temperature: float = 0.7) -> ChatResponse:
        """Process user query through RAG pipeline"""
        
        start_time = time.time()
        
        # Get or create session
        if not session_id:
            session = self.chat_history.create_session()
            session_id = session.id
        else:
            session = self.chat_history.get_session(session_id)
            if not session:
                session = self.chat_history.create_session()
                session_id = session.id
        
        # Store user message
        user_message = ChatMessage(
            id=str(uuid.uuid4()),
            role=MessageRole.USER,
            content=query,
            timestamp=datetime.now()
        )
        self.chat_history.add_message(session_id, user_message)
        
        # Get chat history if needed
        history = []
        if use_history:
            history = [
                {"role": msg.role.value, "content": msg.content}
                for msg in session.messages[-5:]  # Last 5 messages
            ]
        
        # Create query embedding
        query_embedding = self.embedding_service.create_embedding(query)
        
        # Search relevant documents
        filter_criteria = None
        if document_ids:
            filter_criteria = {"document_id": {"$in": document_ids}}
        
        # Search in vector store
        search_results = self.vector_store.similarity_search(
            collection_name="documents",
            query_embedding=query_embedding,
            n_results=5,
            filter_criteria=filter_criteria
        )
        
        # Create source objects
        sources = []
        for result in search_results:
            source = Source(
                document_id=result['metadata']['document_id'],
                document_name=result['metadata']['document_name'],
                page=result['metadata'].get('page'),
                chunk_text=result['document'][:200] + "...",  # Preview
                relevance_score=1 - result['distance'] if result['distance'] else 0.5,
                metadata=result['metadata']
            )
            sources.append(source)
        
        # Generate response
        llm_response = self.llm_service.generate_response(
            query=query,
            context_chunks=search_results,
            chat_history=history,
            temperature=temperature
        )
        
        # Store assistant message
        assistant_message = ChatMessage(
            id=str(uuid.uuid4()),
            role=MessageRole.ASSISTANT,
            content=llm_response['content'],
            timestamp=datetime.now(),
            sources=sources,
            tokens_used=llm_response['tokens_used']
        )
        self.chat_history.add_message(session_id, assistant_message)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Prepare response
        response = ChatResponse(
            session_id=session_id,
            message=llm_response['content'],
            sources=sources,
            tokens_used=llm_response['tokens_used'],
            processing_time=processing_time
        )
        
        logger.info(f"Processed query in {processing_time:.2f}s, tokens: {llm_response['tokens_used']}")
        return response
    
    async def add_documents(self, chunks: List[str], metadatas: List[Dict]) -> List[str]:
        """Add documents to vector store"""
        
        # Create embeddings
        embeddings = self.embedding_service.create_embeddings(chunks)
        
        # Store in vector DB
        ids = self.vector_store.add_document_chunks(
            collection_name="documents",
            chunks=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )
        
        logger.info(f"Added {len(chunks)} chunks to vector store")
        return ids

# Singleton instance
rag_engine = RAGEngine()