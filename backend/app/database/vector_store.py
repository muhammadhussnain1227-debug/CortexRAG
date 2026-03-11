import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
import logging
from ..config import settings

logger = logging.getLogger(__name__)

class VectorStoreManager:
    """Manages ChromaDB vector store operations"""
    
    def __init__(self):
        """Initialize ChromaDB client"""
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=Settings(anonymized_telemetry=False)
        )
        
    def get_or_create_collection(self, collection_name: str):
        """Get existing collection or create new one"""
        try:
            collection = self.client.get_collection(collection_name)
            logger.info(f"Collection '{collection_name}' retrieved")
        except:
            collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Collection '{collection_name}' created")
        return collection
    
    def add_document_chunks(self, 
                           collection_name: str,
                           chunks: List[str],
                           embeddings: List[List[float]],
                           metadatas: List[Dict[str, Any]]) -> List[str]:
        """Add document chunks to vector store"""
        collection = self.get_or_create_collection(collection_name)
        
        # Generate unique IDs
        ids = [f"{collection_name}_{uuid.uuid4().hex}" for _ in chunks]
        
        # Add to ChromaDB
        collection.add(
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        
        logger.info(f"Added {len(chunks)} chunks to {collection_name}")
        return ids
    
    def similarity_search(self,
                         collection_name: str,
                         query_embedding: List[float],
                         n_results: int = 5,
                         filter_criteria: Optional[Dict] = None) -> List[Dict]:
        """Search for similar chunks"""
        collection = self.get_or_create_collection(collection_name)
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter_criteria
        )
        
        # Format results
        formatted_results = []
        if results['ids'][0]:
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'document': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
        
        return formatted_results
    
    def delete_document(self, collection_name: str, document_id: str):
        """Delete all chunks for a specific document"""
        collection = self.get_or_create_collection(collection_name)
        collection.delete(where={"document_id": document_id})
        logger.info(f"Deleted document {document_id} from {collection_name}")

# Singleton instance
vector_store = VectorStoreManager()