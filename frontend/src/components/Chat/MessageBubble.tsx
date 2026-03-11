import React from 'react';
import { ChatMessage } from '../../types';
import { Bot, User, Clock } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { formatDistanceToNow } from 'date-fns';

interface MessageBubbleProps {
  message: ChatMessage;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`flex max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 ${isUser ? 'ml-3' : 'mr-3'}`}>
          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
            isUser 
              ? 'bg-primary-600 text-white' 
              : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
          }`}>
            {isUser ? <User size={16} /> : <Bot size={16} />}
          </div>
        </div>

        {/* Message Content */}
        <div>
          <div className={`rounded-2xl px-4 py-2 ${
            isUser
              ? 'bg-primary-600 text-white'
              : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100'
          }`}>
            <ReactMarkdown className="prose dark:prose-invert max-w-none">
              {message.content}
            </ReactMarkdown>
          </div>

          {/* Timestamp */}
          <div className={`flex items-center mt-1 text-xs text-gray-500 dark:text-gray-400 ${
            isUser ? 'justify-end' : 'justify-start'
          }`}>
            <Clock size={12} className="mr-1" />
            {formatDistanceToNow(new Date(message.timestamp), { addSuffix: true })}
          </div>

          {/* Sources */}
          {message.sources && message.sources.length > 0 && (
            <div className="mt-2">
              <details className="text-sm">
                <summary className="cursor-pointer text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200">
                  Sources ({message.sources.length})
                </summary>
                <div className="mt-2 space-y-2">
                  {message.sources.map((source, idx) => (
                    <div key={idx} className="text-xs p-2 bg-gray-50 dark:bg-gray-800 rounded">
                      <div className="font-medium text-gray-700 dark:text-gray-300">
                        📄 {source.document_name}
                        {source.page && ` (Page ${source.page})`}
                      </div>
                      <div className="text-gray-500 dark:text-gray-400 mt-1">
                        {source.chunk_text}
                      </div>
                      <div className="text-gray-400 dark:text-gray-500 mt-1">
                        Relevance: {(source.relevance_score * 100).toFixed(0)}%
                      </div>
                    </div>
                  ))}
                </div>
              </details>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};