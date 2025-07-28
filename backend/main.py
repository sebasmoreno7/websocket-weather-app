# main.py
import asyncio
import json
import random
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Real WebSocket Weather Server", version="2.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store observer connections
observers: List[WebSocket] = []
robot_tasks = {}

def get_colombia_time():
    """Get current time in Colombia timezone (UTC-5)"""
    colombia_tz = timezone(timedelta(hours=-5))
    return datetime.now(colombia_tz)

async def get_weather_data(city: str):
    """Get simulated weather data for each city"""
    if city == "bogota":
        temp = random.randint(14, 22)
        humidity = random.randint(60, 85)
        emoji = "🏔️"
    else:  # medellin
        temp = random.randint(20, 30)
        humidity = random.randint(55, 75)
        emoji = "🌺"
    
    colombia_time = get_colombia_time()
    time = colombia_time.strftime("%H:%M:%S")
    
    return {
        "city": city,
        "temperature": temp,
        "humidity": humidity,
        "timestamp": colombia_time.isoformat(),
        "time": time,
        "emoji": emoji
    }

async def broadcast_to_observers(message: dict):
    """Send message to all connected observers"""
    if not observers:
        return
    
    disconnected = []
    for observer in observers:
        try:
            await observer.send_text(json.dumps(message))
            logger.info(f"📤 Broadcasted to observer: {message.get('message', '')}")
        except:
            disconnected.append(observer)
    
    # Clean up disconnected observers
    for obs in disconnected:
        if obs in observers:
            observers.remove(obs)
            logger.info("🗑️ Removed disconnected observer")

async def robot_worker(city: str, interval: int):
    """Background task simulating robot sending weather data"""
    while True:
        try:
            weather = await get_weather_data(city)
            
            message = {
                "type": "weather_update",
                "robot": f"robot_{city}",
                "data": weather,
                "message": f"{weather['emoji']} Robot {city.title()}: {weather['temperature']}°C - {weather['time']}"
            }
            
            await broadcast_to_observers(message)
            logger.info(f"🤖 Robot {city} sent data: {weather['temperature']}°C")
            
            await asyncio.sleep(interval)
            
        except asyncio.CancelledError:
            logger.info(f"🛑 Robot {city} task cancelled")
            break
        except Exception as e:
            logger.error(f"❌ Error in robot {city}: {e}")
            await asyncio.sleep(interval)

async def handle_chat_message(content: str):
    """Handle chat messages and provide weather responses"""
    content_lower = content.lower()
    
    if any(word in content_lower for word in ["temperatura", "temperature", "clima", "weather"]):
        if "bogota" in content_lower or "bogotá" in content_lower:
            weather = await get_weather_data("bogota")
            return {
                "type": "chat_response",
                "message": f"🏔️ Bogotá: {weather['temperature']}°C, Humedad: {weather['humidity']}% - {weather['time']}",
                "timestamp": get_colombia_time().isoformat()
            }
        elif "medellin" in content_lower or "medellín" in content_lower:
            weather = await get_weather_data("medellin")
            return {
                "type": "chat_response", 
                "message": f"🌺 Medellín: {weather['temperature']}°C, Humedad: {weather['humidity']}% - {weather['time']}",
                "timestamp": get_colombia_time().isoformat()
            }
        else:
            # Return both cities
            bogota = await get_weather_data("bogota")
            medellin = await get_weather_data("medellin")
            return {
                "type": "chat_response",
                "message": f"🏔️ Bogotá: {bogota['temperature']}°C | 🌺 Medellín: {medellin['temperature']}°C",
                "timestamp": get_colombia_time().isoformat()
            }
    elif "hora" in content_lower or "time" in content_lower:
        colombia_time = get_colombia_time()
        current_time = colombia_time.strftime("%H:%M:%S")
        return {
            "type": "chat_response",
            "message": f"🕐 Hora actual en Colombia: {current_time}",
            "timestamp": colombia_time.isoformat()
        }
    else:
        return {
            "type": "chat_response",
            "message": "🤖 Puedes preguntar sobre:\n• Clima de Bogotá o Medellín\n• Temperatura actual\n• Hora actual",
            "timestamp": get_colombia_time().isoformat()
        }

@app.on_event("startup")
async def startup_event():
    """Start robot background tasks"""
    robot_tasks["bogota"] = asyncio.create_task(robot_worker("bogota", 15))
    robot_tasks["medellin"] = asyncio.create_task(robot_worker("medellin", 20))
    logger.info("🚀 Robot background tasks started - Bogotá (15s), Medellín (20s)")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up robot tasks"""
    for task in robot_tasks.values():
        task.cancel()
    logger.info("🛑 Robot background tasks stopped")

@app.get("/")
async def root():
    return {
        "message": "🌦️ Real WebSocket Weather Server",
        "version": "2.0.0",
        "observers_connected": len(observers),
        "robots_running": len(robot_tasks),
        "status": "active"
    }

@app.get("/status")
async def get_status():
    return {
        "server": "Real WebSocket Weather Server",
        "status": "running",
        "timestamp": get_colombia_time().isoformat(),
        "observers_connected": len(observers),
        "robot_tasks": list(robot_tasks.keys()),
        "uptime": "running"
    }

@app.websocket("/ws/observer")
async def websocket_observer(websocket: WebSocket):
    await websocket.accept()
    observers.append(websocket)
    
    logger.info(f"✅ Observer connected. Total observers: {len(observers)}")
    
    # Send welcome message
    welcome = {
        "type": "connection",
        "message": "✅ Conectado como Observer - Recibirás datos automáticos de robots",
        "timestamp": get_colombia_time().isoformat()
    }
    await websocket.send_text(json.dumps(welcome))
    
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
            response = await handle_chat_message(content)
            await websocket.send_text(json.dumps(response))
                
    except WebSocketDisconnect:
        if websocket in observers:
            observers.remove(websocket)
        logger.info(f"🔌 Observer disconnected. Remaining: {len(observers)}")
    except Exception as e:
        logger.error(f"❌ Error in observer WebSocket: {e}")
        if websocket in observers:
            observers.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting Real WebSocket Weather Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
