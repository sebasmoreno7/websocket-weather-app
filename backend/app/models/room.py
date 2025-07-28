# app/models/room.py
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque
from typing import Dict, List
from app.models.connection import ClientConnection
from app.models.message import Message
from app.core.config import settings

@dataclass
class RoomStats:
    room_id: str
    connections: Dict[str, ClientConnection] = field(default_factory=dict)
    message_history: deque = field(default_factory=lambda: deque(maxlen=settings.MAX_MESSAGES_PER_ROOM))
    created_at: datetime = field(default_factory=datetime.now)
    total_messages: int = 0
    last_activity: datetime = field(default_factory=datetime.now)
    
    def add_connection(self, connection: ClientConnection):
        """Agrega una nueva conexión a la sala"""
        self.connections[connection.client_id] = connection
        
    def remove_connection(self, client_id: str) -> bool:
        """Remueve una conexión de la sala. Retorna True si la sala queda vacía"""
        if client_id in self.connections:
            del self.connections[client_id]
        return len(self.connections) == 0
    
    def add_message(self, message: Message):
        """Agrega un mensaje al historial"""
        self.message_history.append(message)
        self.total_messages += 1
        self.last_activity = datetime.now()
    
    def get_messages(self, limit: int = None) -> List[Message]:
        """Obtiene los mensajes del historial"""
        messages = list(self.message_history)
        if limit:
            messages = messages[-limit:]
        return messages
    
    def get_average_connection_time(self) -> float:
        """Calcula el tiempo promedio de conexión"""
        if not self.connections:
            return 0.0
        
        connection_times = [conn.get_connection_duration() for conn in self.connections.values()]
        return sum(connection_times) / len(connection_times)
    
    def to_dict(self) -> dict:
        """Convierte la sala a diccionario para serialización"""
        connections_info = [conn.to_dict() for conn in self.connections.values()]
        
        return {
            "room_id": self.room_id,
            "active_connections": len(self.connections),
            "connections": connections_info,
            "total_messages": self.total_messages,
            "messages_in_history": len(self.message_history),
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "average_connection_time_seconds": round(self.get_average_connection_time(), 2)
        }
