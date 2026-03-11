import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar/Sidebar';
import { ChatInterface } from './components/Chat/ChatInterface';
import { Toaster } from 'react-hot-toast';
import { getSessions, deleteSession, getSession } from './services/api';
import { ChatSession } from './types';

function App() {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<string>();

  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    try {
      const data = await getSessions();
      setSessions(data);
    } catch (error) {
      console.error('Failed to load sessions:', error);
    }
  };

  const handleSessionSelect = async (sessionId: string) => {
    setCurrentSessionId(sessionId);
    // Load session messages through chat interface
  };

  const handleSessionDelete = async (sessionId: string) => {
    try {
      await deleteSession(sessionId);
      await loadSessions();
      if (currentSessionId === sessionId) {
        setCurrentSessionId(undefined);
      }
    } catch (error) {
      console.error('Failed to delete session:', error);
    }
  };

  const handleNewChat = () => {
    setCurrentSessionId(undefined);
  };

  return (
    <div className="flex h-screen bg-white dark:bg-gray-900">
      <Toaster position="top-right" />
      
      <Sidebar
        sessions={sessions}
        currentSessionId={currentSessionId}
        onSessionSelect={handleSessionSelect}
        onSessionDelete={handleSessionDelete}
        onNewChat={handleNewChat}
      />
      
      <div className="flex-1">
        <ChatInterface />
      </div>
    </div>
  );
}

export default App;