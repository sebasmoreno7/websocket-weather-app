// src/App.tsx
import React, { useCallback } from 'react';
import { useAuth } from './hooks/useAuth';
import { useNotifications } from './hooks/useNotifications';
import { useWebSocket } from './hooks/useWebSocket';
import { useChat } from './hooks/useChat';
import { useResponsive } from './hooks/useResponsive';
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
  const { mobile, width } = useResponsive();
  
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
      padding: "clamp(0.5rem, 2vw, 1rem)", 
      maxWidth: "1200px", 
      margin: "0 auto",
      backgroundColor: "#f8f9fa",
      minHeight: "100vh"
    }}>
      <NotificationContainer notifications={notifications} />
      
      {/* Header with user info and logout */}
      <div style={{
        display: 'flex',
        flexDirection: mobile ? 'column' : 'row',
        justifyContent: 'space-between',
        alignItems: mobile ? 'stretch' : 'center',
        gap: mobile ? '15px' : '0',
        marginBottom: '20px',
        padding: 'clamp(15px, 3vw, 20px)',
        backgroundColor: 'white',
        borderRadius: '12px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '15px', flex: 1 }}>
          <img 
            src={user?.picture || 'https://via.placeholder.com/50'} 
            alt="Profile" 
            style={{ 
              width: 'clamp(40px, 8vw, 50px)', 
              height: 'clamp(40px, 8vw, 50px)', 
              borderRadius: '50%',
              border: '2px solid #e0e0e0'
            }}
          />
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ 
              fontWeight: 'bold', 
              fontSize: 'clamp(16px, 3.5vw, 18px)',
              color: '#333',
              marginBottom: '2px',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap'
            }}>
              ¡Hola, {user?.name || 'Usuario'}! 👋
            </div>
            <div style={{ 
              fontSize: 'clamp(12px, 2.5vw, 14px)', 
              color: '#666',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap'
            }}>
              {user?.email}
            </div>
          </div>
        </div>
        
        <button
          onClick={logout}
          style={{
            padding: 'clamp(8px, 2vw, 10px) clamp(15px, 3vw, 20px)',
            backgroundColor: '#dc3545',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: 'clamp(12px, 2.5vw, 14px)',
            fontWeight: '500',
            transition: 'background-color 0.2s ease',
            whiteSpace: 'nowrap',
            width: mobile ? '100%' : 'auto'
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
        gridTemplateColumns: mobile ? "1fr" : "1fr 1fr", 
        gap: "clamp(15px, 3vw, 20px)",
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
