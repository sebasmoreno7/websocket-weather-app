// src/components/Notifications/NotificationContainer.tsx
import React from 'react';
import { Message } from '../../types';
import NotificationItem from './NotificationItem';

interface NotificationContainerProps {
  notifications: Message[];
}

const NotificationContainer: React.FC<NotificationContainerProps> = ({ notifications }) => {
  return (
    <div style={{ 
      position: "fixed", 
      top: "20px", 
      right: "20px", 
      zIndex: 1000,
      display: "flex",
      flexDirection: "column",
      gap: "10px"
    }}>
      {notifications.map((notification, idx) => (
        <NotificationItem key={idx} notification={notification} />
      ))}
    </div>
  );
};

export default NotificationContainer;
