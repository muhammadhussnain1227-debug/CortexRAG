import React, { useState, useRef, useEffect } from 'react';
import { Send, Paperclip, Loader2 } from 'lucide-react';
import { MessageBubble } from './MessageBubble';
import { useChat } from '../../hooks/useChat';
import { uploadDocument, uploadUrl } from '../../services/api';
import toast from 'react-hot-toast';

export const ChatInterface: React.FC = () => {
  const [input, setInput] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [selectedDocs, setSelectedDocs] = useState<string[]>([]);
  const { messages, isLoading, sendUserMessage } = useChat();
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    await sendUserMessage(input, selectedDocs);
    setInput('');
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files?.length) return;

    setIsUploading(true);
    try {
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const response = await uploadDocument(file);
        if (response.success && response.document_id) {
          setSelectedDocs(prev => [...prev, response.document_id!]);
          toast.success(`Uploaded: ${file.name}`);
        }
      }
    } catch (error) {
      toast.error('Failed to upload files');
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleUrlUpload = async () => {
    const url = window.prompt('Enter website URL:');
    if (!url) return;

    setIsUploading(true);
    try {
      const response = await uploadUrl(url);
      if (response.success && response.document_id) {
        setSelectedDocs(prev => [...prev, response.document_id!]);
        toast.success('Website content loaded');
      }
    } catch (error) {
      toast.error('Failed to load website');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white dark:bg-gray-900">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 dark:text-gray-400 mt-20">
            <h2 className="text-2xl font-bold mb-2">Welcome to CortexRAG</h2>
            <p>Upload documents and start asking questions!</p>
          </div>
        ) : (
          messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))
        )}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 dark:bg-gray-800 rounded-2xl px-4 py-2">
              <Loader2 className="w-5 h-5 animate-spin text-gray-500" />
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Selected Docs Indicator */}
      {selectedDocs.length > 0 && (
        <div className="px-4 py-2 border-t dark:border-gray-700 bg-gray-50 dark:bg-gray-800">
          <div className="flex items-center gap-2 text-sm">
            <span className="text-gray-600 dark:text-gray-300">
              📄 Querying {selectedDocs.length} document(s)
            </span>
            <button
              onClick={() => setSelectedDocs([])}
              className="text-xs text-red-500 hover:text-red-600"
            >
              Clear
            </button>
          </div>
        </div>
      )}

      {/* Input Area */}
      <form onSubmit={handleSubmit} className="border-t dark:border-gray-700 p-4">
        <div className="flex items-center gap-2">
          <div className="flex gap-1">
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              disabled={isUploading}
              className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
            >
              <Paperclip size={20} />
            </button>
            <button
              type="button"
              onClick={handleUrlUpload}
              disabled={isUploading}
              className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-sm"
            >
              🌐 URL
            </button>
          </div>
          
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileUpload}
            multiple
            accept=".pdf,.txt,.docx,.md"
            className="hidden"
          />
          
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question..."
            className="flex-1 p-2 border dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
            disabled={isLoading}
          />
          
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="p-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send size={20} />
          </button>
        </div>
      </form>
    </div>
  );
};