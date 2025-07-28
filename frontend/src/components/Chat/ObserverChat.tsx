// src/components/Chat/ObserverChat.tsx
import React, { useEffect, useRef } from 'react';
import { Message } from '../../types';
import { useResponsive } from '../../hooks/useResponsive';
import MessageItem from './MessageItem';

interface ObserverChatProps {
  messages: Message[];
}

const ObserverChat: React.FC<ObserverChatProps> = ({ messages }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { mobile } = useResponsive();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div>
      <h2 style={{ 
        fontSize: "clamp(18px, 4vw, 20px)",
        marginBottom: "clamp(15px, 3vw, 20px)"
      }}>
        {mobile ? "🤖 Respuestas & Clima" : "🤖 Respuestas del Chat & Clima en tiempo real"}
      </h2>
      <div style={{ 
        border: "1px solid #ddd", 
        borderRadius: "8px", 
        height: mobile ? "300px" : "400px", 
        overflow: "auto",
        background: "#fafafa",
        padding: "clamp(8px, 2vw, 10px)"
      }}>
        {messages.length === 0 && (
          <div style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            height: "100%",
            color: "#999",
            fontSize: "clamp(14px, 3vw, 16px)",
            textAlign: "center",
            padding: "20px"
          }}>
            {mobile ? "Los mensajes aparecerán aquí..." : "Los mensajes del chat y clima aparecerán aquí..."}
          </div>
        )}
        {messages.map((msg, idx) => (
          <MessageItem key={idx} message={msg} />
        ))}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default ObserverChat;
