// src/components/ConnectionStatus/ConnectionStatus.tsx
import React from 'react';
import { RobotConnections } from '../../types';
import { useResponsive } from '../../hooks/useResponsive';

interface ConnectionStatusProps {
  robotConnections: RobotConnections;
}

const ConnectionStatus: React.FC<ConnectionStatusProps> = ({ robotConnections }) => {
  const { mobile } = useResponsive();

  return (
    <div style={{ 
      background: "#f5f5f5", 
      padding: "clamp(12px, 3vw, 15px)", 
      borderRadius: "8px", 
      marginBottom: "clamp(15px, 3vw, 20px)",
      display: "flex",
      flexDirection: mobile ? "column" : "row",
      gap: mobile ? "10px" : "20px",
      alignItems: mobile ? "flex-start" : "center"
    }}>
      <h2 style={{ 
        margin: 0, 
        fontSize: "clamp(16px, 3.5vw, 18px)",
        marginBottom: mobile ? "5px" : 0
      }}>
        🔗 Estado de Conexiones
      </h2>
      <div style={{
        display: "flex",
        flexDirection: mobile ? "column" : "row",
        gap: mobile ? "8px" : "20px",
        fontSize: "clamp(13px, 2.8vw, 14px)"
      }}>
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
    </div>
  );
};

export default ConnectionStatus;
