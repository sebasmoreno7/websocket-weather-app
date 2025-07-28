# app/services/websocket_service.py
from typing import Optional, List
from datetime import datetime
from fastapi import WebSocket
from app.models.message import Message, MessageType
from app.models.connection import ClientConnection
from app.services.room_manager import room_manager
from app.core.logging import logger

class WebSocketService:
    """Servicio para manejar operaciones de WebSocket"""
    
    @staticmethod
    async def broadcast_to_room(room_id: str, message: Message, exclude_client_id: Optional[str] = None):
        """Envía un mensaje a todos los clientes de una sala, excepto al excluido"""
        room = room_manager.get_room(room_id)
        if not room:
            logger.warning(f"⚠️ Intento de broadcast a sala inexistente: {room_id}")
            return
        
        disconnected_clients = []
        message_text = message.to_websocket_format()
        
        for client_id, connection in room.connections.items():
            if exclude_client_id and client_id == exclude_client_id:
                continue
                
            try:
                await connection.websocket.send_text(message_text)
                connection.update_activity()
                logger.info(f"📤 Mensaje enviado a {client_id} en {room_id}")
            except Exception as e:
                logger.warning(f"⚠️ Error enviando mensaje a {client_id}: {e}")
                disconnected_clients.append(client_id)
        
        # Remover conexiones desconectadas
        for client_id in disconnected_clients:
            room_manager.remove_connection(room_id, client_id)
    
    @staticmethod
    async def send_welcome_message(room_id: str, client_id: str):
        """Envía mensaje de bienvenida cuando un cliente se conecta"""
        welcome_message = Message(
            content=f"Cliente {client_id} se ha unido a la sala",
            sender_id="SERVER",
            timestamp=datetime.now(),
            message_type=MessageType.SYSTEM,
            room_id=room_id
        )
        
        room_manager.add_message_to_room(room_id, welcome_message)
        await WebSocketService.broadcast_to_room(room_id, welcome_message, exclude_client_id=client_id)
    
    @staticmethod
    async def send_goodbye_message(room_id: str, client_id: str):
        """Envía mensaje de despedida cuando un cliente se desconecta"""
        goodbye_message = Message(
            content=f"Cliente {client_id} ha abandonado la sala",
            sender_id="SERVER",
            timestamp=datetime.now(),
            message_type=MessageType.SYSTEM,
            room_id=room_id
        )
        
        room_manager.add_message_to_room(room_id, goodbye_message)
        await WebSocketService.broadcast_to_room(room_id, goodbye_message, exclude_client_id=client_id)
    
    @staticmethod
    async def handle_user_message(room_id: str, client_id: str, content: str):
        """Procesa un mensaje de usuario"""
        message = Message(
            content=content,
            sender_id=client_id,
            timestamp=datetime.now(),
            message_type=MessageType.USER,
            room_id=room_id
        )
        
        # Guardar en historial
        room_manager.add_message_to_room(room_id, message)
        
        # Broadcast a otros clientes
        await WebSocketService.broadcast_to_room(room_id, message, exclude_client_id=client_id)
        
        # Actualizar última actividad
        room = room_manager.get_room(room_id)
        if room and client_id in room.connections:
            room.connections[client_id].update_activity()

# Global websocket service instance
websocket_service = WebSocketService()
