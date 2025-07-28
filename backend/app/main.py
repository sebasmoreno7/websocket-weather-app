# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import logger
from app.routers import websocket, api
from app.services.heartbeat_service import heartbeat_service
import asyncio

def create_application() -> FastAPI:
    """Factory function para crear la aplicación FastAPI"""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Advanced WebSocket Router with room management, message history, and real-time communication"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(websocket.router, tags=["WebSocket"])
    app.include_router(api.router, prefix="/api/v1", tags=["API"])

    return app

# Create app instance
app = create_application()

@app.on_event("startup")
async def startup_event():
    """Eventos que se ejecutan al iniciar la aplicación"""
    logger.info("🚀 Iniciando servidor WebSocket avanzado...")
    logger.info(f"📋 Proyecto: {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"🔐 Tokens válidos configurados: {len(settings.VALID_TOKENS)}")
    logger.info(f"💓 Heartbeat configurado cada {settings.HEARTBEAT_INTERVAL} segundos")
    logger.info(f"📨 Máximo de mensajes por sala: {settings.MAX_MESSAGES_PER_ROOM}")
    
    # Iniciar heartbeat en segundo plano
    asyncio.create_task(heartbeat_service.start_heartbeat())
    
    logger.info("✅ Servidor iniciado correctamente")

@app.on_event("shutdown")
async def shutdown_event():
    """Eventos que se ejecutan al cerrar la aplicación"""
    logger.info("🛑 Cerrando servidor...")
    
    # Detener heartbeat
    await heartbeat_service.stop_heartbeat()
    
    logger.info("✅ Servidor cerrado correctamente")
