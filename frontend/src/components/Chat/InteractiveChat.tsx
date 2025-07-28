// src/components/Chat/InteractiveChat.tsx
import React from 'react';
import { useResponsive } from '../../hooks/useResponsive';

interface InteractiveChatProps {
  userInput: string;
  onInputChange: (value: string) => void;
  onSendMessage: () => void;
  onKeyPress: (e: React.KeyboardEvent) => void;
}

const InteractiveChat: React.FC<InteractiveChatProps> = ({
  userInput,
  onInputChange,
  onSendMessage,
  onKeyPress
}) => {
  const { mobile } = useResponsive();

  return (
    <div>
      <h2 style={{ 
        fontSize: "clamp(18px, 4vw, 20px)",
        marginBottom: "clamp(15px, 3vw, 20px)"
      }}>
        💬 Chat Clima Colombia
      </h2>
      <div style={{ 
        border: "1px solid #ddd", 
        borderRadius: "8px", 
        background: "#fafafa",
        padding: "clamp(15px, 3vw, 20px)",
        minHeight: mobile ? "80px" : "100px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center"
      }}>
        <p style={{ 
          margin: "0 0 15px 0", 
          color: "#666", 
          fontSize: "clamp(12px, 2.5vw, 14px)",
          lineHeight: "1.4"
        }}>
          💡 {mobile ? "Pregunta sobre el clima" : "Escribe tu pregunta y las respuestas aparecerán en el panel derecho"}
        </p>
        
        <div style={{ 
          display: "flex", 
          flexDirection: mobile ? "column" : "row",
          gap: mobile ? "12px" : "10px" 
        }}>
          <input
            type="text"
            value={userInput}
            onChange={(e) => onInputChange(e.target.value)}
            onKeyPress={onKeyPress}
            placeholder={mobile ? "Pregunta por el clima..." : "Pregunta por Bogotá, Medellín, temperatura, hora..."}
            style={{
              flex: 1,
              padding: "clamp(10px, 2.5vw, 12px)",
              border: "1px solid #ddd",
              borderRadius: "6px",
              fontSize: "clamp(14px, 3vw, 16px)"
            }}
          />
          
                    <button
            onClick={onSendMessage}
            style={{
              padding: "clamp(10px, 2.5vw, 12px) clamp(16px, 3vw, 20px)",
              backgroundColor: "#007bff",
              color: "white",
              border: "none",
              borderRadius: "6px",
              cursor: "pointer",
              fontSize: "clamp(14px, 3vw, 16px)",
              fontWeight: "500",
              whiteSpace: "nowrap",
              minWidth: mobile ? "100%" : "auto"
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.backgroundColor = "#0056b3";
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.backgroundColor = "#007bff";
            }}
          >
            {mobile ? "Enviar 📤" : "Enviar"}
          </button>
        </div>
        
        <div style={{ 
          marginTop: "15px", 
          fontSize: "12px", 
          color: "#888" 
        }}>
          <strong>Puedes preguntar:</strong> clima Bogotá, temperatura Medellín, hora actual
        </div>
      </div>
    </div>
  );
};

export default InteractiveChat;
