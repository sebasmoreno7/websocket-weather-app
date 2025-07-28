// src/App.tsx
import React, { useCallback } from 'react';
import { useNotifications } from './hooks/useNotifications';
import { useWebSocket } from './hooks/useWebSocket';
import { useChat } from './hooks/useChat';
import NotificationContainer from './components/Notifications/NotificationContainer';
import ConnectionStatus from './components/ConnectionStatus/ConnectionStatus';
import ObserverChat from './components/Chat/ObserverChat';
import InteractiveChat from './components/Chat/InteractiveChat';
import AppStyles from './components/Layout/AppStyles';

function App() {
  const { notifications, addNotification } = useNotifications();
  
  const addSystemMessage = useCallback((message: string) => {
    // This will be passed to useWebSocket to add system messages
  }, []);

  const { observerMessages, robotConnections, sendChatMessage } = useWebSocket({
    onNotification: addNotification,
    onSystemMessage: addSystemMessage
  });

  const { 
    chatMessages, 
    userInput,
    setUserInput,
    handleSendMessage, 
    handleKeyPress,
    addChatMessage
  } = useChat({ sendChatMessage });

  return (
    <div style={{ 
      fontFamily: "sans-serif", 
      padding: "1rem", 
      maxWidth: "1200px", 
      margin: "0 auto" 
    }}>
      <NotificationContainer notifications={notifications} />
      
      <ConnectionStatus robotConnections={robotConnections} />

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
        <InteractiveChat
          userInput={userInput}
          onInputChange={setUserInput}
          onSendMessage={handleSendMessage}
          onKeyPress={handleKeyPress}
        />
        
        <ObserverChat messages={observerMessages} />
      </div>

      <AppStyles />
    </div>
  );
}

export default App;
