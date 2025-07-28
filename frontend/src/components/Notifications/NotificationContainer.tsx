// src/components/Notifications/NotificationContainer.tsx
import React from 'react';
import { Message } from '../../types';
import { useResponsive } from '../../hooks/useResponsive';
import NotificationItem from './NotificationItem';

interface NotificationContainerProps {
  notifications: Message[];
}

const NotificationContainer: React.FC<NotificationContainerProps> = ({ notifications }) => {
  const { mobile } = useResponsive();

  return (
    <div style={{ 
      position: "fixed", 
      top: mobile ? "10px" : "20px", 
      right: mobile ? "10px" : "20px", 
      left: mobile ? "10px" : "auto",
      zIndex: 1000,
      display: "flex",
      flexDirection: "column",
      gap: mobile ? "8px" : "10px",
      maxWidth: mobile ? "none" : "400px"
    }}>
      {notifications.map((notification, idx) => (
        <NotificationItem key={idx} notification={notification} />
      ))}
    </div>
  );
};

export default NotificationContainer;
