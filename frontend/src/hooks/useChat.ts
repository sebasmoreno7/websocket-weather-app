// src/hooks/useChat.ts
import { useState, useCallback } from 'react';
import { Message } from '../types';

interface UseChatProps {
  sendChatMessage?: (message: string) => void;
}

export const useChat = ({ sendChatMessage }: UseChatProps = {}) => {
  const [chatMessages, setChatMessages] = useState<Message[]>([]);
  const [userInput, setUserInput] = useState("");

  const addChatMessage = useCallback((message: Message) => {
    setChatMessages(prev => [...prev, message]);
  }, []);

  const handleSendMessage = useCallback(() => {
    if (!userInput.trim()) return;

    // Send message via WebSocket if available
    if (sendChatMessage) {
      sendChatMessage(userInput);
    } else {
      // Fallback: add message locally
      const userMessage: Message = {
        sender: "Usuario",
        content: userInput,
        timestamp: new Date(),
        type: 'user'
      };
      addChatMessage(userMessage);
    }
    
    setUserInput("");
  }, [userInput, sendChatMessage, addChatMessage]);

  const handleKeyPress = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  }, [handleSendMessage]);

  return {
    chatMessages,
    userInput,
    setUserInput,
    handleSendMessage,
    handleKeyPress,
    addChatMessage
  };
};
