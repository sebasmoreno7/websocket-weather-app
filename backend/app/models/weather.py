"""
Pydantic models for weather data and API responses
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class WeatherData(BaseModel):
    """Weather data model"""
    city: str
    name: str
    temperature: int
    humidity: int
    description: str
    time: str
    emoji: str
    source: str
    real_data: bool
    altitude: Optional[int] = None

class ChatResponse(BaseModel):
    """Chat response model"""
    type: str
    message: str
    timestamp: str

class WeatherUpdate(BaseModel):
    """Weather update message model"""
    type: str
    robot: str
    data: WeatherData
    message: str

class ConnectionMessage(BaseModel):
    """WebSocket connection message model"""
    type: str
    message: str
    timestamp: str

class ServerStatus(BaseModel):
    """Server status model"""
    server: str
    status: str
    timestamp: str
    observers_connected: int
    robot_tasks: list
    uptime: str

class RootResponse(BaseModel):
    """Root endpoint response model"""
    message: str
    version: str
    observers_connected: int
    robots_running: int
    status: str
