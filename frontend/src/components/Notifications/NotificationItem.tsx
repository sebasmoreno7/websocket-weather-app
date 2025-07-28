// src/components/Notifications/NotificationItem.tsx
import React from 'react';
import { Message } from '../../types';

interface NotificationItemProps {
  notification: Message;
}

const NotificationItem: React.FC<NotificationItemProps> = ({ notification }) => {
  return (
    <div
      style={{
        background: "#4CAF50",
        color: "white",
        padding: "10px 15px",
        borderRadius: "8px",  
        boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
        animation: "slideIn 0.3s ease-out"
      }}
    >
      {notification.content}
    </div>
  );
};

export default NotificationItem;
