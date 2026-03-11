import os
import tempfile
from typing import List, Tuple, Dict, Any
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging
from ..config import settings

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Process various document types"""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def process_pdf(self, file_path: str, filename: str) -> Tuple[List[str], List[Dict]]:
        """Process PDF file"""
        chunks = []
        metadatas = []
        
        try:
            reader = PdfReader(file_path)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text.strip():
                    page_chunks = self.text_splitter.split_text(text)
                    for chunk in page_chunks:
                        chunks.append(chunk)
                        metadatas.append({
                            "document_id": filename,
                            "document_name": filename,
                            "page": page_num + 1,
                            "type": "pdf",
                            "chunk_index": len(chunks)
                        })
            
            logger.info(f"Processed PDF {filename}: {len(chunks)} chunks")
        except Exception as e:
            logger.error(f"Error processing PDF {filename}: {str(e)}")
            raise
        
        return chunks, metadatas
    
    def process_website(self, url: str) -> Tuple[List[str], List[Dict]]:
        """Process website content"""
        chunks = []
        metadatas = []
        
        try:
            # Fetch website content
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean text
            lines = (line.strip() for line in text.splitlines())
            chunks_text = [chunk for chunk in lines if chunk]
            text = '\n'.join(chunks_text)
            
            # Split into chunks
            text_chunks = self.text_splitter.split_text(text)
            
            for chunk in text_chunks:
                chunks.append(chunk)
                metadatas.append({
                    "document_id": url,
                    "document_name": url,
                    "type": "website",
                    "url": url,
                    "title": soup.title.string if soup.title else url,
                    "chunk_index": len(chunks)
                })
            
            logger.info(f"Processed website {url}: {len(chunks)} chunks")
        except Exception as e:
            logger.error(f"Error processing website {url}: {str(e)}")
            raise
        
        return chunks, metadatas
    
    def process_text(self, text: str, filename: str) -> Tuple[List[str], List[Dict]]:
        """Process raw text"""
        chunks = self.text_splitter.split_text(text)
        metadatas = []
        
        for i, chunk in enumerate(chunks):
            metadatas.append({
                "document_id": filename,
                "document_name": filename,
                "type": "text",
                "chunk_index": i
            })
        
        logger.info(f"Processed text {filename}: {len(chunks)} chunks")
        return chunks, metadatas

# Singleton instance
doc_processor = DocumentProcessor()