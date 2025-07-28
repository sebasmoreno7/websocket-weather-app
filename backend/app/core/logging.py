# app/core/logging.py
import logging
from app.core.config import settings

def setup_logging():
    """Configura el sistema de logging de la aplicación"""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format=settings.LOG_FORMAT
    )
    
    # Create logger for the application
    logger = logging.getLogger("websocket_server")
    return logger

# Global logger instance
logger = setup_logging()
