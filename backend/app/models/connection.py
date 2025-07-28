# app/models/connection.py
from dataclasses import dataclass, field
from datetime import datetime
from fastapi import WebSocket

@dataclass
class ClientConnection:
    websocket: WebSocket
    client_id: str
    room_id: str
    connected_at: datetime
    last_activity: datetime = field(default_factory=datetime.now)
    
    def update_activity(self):
        """Actualiza la última actividad del cliente"""
        self.last_activity = datetime.now()
    
    def get_connection_duration(self) -> float:
        """Retorna la duración de la conexión en segundos"""
        return (datetime.now() - self.connected_at).total_seconds()
    
    def to_dict(self) -> dict:
        """Convierte la conexión a diccionario para serialización"""
        return {
            "client_id": self.client_id,
            "room_id": self.room_id,
            "connected_at": self.connected_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "connection_duration_seconds": self.get_connection_duration()
        }
