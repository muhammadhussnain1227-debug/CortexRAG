# CortexRAG - Multi-Document Chat with Source Tracking

## 🚀 Features
- Chat with multiple PDFs, documents, and websites
- Source citations with page numbers
- Chat history persistence
- Dark/Light theme
- Modern React frontend
- FastAPI backend
- Vector search with ChromaDB

## 📋 Prerequisites
- Python 3.10+
- Node.js 18+
- OpenAI API key

## 🛠️ Installation

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your OpenAI API key to .env
uvicorn app.main:app --reload