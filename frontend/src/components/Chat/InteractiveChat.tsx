// src/components/Chat/InteractiveChat.tsx
import React from 'react';

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
  return (
    <div>
      <h2>💬 Chat Clima Colombia</h2>
      <div style={{ 
        border: "1px solid #ddd", 
        borderRadius: "8px", 
        background: "#fafafa",
        padding: "20px",
        minHeight: "100px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center"
      }}>
        <p style={{ 
          margin: "0 0 15px 0", 
          color: "#666", 
          fontSize: "14px" 
        }}>
          💡 Escribe tu pregunta y las respuestas aparecerán en el panel derecho
        </p>
        
        <div style={{ display: "flex", gap: "10px" }}>
          <input
            type="text"
            value={userInput}
            onChange={(e) => onInputChange(e.target.value)}
            onKeyPress={onKeyPress}
            placeholder="Pregunta por Bogotá, Medellín, temperatura, hora..."
            style={{
              flex: 1,
              padding: "12px",
              border: "1px solid #ddd",
              borderRadius: "6px",
              fontSize: "14px"
            }}
          />
          
          <button
            onClick={onSendMessage}
            style={{
              padding: "12px 20px",
              backgroundColor: "#007bff",
              color: "white",
              border: "none",
              borderRadius: "6px",
              cursor: "pointer",
              fontSize: "14px",
              fontWeight: "bold"
            }}
          >
            Enviar 📤
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
