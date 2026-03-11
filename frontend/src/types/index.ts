export type MessageRole = 'user' | 'assistant' | 'system';

export interface Source {
  document_id: string;
  document_name: string;
  page?: number;
  chunk_text: string;
  relevance_score: number;
  metadata: Record<string, any>;
}

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: Date;
  sources?: Source[];
  tokens_used?: number;
}

export interface ChatSession {
  id: string;
  title: string;
  created_at: Date;
  updated_at: Date;
  messages: ChatMessage[];
  document_ids: string[];
}

export interface ChatRequest {
  session_id?: string;
  message: string;
  document_ids?: string[];
  use_history?: boolean;
  temperature?: number;
}

export interface ChatResponse {
  session_id: string;
  message: string;
  sources: Source[];
  tokens_used: number;
  processing_time: number;
}

export interface Document {
  id: string;
  filename: string;
  type: string;
  size: number;
  uploaded_at: Date;
  chunk_count: number;
}

export interface UploadResponse {
  success: boolean;
  document_id?: string;
  message: string;
  chunk_count?: number;
}