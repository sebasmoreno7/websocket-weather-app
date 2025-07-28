// src/hooks/useWebSocket.ts
import { useState, useEffect, useRef, useCallback } from 'react';
import { Message, MessageType, RobotConnections } from '../types';

interface UseWebSocketProps {
  onNotification?: (message: string, type?: 'info' | 'success' | 'warning' | 'error') => void;
  onSystemMessage?: (message: string) => void;
}

export const useWebSocket = ({ onNotification, onSystemMessage }: UseWebSocketProps) => {
  const [observerMessages, setObserverMessages] = useState<Message[]>([]);
  const [robotConnections, setRobotConnections] = useState<RobotConnections>({
    observer: false,
    robotA: true, // Server robots are always "connected" as background tasks
    robotB: true
  });

  const observerWs = useRef<WebSocket | null>(null);

  const addMessage = useCallback((sender: string, content: string, type: MessageType) => {
    const message: Message = {
      sender,
      content,
      timestamp: new Date(),
      type
    };
    setObserverMessages(prev => [...prev, message]);
  }, []);

  const sendChatMessage = useCallback((message: string) => {
    if (observerWs.current?.readyState === WebSocket.OPEN) {
      observerWs.current.send(message);
      addMessage('Usuario', message, 'user');
    }
  }, [addMessage]);

  useEffect(() => {
    // Connect as Observer to receive automatic robot data
    const connectObserver = () => {
      observerWs.current = new WebSocket('ws://localhost:8000/ws/observer');
      
      observerWs.current.onopen = () => {
        setRobotConnections(prev => ({ ...prev, observer: true }));
        onNotification?.('✅ Observer conectado - Robots activos en servidor', 'success');
        addMessage('Sistema', '✅ Conectado como Observer - Recibirás datos automáticos', "system");
      };

      observerWs.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          
          if (data.type === 'weather_update') {
            // Robot weather data from server
            onNotification?.(`📡 ${data.robot}: ${data.data.temperature}°C`, 'info');
            addMessage('Robot', data.message, "robot");
          } else if (data.type === 'chat_response') {
            // Chat response from server - show in observer panel
            addMessage('Chat Bot', data.message, "system");
          } else if (data.type === 'connection') {
            // Connection message
            addMessage('Sistema', data.message, "system");
          } else {
            // Fallback for string messages
            addMessage('Servidor', data.message || event.data, "robot");
          }
        } catch (error) {
          // Handle non-JSON messages
          const message = event.data;
          if (message.includes('Robot Bogotá') || message.includes('Robot Medellín')) {
            addMessage('Robot', message, "robot");
          } else {
            addMessage('Servidor', message, "system");
          }
        }
      };

      observerWs.current.onclose = () => {
        setRobotConnections(prev => ({ ...prev, observer: false }));
        onNotification?.('❌ Observer desconectado', 'warning');
        addMessage('Sistema', '❌ Observer desconectado', "system");
        
        // Auto-reconnect after 3 seconds
        setTimeout(() => {
          if (!observerWs.current || observerWs.current.readyState === WebSocket.CLOSED) {
            addMessage('Sistema', '� Reintentando conexión...', "system");
            connectObserver();
          }
        }, 3000);
      };

      observerWs.current.onerror = (error) => {
        onNotification?.('❌ Error en conexión Observer', 'error');
        addMessage('Sistema', '❌ Error en conexión Observer', "system");
      };
    };

    // Initialize observer connection
    addMessage('Sistema', '🧪 Conectando como Observer al servidor con robots...', "system");
    connectObserver();

    // Cleanup function
    return () => {
      observerWs.current?.close();
      addMessage('Sistema', '🔌 Conexión Observer cerrada', "system");
    };
  }, [onNotification, addMessage]);

  return {
    observerMessages,
    robotConnections,
    sendChatMessage
  };
};
