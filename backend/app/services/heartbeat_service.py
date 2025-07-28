# app/services/heartbeat_service.py
import asyncio
from datetime import datetime
from app.models.message import Message, MessageType
from app.services.room_manager import room_manager
from app.services.websocket_service import websocket_service
from app.core.config import settings
from app.core.logging import logger

class HeartbeatService:
    """Servicio para enviar heartbeats automáticos"""
    
    def __init__(self):
        self.running = False
    
    async def start_heartbeat(self):
        """Inicia el servicio de heartbeat"""
        if self.running:
            return
        
        self.running = True
        logger.info(f"💓 Servicio de heartbeat iniciado (intervalo: {settings.HEARTBEAT_INTERVAL}s)")
        
        while self.running:
            await asyncio.sleep(settings.HEARTBEAT_INTERVAL)
            await self._send_heartbeat()
    
    async def stop_heartbeat(self):
        """Detiene el servicio de heartbeat"""
        self.running = False
        logger.info("💓 Servicio de heartbeat detenido")
    
    async def _send_heartbeat(self):
        """Envía heartbeat a todas las salas de observers"""
        observer_room = room_manager.get_room("observer")
        if not observer_room or not observer_room.connections:
            return
        
        heartbeat_message = Message(
            content="💓 Server heartbeat - System operational",
            sender_id="SERVER",
            timestamp=datetime.now(),
            message_type=MessageType.HEARTBEAT,
            room_id="observer"
        )
        
        room_manager.add_message_to_room("observer", heartbeat_message)
        await websocket_service.broadcast_to_room("observer", heartbeat_message)
        logger.info("💓 Heartbeat enviado a observers")
    
    async def send_custom_heartbeat(self, room_id: str, message: str = None):
        """Envía un heartbeat personalizado a una sala específica"""
        if not message:
            message = f"💓 Custom heartbeat for {room_id}"
        
        heartbeat_message = Message(
            content=message,
            sender_id="SERVER",
            timestamp=datetime.now(),
            message_type=MessageType.HEARTBEAT,
            room_id=room_id
        )
        
        room_manager.add_message_to_room(room_id, heartbeat_message)
        await websocket_service.broadcast_to_room(room_id, heartbeat_message)
        logger.info(f"💓 Heartbeat personalizado enviado a {room_id}")

# Global heartbeat service instance
heartbeat_service = HeartbeatService()
