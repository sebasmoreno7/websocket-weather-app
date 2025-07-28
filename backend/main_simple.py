# main.py - Versión Simple sin Login
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import logging
import asyncio
import json
from datetime import datetime
from collections import deque
from dataclasses import dataclass, field

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Simple WebSocket Server", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
MAX_MESSAGES_PER_ROOM = 50

@dataclass
class Message:
    content: str
    sender: str
    timestamp: str
    type: str = "user"

@dataclass
class Room:
    connections: Dict[str, WebSocket] = field(default_factory=dict)
    messages: deque = field(default_factory=lambda: deque(maxlen=MAX_MESSAGES_PER_ROOM))

# Global state
rooms: Dict[str, Room] = {}

async def broadcast_to_room(room_id: str, message: dict, exclude_sender: str = None):
    """Send message to all clients in a room"""
    if room_id not in rooms:
        return
    
    disconnected = []
    for client_id, websocket in rooms[room_id].connections.items():
        if client_id == exclude_sender:
            continue
            
        try:
            await websocket.send_text(json.dumps(message))
        except:
            disconnected.append(client_id)
    
    # Clean up disconnected clients
    for client_id in disconnected:
        if client_id in rooms[room_id].connections:
            del rooms[room_id].connections[client_id]
            logger.info(f"Removed disconnected client {client_id} from {room_id}")

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    
    # Generate simple client ID
    client_id = f"client_{len(rooms.get(room_id, Room()).connections) + 1}_{int(datetime.now().timestamp())}"
    
    # Create room if it doesn't exist
    if room_id not in rooms:
        rooms[room_id] = Room()
        logger.info(f"Created room: {room_id}")
    
    # Add client to room
    rooms[room_id].connections[client_id] = websocket
    logger.info(f"Client {client_id} connected to room {room_id}")
    
    # Send welcome message
    welcome_msg = {
        "content": f"¡Bienvenido a la sala {room_id}!",
        "sender": "Sistema",
        "timestamp": datetime.now().isoformat(),
        "type": "system"
    }
    
    try:
        await websocket.send_text(json.dumps(welcome_msg))
        
        # Send recent messages
        for msg in list(rooms[room_id].messages):
            await websocket.send_text(json.dumps({
                "content": msg.content,
                "sender": msg.sender,
                "timestamp": msg.timestamp,
                "type": msg.type
            }))
    except:
        pass
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            
            # Create message object
            message = Message(
                content=data,
                sender=client_id,
                timestamp=datetime.now().isoformat(),
                type="user"
            )
            
            # Store message
            rooms[room_id].messages.append(message)
            
            # Broadcast to other clients
            msg_dict = {
                "content": message.content,
                "sender": message.sender,
                "timestamp": message.timestamp,
                "type": message.type
            }
            
            await broadcast_to_room(room_id, msg_dict, exclude_sender=client_id)
            
    except WebSocketDisconnect:
        logger.info(f"Client {client_id} disconnected from {room_id}")
    except Exception as e:
        logger.error(f"Error with client {client_id}: {e}")
    finally:
        # Clean up
        if room_id in rooms and client_id in rooms[room_id].connections:
            del rooms[room_id].connections[client_id]
            
        # Send goodbye message
        goodbye_msg = {
            "content": f"Cliente {client_id} ha salido de la sala",
            "sender": "Sistema",
            "timestamp": datetime.now().isoformat(),
            "type": "system"
        }
        await broadcast_to_room(room_id, goodbye_msg)
        
        # Remove room if empty
        if room_id in rooms and not rooms[room_id].connections:
            del rooms[room_id]
            logger.info(f"Removed empty room: {room_id}")

@app.get("/")
async def root():
    return {
        "message": "🤖 Simple WebSocket Server",
        "version": "1.0.0",
        "active_rooms": len(rooms),
        "total_connections": sum(len(room.connections) for room in rooms.values())
    }

@app.get("/rooms/{room_id}/messages")
async def get_messages(room_id: str):
    """Get messages from a room"""
    if room_id not in rooms:
        return {"messages": []}
    
    messages = []
    for msg in rooms[room_id].messages:
        messages.append({
            "content": msg.content,
            "sender": msg.sender,
            "timestamp": msg.timestamp,
            "type": msg.type
        })
    
    return {"messages": messages}

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting Simple WebSocket Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
