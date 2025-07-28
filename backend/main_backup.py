# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="WebSocket Weather Server", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active connections by room
rooms: Dict[str, List[WebSocket]] = {}
    
    # Remover conexiones desconectadas
    for client_id in disconnected_clients:
        remove_client_from_room(room_id, client_id)

def remove_client_from_room(room_id: str, client_id: str):
    """Remueve un cliente de una sala"""
    if room_id in rooms and client_id in rooms[room_id].connections:
        del rooms[room_id].connections[client_id]
        logger.info(f"🗑️ Cliente {client_id} removido de {room_id}")
        
        # Si la sala queda vacía, la removemos
        if not rooms[room_id].connections:
            del rooms[room_id]
            logger.info(f"🏠 Sala {room_id} eliminada (sin conexiones)")

async def send_heartbeat():
    """Envía heartbeat a todas las salas de observers"""
    while True:
        await asyncio.sleep(HEARTBEAT_INTERVAL)
        
        if "observer" in rooms:
            heartbeat_message = Message(
                content="💓 Server heartbeat - System operational",
                sender_id="SERVER",
                timestamp=datetime.now(),
                message_type=MessageType.HEARTBEAT,
                room_id="observer"
            )
            
            add_message_to_history("observer", heartbeat_message)
            await broadcast_to_room("observer", heartbeat_message)
            logger.info("💓 Heartbeat enviado a observers")

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    room_id: str,
    client_id: str = Query(..., description="Identificador único del cliente"),
    token: str = Query(..., description="Token de autenticación")
):
    # Validar token
    if not validate_token(token):
        logger.warning(f"🔒 Acceso denegado para {client_id} en {room_id}: token inválido")
        await websocket.close(code=4001, reason="Invalid token")
        return
    
    # Validar que client_id no esté ya en uso en esta sala
    if room_id in rooms and client_id in rooms[room_id].connections:
        logger.warning(f"⚠️ Client ID {client_id} ya existe en {room_id}")
        await websocket.close(code=4002, reason="Client ID already exists in room")
        return
    
    await websocket.accept()
    logger.info(f"✅ Nueva conexión WebSocket: {client_id} en room {room_id}")
    
    # Crear sala si no existe
    if room_id not in rooms:
        rooms[room_id] = RoomStats(room_id=room_id)
        logger.info(f"🏠 Nueva sala creada: {room_id}")
    
    # Agregar conexión
    connection = ClientConnection(
        websocket=websocket,
        client_id=client_id,
        room_id=room_id,
        connected_at=datetime.now()
    )
    rooms[room_id].connections[client_id] = connection
    
    logger.info(f"📊 Conexiones activas en {room_id}: {len(rooms[room_id].connections)}")
    
    # Mensaje de bienvenida
    welcome_message = Message(
        content=f"Cliente {client_id} se ha unido a la sala",
        sender_id="SERVER",
        timestamp=datetime.now(),
        message_type=MessageType.SYSTEM,
        room_id=room_id
    )
    add_message_to_history(room_id, welcome_message)
    await broadcast_to_room(room_id, welcome_message, exclude_client_id=client_id)

    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"� Mensaje recibido de {client_id} en {room_id}: {data}")
            
            # Crear mensaje
            message = Message(
                content=data,
                sender_id=client_id,
                timestamp=datetime.now(),
                message_type=MessageType.USER,
                room_id=room_id
            )
            
            # Guardar en historial
            add_message_to_history(room_id, message)
            
            # Broadcast a otros clientes
            await broadcast_to_room(room_id, message, exclude_client_id=client_id)
            
            # Actualizar última actividad
            connection.last_activity = datetime.now()
                    
    except WebSocketDisconnect:
        logger.info(f"🔌 Conexión desconectada: {client_id} de room {room_id}")
        
        # Mensaje de despedida
        goodbye_message = Message(
            content=f"Cliente {client_id} ha abandonado la sala",
            sender_id="SERVER",
            timestamp=datetime.now(),
            message_type=MessageType.SYSTEM,
            room_id=room_id
        )
        add_message_to_history(room_id, goodbye_message)
        await broadcast_to_room(room_id, goodbye_message, exclude_client_id=client_id)
        
        remove_client_from_room(room_id, client_id)
        
    except Exception as e:
        logger.error(f"❌ Error inesperado en WebSocket para {client_id}: {e}")
        remove_client_from_room(room_id, client_id)

