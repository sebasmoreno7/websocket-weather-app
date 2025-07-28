# app/services/room_manager.py
from typing import Dict, Optional, List
from datetime import datetime
from app.models.room import RoomStats
from app.models.connection import ClientConnection
from app.models.message import Message, MessageType
from app.core.logging import logger

class RoomManager:
    """Gestor centralizado de salas y conexiones"""
    
    def __init__(self):
        self.rooms: Dict[str, RoomStats] = {}
    
    def create_room(self, room_id: str) -> RoomStats:
        """Crea una nueva sala si no existe"""
        if room_id not in self.rooms:
            self.rooms[room_id] = RoomStats(room_id=room_id)
            logger.info(f"🏠 Nueva sala creada: {room_id}")
        return self.rooms[room_id]
    
    def get_room(self, room_id: str) -> Optional[RoomStats]:
        """Obtiene una sala por ID"""
        return self.rooms.get(room_id)
    
    def get_all_rooms(self) -> Dict[str, RoomStats]:
        """Obtiene todas las salas"""
        return self.rooms.copy()
    
    def add_connection(self, room_id: str, connection: ClientConnection) -> bool:
        """Agrega una conexión a una sala"""
        # Verificar si el client_id ya existe en la sala
        if room_id in self.rooms and connection.client_id in self.rooms[room_id].connections:
            logger.warning(f"⚠️ Client ID {connection.client_id} ya existe en {room_id}")
            return False
        
        # Crear sala si no existe
        room = self.create_room(room_id)
        room.add_connection(connection)
        
        logger.info(f"✅ Nueva conexión: {connection.client_id} en room {room_id}")
        logger.info(f"📊 Conexiones activas en {room_id}: {len(room.connections)}")
        return True
    
    def remove_connection(self, room_id: str, client_id: str) -> bool:
        """Remueve una conexión de una sala"""
        if room_id not in self.rooms:
            return False
        
        room = self.rooms[room_id]
        is_empty = room.remove_connection(client_id)
        
        logger.info(f"🗑️ Cliente {client_id} removido de {room_id}")
        
        # Si la sala queda vacía, la eliminamos
        if is_empty:
            del self.rooms[room_id]
            logger.info(f"🏠 Sala {room_id} eliminada (sin conexiones)")
        
        return True
    
    def add_message_to_room(self, room_id: str, message: Message):
        """Agrega un mensaje al historial de una sala"""
        room = self.get_room(room_id)
        if room:
            room.add_message(message)
            logger.info(f"📝 Mensaje guardado en historial de {room_id}: {message.sender_id} -> {message.content[:50]}...")
    
    def get_room_messages(self, room_id: str, limit: Optional[int] = None) -> List[Message]:
        """Obtiene los mensajes de una sala"""
        room = self.get_room(room_id)
        if room:
            return room.get_messages(limit)
        return []
    
    def get_total_connections(self) -> int:
        """Obtiene el total de conexiones activas"""
        return sum(len(room.connections) for room in self.rooms.values())
    
    def get_total_messages(self) -> int:
        """Obtiene el total de mensajes enviados"""
        return sum(room.total_messages for room in self.rooms.values())

# Global room manager instance
room_manager = RoomManager()
