// src/components/ConnectionStatus/ConnectionStatus.tsx
import React from 'react';
import { RobotConnections } from '../../types';

interface ConnectionStatusProps {
  robotConnections: RobotConnections;
}

const ConnectionStatus: React.FC<ConnectionStatusProps> = ({ robotConnections }) => {
  return (
    <div style={{ 
      background: "#f5f5f5", 
      padding: "15px", 
      borderRadius: "8px", 
      marginBottom: "20px",
      display: "flex",
      gap: "20px",
      alignItems: "center"
    }}>
      <h2 style={{ margin: 0 }}>🔗 Estado de Conexiones</h2>
      <span style={{ color: robotConnections.observer ? "#4CAF50" : "#f44336" }}>
        Observer: {robotConnections.observer ? "✅" : "❌"}
      </span>
      <span style={{ color: robotConnections.robotA ? "#4CAF50" : "#f44336" }}>
        🏔️ Bogotá: {robotConnections.robotA ? "✅" : "❌"}
      </span>
      <span style={{ color: robotConnections.robotB ? "#4CAF50" : "#f44336" }}>
        🌺 Medellín: {robotConnections.robotB ? "✅" : "❌"}
      </span>
    </div>
  );
};

export default ConnectionStatus;
