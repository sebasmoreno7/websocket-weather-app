# app/routers/api.py
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime
from app.models.message import Message, MessageType
from app.services.room_manager import room_manager
from app.services.websocket_service import websocket_service
from app.utils.auth import validate_token
from app.core.config import settings
from app.core.logging import logger

router = APIRouter()

@router.get("/")
async def root():
    """Endpoint raíz con información del servidor"""
    return {
        "message": f"🤖 {settings.PROJECT_NAME} is running!",
        "version": settings.VERSION,
        "active_rooms": list(room_manager.get_all_rooms().keys()),
        "total_connections": room_manager.get_total_connections()
    }

@router.get("/messages/{room_id}")
async def get_room_messages(room_id: str, limit: Optional[int] = Query(None, ge=1, le=100)):
    """Obtiene el historial de mensajes de una sala"""
    room = room_manager.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room '{room_id}' not found")
    
    messages = room.get_messages(limit)
    
    # Formatear mensajes para la respuesta
    formatted_messages = [msg.to_dict() for msg in messages]
    
    logger.info(f"📖 Historial solicitado para {room_id}: {len(formatted_messages)} mensajes")
    
    return {
        "room_id": room_id,
        "messages": formatted_messages,
        "total_messages": len(formatted_messages),
        "room_stats": {
            "total_messages_ever": room.total_messages,
            "active_connections": len(room.connections),
            "created_at": room.created_at.isoformat(),
            "last_activity": room.last_activity.isoformat()
        }
    }

@router.get("/status")
async def get_status():
    """Endpoint para obtener el estado detallado de todas las salas"""
    rooms_data = room_manager.get_all_rooms()
    detailed_status = {room_id: room.to_dict() for room_id, room in rooms_data.items()}
    
    return {
        "server_info": {
            "title": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "timestamp": datetime.now().isoformat(),
            "configuration": {
                "max_messages_per_room": settings.MAX_MESSAGES_PER_ROOM,
                "heartbeat_interval": settings.HEARTBEAT_INTERVAL
            }
        },
        "summary": {
            "total_rooms": len(rooms_data),
            "total_connections": room_manager.get_total_connections(),
            "total_messages_all_rooms": room_manager.get_total_messages()
        },
        "rooms": detailed_status
    }

@router.post("/broadcast/{room_id}")
async def server_broadcast(room_id: str, message: str, token: str = Query(...)):
    """Permite al servidor enviar mensajes a una sala específica"""
    if not validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    room = room_manager.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room '{room_id}' not found")
    
    server_message = Message(
        content=message,
        sender_id="SERVER_API",
        timestamp=datetime.now(),
        message_type=MessageType.SYSTEM,
        room_id=room_id
    )
    
    room_manager.add_message_to_room(room_id, server_message)
    await websocket_service.broadcast_to_room(room_id, server_message)
    
    logger.info(f"📢 Mensaje enviado desde API a {room_id}: {message}")
    
    return {
        "success": True,
        "message": "Message sent successfully",
        "room_id": room_id,
        "recipients": len(room.connections)
    }

@router.get("/rooms")
async def list_rooms():
    """Lista todas las salas activas"""
    rooms_data = room_manager.get_all_rooms()
    
    rooms_summary = []
    for room_id, room in rooms_data.items():
        rooms_summary.append({
            "room_id": room_id,
            "active_connections": len(room.connections),
            "total_messages": room.total_messages,
            "created_at": room.created_at.isoformat(),
            "last_activity": room.last_activity.isoformat()
        })
    
    return {
        "total_rooms": len(rooms_data),
        "rooms": rooms_summary
    }

@router.get("/rooms/{room_id}/connections")
async def get_room_connections(room_id: str):
    """Obtiene las conexiones activas de una sala"""
    room = room_manager.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room '{room_id}' not found")
    
    connections = [conn.to_dict() for conn in room.connections.values()]
    
    return {
        "room_id": room_id,
        "active_connections": len(connections),
        "connections": connections
    }
