"""
WebSocket management service for handling connections and broadcasting
"""
import json
import logging
from typing import List
from fastapi import WebSocket
from app.models.weather import WeatherUpdate, ConnectionMessage

logger = logging.getLogger(__name__)

class WebSocketManager:
    """Manager for WebSocket connections and broadcasting"""
    
    def __init__(self):
        self.observers: List[WebSocket] = []
    
    async def connect_observer(self, websocket: WebSocket):
        """Connect a new observer"""
        await websocket.accept()
        self.observers.append(websocket)
        logger.info(f"✅ Observer connected. Total observers: {len(self.observers)}")
        
        # Send welcome message
        welcome = ConnectionMessage(
            type="connection",
            message="✅ Conectado como Observer - Recibirás datos automáticos de robots",
            timestamp=self._get_timestamp()
        )
        await websocket.send_text(welcome.json())
    
    def disconnect_observer(self, websocket: WebSocket):
        """Disconnect an observer"""
        if websocket in self.observers:
            self.observers.remove(websocket)
        logger.info(f"🔌 Observer disconnected. Remaining: {len(self.observers)}")
    
    async def broadcast_to_observers(self, message: dict):
        """Send message to all connected observers"""
        if not self.observers:
            return
        
        disconnected = []
        message_json = json.dumps(message)
        
        for observer in self.observers:
            try:
                await observer.send_text(message_json)
                logger.info(f"📤 Broadcasted to observer: {message.get('message', '')}")
            except Exception as e:
                logger.warning(f"Failed to send to observer: {e}")
                disconnected.append(observer)
        
        # Clean up disconnected observers
        for obs in disconnected:
            self.disconnect_observer(obs)
    
    def get_observer_count(self) -> int:
        """Get the number of connected observers"""
        return len(self.observers)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from app.utils.helpers import get_colombia_time
        return get_colombia_time().isoformat()

# Global WebSocket manager instance
websocket_manager = WebSocketManager()
