import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "CortexRAG"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Database Settings
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    CHAT_HISTORY_DIR: str = "./chat_history"
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {"pdf", "txt", "docx", "md"}
    
    # Model Settings
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    LLM_MODEL: str = "gpt-4-turbo-preview"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"

settings = Settings()