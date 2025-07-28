"""
Robot service for background weather data collection tasks
"""
import asyncio
import logging
from typing import Dict
from app.services.weather_service import WeatherService
from app.services.websocket_manager import websocket_manager
from app.models.weather import WeatherUpdate
from app.core.settings import settings

logger = logging.getLogger(__name__)

class RobotService:
    """Service for managing robot background tasks"""
    
    def __init__(self):
        self.robot_tasks: Dict[str, asyncio.Task] = {}
    
    async def start_all_robots(self):
        """Start all robot background tasks"""
        for city, interval in settings.ROBOT_INTERVALS.items():
            self.robot_tasks[city] = asyncio.create_task(
                self._robot_worker(city, interval)
            )
        logger.info(f"🚀 Robot background tasks started - {', '.join([f'{city.title()} ({interval}s)' for city, interval in settings.ROBOT_INTERVALS.items()])}")
    
    async def stop_all_robots(self):
        """Stop all robot background tasks"""
        for task in self.robot_tasks.values():
            task.cancel()
        self.robot_tasks.clear()
        logger.info("🛑 Robot background tasks stopped")
    
    def get_running_robots(self) -> list:
        """Get list of running robot cities"""
        return list(self.robot_tasks.keys())
    
    def get_robot_count(self) -> int:
        """Get number of running robots"""
        return len(self.robot_tasks)
    
    async def _robot_worker(self, city: str, interval: int):
        """Background task simulating robot sending weather data"""
        while True:
            try:
                weather = await WeatherService.get_weather_data(city)
                
                message = WeatherUpdate(
                    type="weather_update",
                    robot=f"robot_{city}",
                    data=weather,
                    message=f"{weather.emoji} Robot {weather.name}: {weather.temperature}°C, {weather.description} - {weather.time} ({weather.source})"
                )
                
                await websocket_manager.broadcast_to_observers(message.dict())
                logger.info(f"🤖 Robot {city} sent data: {weather.temperature}°C")
                
                await asyncio.sleep(interval)
                
            except asyncio.CancelledError:
                logger.info(f"🛑 Robot {city} task cancelled")
                break
            except Exception as e:
                logger.error(f"❌ Error in robot {city}: {e}")
                await asyncio.sleep(interval)

# Global robot service instance
robot_service = RobotService()
