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
    robotA: false,
    robotB: false
  });

  const observerWs = useRef<WebSocket | null>(null);
  const robotAWs = useRef<WebSocket | null>(null);
  const robotBWs = useRef<WebSocket | null>(null);

  const addMessage = useCallback((sender: string, content: string, type: MessageType) => {
    const message: Message = {
      sender,
      content,
      timestamp: new Date(),
      type
    };
    setObserverMessages(prev => [...prev, message]);
  }, []);

  const getCityWeatherData = async (city: 'bogota' | 'medellin') => {
    // Simulated weather data
    const temp = city === 'bogota' ? Math.floor(Math.random() * 8) + 14 : Math.floor(Math.random() * 10) + 20;
    const time = new Date().toLocaleTimeString('es-CO', {
      hour: '2-digit',
      minute: '2-digit'
    });
    return { temp, time };
  };

  useEffect(() => {
    // Connect to Observer WebSocket
    const connectObserver = () => {
      observerWs.current = new WebSocket('ws://localhost:8000/ws/observer');
      
      observerWs.current.onopen = () => {
        setRobotConnections(prev => ({ ...prev, observer: true }));
        onNotification?.('✅ Observer conectado', 'success');
        addMessage('Sistema', 'Observer conectado exitosamente', "system");
      };

      observerWs.current.onmessage = (event) => {
        const data = event.data;
        onNotification?.('📨 Mensaje recibido del robot', 'info');
        
        // Parse robot message
        if (data.includes('Robot Bogotá') || data.includes('Robot Medellín')) {
          addMessage('Robot', data, "robot");
        } else {
          addMessage('Observer', data, "robot");
        }
      };

      observerWs.current.onclose = () => {
        setRobotConnections(prev => ({ ...prev, observer: false }));
        onNotification?.('❌ Observer desconectado', 'warning');
        addMessage('Sistema', 'Observer desconectado', "system");
      };

      observerWs.current.onerror = () => {
        onNotification?.('❌ Error en Observer', 'error');
        addMessage('Sistema', 'Error en conexión Observer', "system");
      };
    };

    // Connect Robot A (Bogotá)
    const connectRobotA = () => {
      robotAWs.current = new WebSocket('ws://localhost:8000/ws/robots');
      
      robotAWs.current.onopen = () => {
        setRobotConnections(prev => ({ ...prev, robotA: true }));
        onNotification?.('✅ Robot Bogotá conectado', 'success');
        addMessage('Sistema', 'Robot Bogotá conectado', "system");
        
        // Send periodic weather updates for Bogotá
        const intervalA = setInterval(async () => {
          if (robotAWs.current?.readyState === WebSocket.OPEN) {
            try {
              const bogotaData = await getCityWeatherData('bogota');
              const msg = `🏔️ Robot Bogotá: ${bogotaData.temp}°C - ${bogotaData.time}`;
              
              // Send to robots room
              robotAWs.current.send(msg);
              
              // Send to observer room if connected
              if (observerWs.current?.readyState === WebSocket.OPEN) {
                observerWs.current.send(msg);
              }
              
              addMessage('Sistema', `📤 Enviando: ${msg}`, "system");
            } catch (error) {
              const errorMsg = `🏔️ Robot Bogotá: Error obteniendo datos`;
              robotAWs.current.send(errorMsg);
              addMessage('Sistema', `📤 Error: ${errorMsg}`, "system");
            }
          }
        }, 15000); // Every 15 seconds

        return () => clearInterval(intervalA);
      };

      robotAWs.current.onerror = () => {
        setRobotConnections(prev => ({ ...prev, robotA: false }));
        onNotification?.('❌ Error Robot Bogotá', 'error');
      };

      robotAWs.current.onclose = () => {
        setRobotConnections(prev => ({ ...prev, robotA: false }));
        addMessage('Sistema', 'Robot Bogotá desconectado', "system");
      };
    };

    // Connect Robot B (Medellín)
    const connectRobotB = () => {
      robotBWs.current = new WebSocket('ws://localhost:8000/ws/robots');
      
      robotBWs.current.onopen = () => {
        setRobotConnections(prev => ({ ...prev, robotB: true }));
        onNotification?.('✅ Robot Medellín conectado', 'success');
        addMessage('Sistema', 'Robot Medellín conectado', "system");
        
        // Send periodic weather updates for Medellín
        const intervalB = setInterval(async () => {
          if (robotBWs.current?.readyState === WebSocket.OPEN) {
            try {
              const medellinData = await getCityWeatherData('medellin');
              const msg = `🌺 Robot Medellín: ${medellinData.temp}°C - ${medellinData.time}`;
              
              // Send to robots room
              robotBWs.current.send(msg);
              
              // Send to observer room if connected
              if (observerWs.current?.readyState === WebSocket.OPEN) {
                observerWs.current.send(msg);
              }
              
              addMessage('Sistema', `📤 Enviando: ${msg}`, "system");
            } catch (error) {
              const errorMsg = `🌺 Robot Medellín: Error obteniendo datos`;
              robotBWs.current.send(errorMsg);
              addMessage('Sistema', `📤 Error: ${errorMsg}`, "system");
            }
          }
        }, 20000); // Every 20 seconds

        return () => clearInterval(intervalB);
      };

      robotBWs.current.onerror = () => {
        setRobotConnections(prev => ({ ...prev, robotB: false }));
        onNotification?.('❌ Error Robot Medellín', 'error');
      };

      robotBWs.current.onclose = () => {
        setRobotConnections(prev => ({ ...prev, robotB: false }));
        addMessage('Sistema', 'Robot Medellín desconectado', "system");
      };
    };

    // Initialize connections
    addMessage('Sistema', '🧪 Iniciando conexiones WebSocket...', "system");
    
    connectObserver();
    connectRobotA();
    connectRobotB();

    // Cleanup function
    return () => {
      observerWs.current?.close();
      robotAWs.current?.close();
      robotBWs.current?.close();
      addMessage('Sistema', '🔌 Todas las conexiones cerradas', "system");
    };
  }, [onNotification, addMessage]);

  return {
    observerMessages,
    robotConnections
  };
};
