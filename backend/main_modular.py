"""
FastAPI Weather WebSocket Server - Modular Architecture
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import application components
from app.core.settings import settings
from app.api.routes import router as api_router
from app.api.websockets import router as websocket_router
from app.services.robot_service import robot_service

# Configure logging  
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.VERSION}...")
    await robot_service.start_all_robots()
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down application...")
    await robot_service.stop_all_robots()

def create_app() -> FastAPI:
    """Application factory"""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        lifespan=lifespan
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(api_router)
    app.include_router(websocket_router)
    
    return app

# Create the FastAPI app
app = create_app()

if __name__ == "__main__":
    import uvicorn
    logger.info(f"🚀 Starting {settings.APP_NAME}...")
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        log_level="info",
        reload=True
    )
