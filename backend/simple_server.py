#!/usr/bin/env python3
# Simple test WebSocket server for development
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import uvicorn

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active connections
connections = {}

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, client_id: str = "default", token: str = "default"):
    await websocket.accept()
    
    # Store connection
    if room_id not in connections:
        connections[room_id] = []
    connections[room_id].append(websocket)
    
    try:
        # Send welcome message
        await websocket.send_text(json.dumps({
            "type": "system",
            "message": f"Conectado a la sala {room_id}",
            "sender_id": "system",
            "timestamp": "2024-01-01T00:00:00Z"
        }))
        
        # Keep connection alive and handle messages
        while True:
            try:
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                # Echo message back to all connections in room
                for conn in connections[room_id]:
                    if conn != websocket:  # Don't send back to sender
                        try:
                            await conn.send_text(json.dumps({
                                "type": "user",
                                "message": message_data.get("message", ""),
                                "sender_id": message_data.get("client_id", "unknown"),
                                "timestamp": message_data.get("timestamp", "2024-01-01T00:00:00Z")
                            }))
                        except:
                            pass  # Connection might be closed
                            
            except WebSocketDisconnect:
                break
            except Exception as e:
                print(f"Error: {e}")
                break
                
    except WebSocketDisconnect:
        pass
    finally:
        # Remove connection
        if room_id in connections:
            try:
                connections[room_id].remove(websocket)
                if not connections[room_id]:
                    del connections[room_id]
            except ValueError:
                pass

@app.get("/messages/{room_id}")
async def get_messages(room_id: str, limit: int = 50):
    # Return empty messages for now
    return {"messages": []}

@app.get("/status")
async def get_status():
    return {"status": "running", "rooms": len(connections)}

if __name__ == "__main__":
    print("🚀 Starting simple WebSocket server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
