from openai import OpenAI
from typing import List, Dict, Any
import logging
from ..config import settings

logger = logging.getLogger(__name__)

class LLMService:
    """Handle LLM interactions"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.LLM_MODEL
    
    def generate_response(self, 
                         query: str,
                         context_chunks: List[Dict],
                         chat_history: List[Dict] = None,
                         temperature: float = 0.7) -> Dict[str, Any]:
        """Generate response using RAG"""
        
        # Format context
        context_text = "\n\n".join([
            f"[Source {i+1}] {chunk['document']}" 
            for i, chunk in enumerate(context_chunks)
        ])
        
        # Format chat history
        history_text = ""
        if chat_history:
            history_text = "Previous conversation:\n"
            for msg in chat_history[-5:]:  # Last 5 messages
                role = "User" if msg['role'] == 'user' else "Assistant"
                history_text += f"{role}: {msg['content']}\n"
        
        # Create system prompt
        system_prompt = """You are CortexRAG, an AI assistant specialized in answering questions based on provided documents.
        Always cite your sources using [Source X] notation.
        If you cannot find the answer in the provided context, say so politely.
        Be concise but comprehensive in your answers."""
        
        # Create user prompt
        user_prompt = f"""Context from documents:
{context_text}

{history_text}

Current question: {query}

Answer the question using the provided context. Cite sources as [Source X] where X is the source number.
If the context doesn't contain relevant information, say that you cannot find the answer in the provided documents."""

        try:
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )
            
            result = {
                "content": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
                "model": self.model
            }
            
            logger.info(f"Generated response with {result['tokens_used']} tokens")
            return result
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

# Singleton instance
llm_service = LLMService()