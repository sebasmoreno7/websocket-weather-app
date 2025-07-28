// src/components/Notifications/NotificationItem.tsx
import React from 'react';
import { Message } from '../../types';
import { useResponsive } from '../../hooks/useResponsive';

interface NotificationItemProps {
  notification: Message;
}

const NotificationItem: React.FC<NotificationItemProps> = ({ notification }) => {
  const { mobile } = useResponsive();

  return (
    <div
      style={{
        background: "#4CAF50",
        color: "white",
        padding: mobile ? "8px 12px" : "10px 15px",
        borderRadius: "8px",  
        boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
        animation: "slideIn 0.3s ease-out",
        fontSize: mobile ? "13px" : "14px",
        lineHeight: "1.4",
        wordBreak: "break-word"
      }}
    >
      {notification.content}
    </div>
  );
};

export default NotificationItem;
