"""
API routes for the weather application
"""
from fastapi import APIRouter
from app.models.weather import RootResponse, ServerStatus
from app.services.websocket_manager import websocket_manager
from app.services.robot_service import robot_service
from app.core.settings import settings
from app.utils.helpers import get_colombia_time

router = APIRouter()

@router.get("/", response_model=RootResponse)
async def root():
    """Root endpoint with server information"""
    return RootResponse(
        message=f"🌦️ {settings.APP_NAME}",
        version=settings.VERSION,
        observers_connected=websocket_manager.get_observer_count(),
        robots_running=robot_service.get_robot_count(),
        status="active"
    )

@router.get("/status", response_model=ServerStatus)
async def get_status():
    """Get server status information"""
    return ServerStatus(
        server=settings.APP_NAME,
        status="running",
        timestamp=get_colombia_time().isoformat(),
        observers_connected=websocket_manager.get_observer_count(),
        robot_tasks=robot_service.get_running_robots(),
        uptime="running"
    )