@app.get("/")
async def root():
    return {
        "message": "🤖 Advanced WebSocket Server is running!",
        "version": "2.0.0", 
        "active_rooms": list(rooms.keys()),
        "total_connections": sum(len(room.connections) for room in rooms.values())
    }

@app.get("/messages/{room_id}")
async def get_room_messages(room_id: str, limit: Optional[int] = Query(None, ge=1, le=100)):
    """Obtiene el historial de mensajes de una sala"""
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail=f"Room '{room_id}' not found")
    
    room = rooms[room_id]
    messages = list(room.message_history)
    
    # Aplicar límite si se especifica
    if limit:
        messages = messages[-limit:]
    
    # Formatear mensajes para la respuesta
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "content": msg.content,
            "sender_id": msg.sender_id,
            "timestamp": msg.timestamp.isoformat(),
            "message_type": msg.message_type.value,
            "room_id": msg.room_id
        })
    
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

@app.get("/status")
async def get_status():
    """Endpoint para obtener el estado detallado de todas las salas"""
    detailed_status = {}
    
    for room_id, room in rooms.items():
        connections_info = []
        connection_times = []
        
        for client_id, connection in room.connections.items():
            connection_duration = datetime.now() - connection.connected_at
            connection_times.append(connection_duration.total_seconds())
            
            connections_info.append({
                "client_id": client_id,
                "connected_at": connection.connected_at.isoformat(),
                "last_activity": connection.last_activity.isoformat(),
                "connection_duration_seconds": connection_duration.total_seconds()
            })
        
        # Calcular tiempo promedio de conexión
        avg_connection_time = sum(connection_times) / len(connection_times) if connection_times else 0
        
        detailed_status[room_id] = {
            "active_connections": len(room.connections),
            "connections": connections_info,
            "total_messages": room.total_messages,
            "messages_in_history": len(room.message_history),
            "created_at": room.created_at.isoformat(),
            "last_activity": room.last_activity.isoformat(),
            "average_connection_time_seconds": round(avg_connection_time, 2)
        }
    
    return {
        "server_info": {
            "title": "Advanced WebSocket Router",
            "version": "2.0.0",
            "timestamp": datetime.now().isoformat(),
            "uptime_info": "Check individual room creation times"
        },
        "summary": {
            "total_rooms": len(rooms),
            "total_connections": sum(len(room.connections) for room in rooms.values()),
            "total_messages_all_rooms": sum(room.total_messages for room in rooms.values())
        },
        "rooms": detailed_status
    }

@app.post("/broadcast/{room_id}")
async def server_broadcast(room_id: str, message: str, token: str = Query(...)):
    """Permite al servidor enviar mensajes a una sala específica"""
    if not validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail=f"Room '{room_id}' not found")
    
    server_message = Message(
        content=message,
        sender_id="SERVER_API",
        timestamp=datetime.now(),
        message_type=MessageType.SYSTEM,
        room_id=room_id
    )
    
    add_message_to_history(room_id, server_message)
    await broadcast_to_room(room_id, server_message)
    
    logger.info(f"📢 Mensaje enviado desde API a {room_id}: {message}")
    
    return {
        "success": True,
        "message": "Message sent successfully",
        "room_id": room_id,
        "recipients": len(rooms[room_id].connections)
    }

@app.on_event("startup")
async def startup_event():
    """Inicia tareas en segundo plano cuando arranca el servidor"""
    logger.info("🚀 Iniciando servidor WebSocket avanzado...")
    logger.info(f"🔐 Tokens válidos configurados: {len(VALID_TOKENS)}")
    logger.info(f"💓 Heartbeat configurado cada {HEARTBEAT_INTERVAL} segundos")
    
    # Iniciar heartbeat en segundo plano
    asyncio.create_task(send_heartbeat())

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Iniciando servidor WebSocket...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
