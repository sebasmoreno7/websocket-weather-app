# app/models/message.py
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class MessageType(Enum):
    USER = "user"
    SYSTEM = "system"
    HEARTBEAT = "heartbeat"

@dataclass
class Message:
    content: str
    sender_id: str
    timestamp: datetime
    message_type: MessageType = MessageType.USER
    room_id: str = ""
    
    def to_dict(self) -> dict:
        """Convierte el mensaje a diccionario para serialización"""
        return {
            "content": self.content,
            "sender_id": self.sender_id,
            "timestamp": self.timestamp.isoformat(),
            "message_type": self.message_type.value,
            "room_id": self.room_id
        }
    
    def to_websocket_format(self) -> str:
        """Formato del mensaje para envío por WebSocket"""
        return f"{self.sender_id}: {self.content}"
