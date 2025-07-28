# app/core/config.py
from typing import Set
import os

class Settings:
    """Configuración de la aplicación"""
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS settings
    CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # WebSocket settings
    VALID_TOKENS: Set[str] = {"abc123", "xyz789", "dev_token"}
    MAX_MESSAGES_PER_ROOM: int = 50
    HEARTBEAT_INTERVAL: int = 20  # seconds
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Advanced WebSocket Router"
    VERSION: str = "2.0.0"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Create global settings instance
settings = Settings()
