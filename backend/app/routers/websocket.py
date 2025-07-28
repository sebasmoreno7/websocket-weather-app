# app/routers/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, HTTPException
from datetime import datetime
from app.models.connection import ClientConnection
from app.services.room_manager import room_manager
from app.services.websocket_service import websocket_service
from app.utils.auth import validate_token, validate_client_id
from app.core.logging import logger

router = APIRouter()

@router.websocket("/ws/{room_id}")
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
    
    # Validar client_id
    if not validate_client_id(client_id):
        logger.warning(f"🔒 Client ID inválido: {client_id}")
        await websocket.close(code=4003, reason="Invalid client_id")
        return
    
    await websocket.accept()
    
    # Crear conexión
    connection = ClientConnection(
        websocket=websocket,
        client_id=client_id,
        room_id=room_id,
        connected_at=datetime.now()
    )
    
    # Agregar conexión al room manager
    if not room_manager.add_connection(room_id, connection):
        await websocket.close(code=4002, reason="Client ID already exists in room")
        return
    
    # Enviar mensaje de bienvenida
    await websocket_service.send_welcome_message(room_id, client_id)

    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"📨 Mensaje recibido de {client_id} en {room_id}: {data}")
            
            # Procesar mensaje del usuario
            await websocket_service.handle_user_message(room_id, client_id, data)
                    
    except WebSocketDisconnect:
        logger.info(f"🔌 Conexión desconectada: {client_id} de room {room_id}")
        
        # Enviar mensaje de despedida
        await websocket_service.send_goodbye_message(room_id, client_id)
        
        # Remover conexión
        room_manager.remove_connection(room_id, client_id)
        
    except Exception as e:
        logger.error(f"❌ Error inesperado en WebSocket para {client_id}: {e}")
        room_manager.remove_connection(room_id, client_id)
