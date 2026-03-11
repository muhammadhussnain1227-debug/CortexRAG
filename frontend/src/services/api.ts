import axios from 'axios';
import { ChatMessage, ChatRequest, ChatResponse, ChatSession, UploadResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Chat endpoints
export const sendMessage = async (request: ChatRequest): Promise<ChatResponse> => {
  const response = await api.post('/chat/', request);
  return response.data;
};

export const sendMessageStream = async (
  request: ChatRequest,
  onChunk: (chunk: string) => void
) => {
  // Implement streaming if needed
};

// Document endpoints
export const uploadDocument = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/documents/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const uploadUrl = async (url: string): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('url', url);
  
  const response = await api.post('/documents/url', formData);
  return response.data;
};

// History endpoints
export const getSessions = async (): Promise<ChatSession[]> => {
  const response = await api.get('/history/sessions');
  return response.data;
};

export const getSession = async (sessionId: string): Promise<ChatSession> => {
  const response = await api.get(`/history/sessions/${sessionId}`);
  return response.data;
};

export const deleteSession = async (sessionId: string): Promise<void> => {
  await api.delete(`/history/sessions/${sessionId}`);
};

export const getSessionMessages = async (
  sessionId: string,
  limit: number = 50
): Promise<ChatMessage[]> => {
  const response = await api.get(`/history/sessions/${sessionId}/messages?limit=${limit}`);
  return response.data;
};