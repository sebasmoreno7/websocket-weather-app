"""
Configuration settings for the Weather WebSocket Server
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # API Configuration
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "demo_key_for_testing")
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000", 
        "http://127.0.0.1:3000"
    ]
    
    # Application Info
    APP_NAME: str = "Real WebSocket Weather Server"
    VERSION: str = "2.0.0"
    
    # Robot Configuration
    ROBOT_INTERVALS: Dict[str, int] = {
        "bogota": 15,
        "medellin": 20
    }
    
    # City Coordinates for OpenWeatherMap API
    CITIES: Dict[str, Dict[str, Any]] = {
        "bogota": {
            "lat": 4.7110, 
            "lon": -74.0721, 
            "name": "Bogotá", 
            "emoji": "🏔️",
            "altitude": 2640,
            "avg_temp_range": "14-20°C"
        },
        "medellin": {
            "lat": 6.2442, 
            "lon": -75.5812, 
            "name": "Medellín", 
            "emoji": "🌺",
            "altitude": 1495,
            "avg_temp_range": "20-28°C"
        }
    }

# Global settings instance
settings = Settings()
