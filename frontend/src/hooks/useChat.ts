import { useState, useCallback } from 'react';
import { ChatMessage, ChatResponse, Source } from '../types';
import { sendMessage } from '../services/api';
import toast from 'react-hot-toast';

export const useChat = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentSessionId, setCurrentSessionId] = useState<string>();

  const sendUserMessage = useCallback(async (
    content: string,
    documentIds: string[] = []
  ) => {
    if (!content.trim()) return;

    // Add user message immediately
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await sendMessage({
        session_id: currentSessionId,
        message: content,
        document_ids: documentIds,
        use_history: true,
        temperature: 0.7,
      });

      // Add assistant message
      const assistantMessage: ChatMessage = {
        id: response.session_id + '-' + Date.now(),
        role: 'assistant',
        content: response.message,
        timestamp: new Date(),
        sources: response.sources,
        tokens_used: response.tokens_used,
      };

      setMessages(prev => [...prev, assistantMessage]);
      setCurrentSessionId(response.session_id);
      
    } catch (error) {
      console.error('Chat error:', error);
      toast.error('Failed to send message. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }, [currentSessionId]);

  const clearChat = useCallback(() => {
    setMessages([]);
    setCurrentSessionId(undefined);
  }, []);

  return {
    messages,
    isLoading,
    currentSessionId,
    sendUserMessage,
    clearChat,
  };
};