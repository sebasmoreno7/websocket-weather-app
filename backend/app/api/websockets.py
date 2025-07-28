"""
WebSocket routes for real-time communication
"""
import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_manager import websocket_manager
from app.services.chat_service import ChatService

logger = logging.getLogger(__name__)

router = APIRouter()

@router.websocket("/ws/observer")
async def websocket_observer(websocket: WebSocket):
    """WebSocket endpoint for observers"""
    await websocket_manager.connect_observer(websocket)
    
    try:
        while True:
            # Wait for messages from client (chat)
            data = await websocket.receive_text()
            logger.info(f"💬 Chat message from observer: {data}")
            
            try:
                # Try to parse as JSON
                message_data = json.loads(data)
                content = message_data.get("content", data)
            except json.JSONDecodeError:
                content = data
            
            # Handle chat message
            response = await ChatService.handle_chat_message(content)
            await websocket.send_text(json.dumps(response))
                
    except WebSocketDisconnect:
        websocket_manager.disconnect_observer(websocket)
    except Exception as e:
        logger.error(f"❌ Error in observer WebSocket: {e}")
        websocket_manager.disconnect_observer(websocket)
