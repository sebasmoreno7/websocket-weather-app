// src/components/Chat/ObserverChat.tsx
import React, { useEffect, useRef } from 'react';
import { Message } from '../../types';
import MessageItem from './MessageItem';

interface ObserverChatProps {
  messages: Message[];
}

const ObserverChat: React.FC<ObserverChatProps> = ({ messages }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div>
      <h2>🤖 Respuestas del Chat & Clima en tiempo real</h2>
      <div style={{ 
        border: "1px solid #ddd", 
        borderRadius: "8px", 
        height: "400px", 
        overflow: "auto",
        background: "#fafafa",
        padding: "10px"
      }}>
        {messages.map((msg, idx) => (
          <MessageItem key={idx} message={msg} />
        ))}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default ObserverChat;
