// src/hooks/useNotifications.ts
import { useState, useCallback } from 'react';
import { Message } from '../types';

export const useNotifications = () => {
  const [notifications, setNotifications] = useState<Message[]>([]);

  const addNotification = useCallback((message: string) => {
    const notification: Message = {
      sender: "Sistema",
      content: message,
      timestamp: new Date(),
      type: 'notification'
    };

    setNotifications(prev => [...prev, notification]);
    
    // Auto-remove notification after 5 seconds
    setTimeout(() => {
      setNotifications(prev => prev.slice(1));
    }, 5000);
  }, []);

  return {
    notifications,
    addNotification
  };
};
