import json
import os
from typing import List, Optional
from datetime import datetime
import uuid
from .models import ChatSession, ChatMessage, MessageRole
from ..config import settings
import logging

logger = logging.getLogger(__name__)

class ChatHistoryManager:
    """Manages chat history storage"""
    
    def __init__(self):
        self.history_dir = settings.CHAT_HISTORY_DIR
        os.makedirs(self.history_dir, exist_ok=True)
    
    def _get_session_path(self, session_id: str) -> str:
        """Get file path for session"""
        return os.path.join(self.history_dir, f"{session_id}.json")
    
    def create_session(self, title: str = "New Chat") -> ChatSession:
        """Create a new chat session"""
        session = ChatSession(
            id=str(uuid.uuid4()),
            title=title,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            messages=[]
        )
        
        self._save_session(session)
        logger.info(f"Created new session: {session.id}")
        return session
    
    def _save_session(self, session: ChatSession):
        """Save session to disk"""
        path = self._get_session_path(session.id)
        with open(path, 'w') as f:
            json.dump(session.dict(), f, default=str, indent=2)
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get session by ID"""
        path = self._get_session_path(session_id)
        if not os.path.exists(path):
            return None
        
        with open(path, 'r') as f:
            data = json.load(f)
            # Convert string timestamps back to datetime
            if 'created_at' in data:
                data['created_at'] = datetime.fromisoformat(data['created_at'])
            if 'updated_at' in data:
                data['updated_at'] = datetime.fromisoformat(data['updated_at'])
            if 'messages' in data:
                for msg in data['messages']:
                    if 'timestamp' in msg:
                        msg['timestamp'] = datetime.fromisoformat(msg['timestamp'])
            
            return ChatSession(**data)
    
    def get_all_sessions(self) -> List[ChatSession]:
        """Get all chat sessions"""
        sessions = []
        for filename in os.listdir(self.history_dir):
            if filename.endswith('.json'):
                session_id = filename.replace('.json', '')
                session = self.get_session(session_id)
                if session:
                    sessions.append(session)
        
        # Sort by updated_at descending
        sessions.sort(key=lambda x: x.updated_at, reverse=True)
        return sessions
    
    def add_message(self, session_id: str, message: ChatMessage) -> ChatSession:
        """Add message to session"""
        session = self.get_session(session_id)
        if not session:
            session = self.create_session()
        
        session.messages.append(message)
        session.updated_at = datetime.now()
        
        # Update title if first message
        if len(session.messages) == 1 and message.role == MessageRole.USER:
            session.title = message.content[:50] + "..." if len(message.content) > 50 else message.content
        
        self._save_session(session)
        return session
    
    def delete_session(self, session_id: str):
        """Delete a session"""
        path = self._get_session_path(session_id)
        if os.path.exists(path):
            os.remove(path)
            logger.info(f"Deleted session: {session_id}")
    
    def get_session_messages(self, session_id: str, limit: int = 50) -> List[ChatMessage]:
        """Get recent messages from session"""
        session = self.get_session(session_id)
        if session:
            return session.messages[-limit:]
        return []

# Singleton instance
chat_history = ChatHistoryManager()