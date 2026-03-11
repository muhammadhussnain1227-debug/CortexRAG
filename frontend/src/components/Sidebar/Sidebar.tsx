import React from 'react';
import { MessageSquare, Settings, Sun, Moon, Trash2 } from 'lucide-react';
import { useTheme } from '../../hooks/useTheme';
import { ChatSession } from '../../types';
import { formatDistanceToNow } from 'date-fns';

interface SidebarProps {
  sessions: ChatSession[];
  currentSessionId?: string;
  onSessionSelect: (sessionId: string) => void;
  onSessionDelete: (sessionId: string) => void;
  onNewChat: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  sessions,
  currentSessionId,
  onSessionSelect,
  onSessionDelete,
  onNewChat,
}) => {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="w-64 h-full bg-gray-50 dark:bg-gray-900 border-r dark:border-gray-700 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b dark:border-gray-700">
        <h1 className="text-xl font-bold text-gray-900 dark:text-white">CortexRAG</h1>
        <button
          onClick={onNewChat}
          className="mt-2 w-full px-3 py-2 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
        >
          + New Chat
        </button>
      </div>

      {/* Chat History */}
      <div className="flex-1 overflow-y-auto p-2">
        <h2 className="px-2 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2">
          Recent Chats
        </h2>
        
        {sessions.length === 0 ? (
          <p className="text-sm text-gray-500 dark:text-gray-400 text-center mt-4">
            No chats yet
          </p>
        ) : (
          <div className="space-y-1">
            {sessions.map((session) => (
              <div
                key={session.id}
                className={`group relative rounded-lg cursor-pointer ${
                  currentSessionId === session.id
                    ? 'bg-primary-100 dark:bg-primary-900'
                    : 'hover:bg-gray-200 dark:hover:bg-gray-800'
                }`}
              >
                <div
                  onClick={() => onSessionSelect(session.id)}
                  className="p-3 pr-8"
                >
                  <div className="flex items-center">
                    <MessageSquare size={16} className="mr-2 text-gray-500 dark:text-gray-400" />
                    <span className="text-sm font-medium text-gray-900 dark:text-white truncate">
                      {session.title}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {formatDistanceToNow(new Date(session.updated_at), { addSuffix: true })}
                  </p>
                </div>
                
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onSessionDelete(session.id);
                  }}
                  className="absolute right-2 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 p-1 text-gray-500 hover:text-red-500 dark:text-gray-400 dark:hover:text-red-400"
                >
                  <Trash2 size={14} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t dark:border-gray-700">
        <button
          onClick={toggleTheme}
          className="w-full p-2 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-800 rounded-lg flex items-center justify-center gap-2"
        >
          {theme === 'light' ? <Moon size={16} /> : <Sun size={16} />}
          <span className="text-sm">{theme === 'light' ? 'Dark' : 'Light'} Mode</span>
        </button>
      </div>
    </div>
  );
};