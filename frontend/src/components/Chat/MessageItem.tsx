// src/components/Chat/MessageItem.tsx
import React from 'react';
import { Message } from '../../types';
import { useResponsive } from '../../hooks/useResponsive';

interface MessageItemProps {
  message: Message;
  isUserMessage?: boolean;
}

const MessageItem: React.FC<MessageItemProps> = ({ message, isUserMessage = false }) => {
  const { mobile } = useResponsive();

  const getBackgroundColor = () => {
    if (isUserMessage && message.type === 'user') return "#e8f5e8";
    if (message.type === 'system') return "#e3f2fd";
    if (message.type === 'robot') return "#fff";
    return "#f0f0f0";
  };

  const getBorderStyle = () => {
    if (message.type === 'robot') return "1px solid #4CAF50";
    return "none";
  };

  const getTextColor = () => {
    if (message.type === 'robot') return "#4CAF50";
    if (message.type === 'user') return "#2E7D32";
    if (message.type === 'system') return "#1976D2";
    return "#333";
  };

  return (
    <div 
      style={{ 
        marginBottom: "clamp(8px, 2vw, 10px)",
        padding: "clamp(6px, 1.5vw, 8px)",
        borderRadius: "6px",
        background: getBackgroundColor(),
        border: getBorderStyle(),
        marginLeft: (isUserMessage && message.type === 'user') ? (mobile ? "10px" : "20px") : "0",
        marginRight: (isUserMessage && message.type === 'user') ? "0" : (mobile ? "10px" : "20px")
      }}
    >
      <div style={{ 
        fontSize: mobile ? "0.7em" : "0.8em", 
        color: "#666", 
        marginBottom: "4px" 
      }}>
        {message.timestamp.toLocaleTimeString()}
      </div>
      <div style={{ 
        whiteSpace: "pre-line",
        fontSize: "clamp(13px, 2.8vw, 14px)",
        lineHeight: "1.4"
      }}>
        <strong style={{ color: getTextColor() }}>
          {message.sender}
        </strong>: {message.content}
      </div>
    </div>
  );
};

export default MessageItem;
