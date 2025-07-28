// src/App.tsx
import React, { useCallback } from 'react';
import { useAuth } from './hooks/useAuth';
import { useNotifications } from './hooks/useNotifications';
import { useWebSocket } from './hooks/useWebSocket';
import { useChat } from './hooks/useChat';
import LoginScreen from './components/Auth/LoginScreen';
import OAuthCallback from './components/Auth/OAuthCallback';
import NotificationContainer from './components/Notifications/NotificationContainer';
import ConnectionStatus from './components/ConnectionStatus/ConnectionStatus';
import ObserverChat from './components/Chat/ObserverChat';
import InteractiveChat from './components/Chat/InteractiveChat';
import AppStyles from './components/Layout/AppStyles';

function App() {
  const { user, loading, logout, isAuthenticated } = useAuth();
  const { notifications, addNotification } = useNotifications();
  
  const addSystemMessage = useCallback((message: string) => {
    // This will be passed to useWebSocket to add system messages
  }, []);

  const { observerMessages, robotConnections, sendChatMessage } = useWebSocket({
    onNotification: addNotification,
    onSystemMessage: addSystemMessage
  });

  const { 
    userInput,
    setUserInput,
    handleSendMessage, 
    handleKeyPress
  } = useChat({ sendChatMessage });

  // Check if this is the OAuth callback page
  if (window.location.pathname === '/oauth/callback') {
    return <OAuthCallback />;
  }

  // Show loading screen
  if (loading) {
    return (
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        backgroundColor: '#f0f2f5',
        fontFamily: 'Arial, sans-serif'
      }}>
        <div style={{
          width: '40px',
          height: '40px',
          border: '4px solid #f3f3f3',
          borderTop: '4px solid #4285f4',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite',
          marginBottom: '20px'
        }} />
        <div style={{ fontSize: '18px', color: '#333' }}>
          Cargando...
        </div>
        <style dangerouslySetInnerHTML={{
          __html: `
            @keyframes spin {
              0% { transform: rotate(0deg); }
              100% { transform: rotate(360deg); }
            }
          `
        }} />
      </div>
    );
  }

  // Show login screen if not authenticated
  if (!isAuthenticated) {
    return <LoginScreen />;
  }

  return (
    <div style={{ 
      fontFamily: "sans-serif", 
      padding: "1rem", 
      maxWidth: "1200px", 
      margin: "0 auto",
      backgroundColor: "#f8f9fa",
      minHeight: "100vh"
    }}>
      <NotificationContainer notifications={notifications} />
      
      {/* Header with user info and logout */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '20px',
        padding: '20px',
        backgroundColor: 'white',
        borderRadius: '12px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
          <img 
            src={user?.picture || 'https://via.placeholder.com/50'} 
            alt="Profile" 
            style={{ 
              width: '50px', 
              height: '50px', 
              borderRadius: '50%',
              border: '2px solid #e0e0e0'
            }}
          />
          <div>
            <div style={{ 
              fontWeight: 'bold', 
              fontSize: '18px',
              color: '#333',
              marginBottom: '2px'
            }}>
              ¡Hola, {user?.name || 'Usuario'}! 👋
            </div>
            <div style={{ 
              fontSize: '14px', 
              color: '#666' 
            }}>
              {user?.email}
            </div>
          </div>
        </div>
        
        <button
          onClick={logout}
          style={{
            padding: '10px 20px',
            backgroundColor: '#dc3545',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '14px',
            fontWeight: '500',
            transition: 'background-color 0.2s ease'
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.backgroundColor = '#c82333';
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.backgroundColor = '#dc3545';
          }}
        >
          Cerrar Sesión 🚪
        </button>
      </div>
      
      <ConnectionStatus robotConnections={robotConnections} />

      <div style={{ 
        display: "grid", 
        gridTemplateColumns: "1fr 1fr", 
        gap: "20px",
        marginTop: "20px"
      }}>
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
