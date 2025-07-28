"""
Weather data service for fetching real and simulated weather data
"""
import aiohttp
import random
import logging
from typing import Optional
from app.core.settings import settings
from app.models.weather import WeatherData
from app.utils.helpers import get_colombia_time

logger = logging.getLogger(__name__)

class WeatherService:
    """Service for weather data operations"""
    
    @staticmethod
    async def get_real_weather_data(city: str) -> Optional[WeatherData]:
        """Get real weather data from OpenWeatherMap API"""
        if city not in settings.CITIES:
            return None
        
        city_info = settings.CITIES[city]
        
        # If no real API key, return simulated data
        if settings.OPENWEATHER_API_KEY == "demo_key_for_testing":
            logger.info(f"Using simulated data for {city} (no real API key configured)")
            return await WeatherService.get_simulated_weather_data(city)
        
        try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "lat": city_info["lat"],
                "lon": city_info["lon"],
                "appid": settings.OPENWEATHER_API_KEY,
                "units": "metric",  # Celsius
                "lang": "es"  # Spanish
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        colombia_time = get_colombia_time()
                        time = colombia_time.strftime("%H:%M:%S")
                        
                        return WeatherData(
                            city=city,
                            name=city_info["name"],
                            temperature=round(data["main"]["temp"]),
                            humidity=data["main"]["humidity"],
                            description=data["weather"][0]["description"].title(),
                            time=time,
                            emoji=city_info["emoji"],
                            source="OpenWeatherMap API",
                            real_data=True,
                            altitude=city_info["altitude"]
                        )
                    else:
                        logger.error(f"OpenWeatherMap API error for {city}: {response.status}")
                        return await WeatherService.get_simulated_weather_data(city)
                        
        except Exception as e:
            logger.error(f"Error fetching real weather data for {city}: {e}")
            return await WeatherService.get_simulated_weather_data(city)

    @staticmethod
    async def get_simulated_weather_data(city: str) -> WeatherData:
        """Get simulated weather data for each city (fallback)"""
        city_info = settings.CITIES[city]
        
        if city == "bogota":
            temp = random.randint(14, 22)
            humidity = random.randint(60, 85)
        else:  # medellin
            temp = random.randint(20, 30)
            humidity = random.randint(55, 75)
        
        colombia_time = get_colombia_time()
        time = colombia_time.strftime("%H:%M:%S")
        
        return WeatherData(
            city=city,
            name=city_info["name"],
            temperature=temp,
            humidity=humidity,
            description="Parcialmente nublado",
            time=time,
            emoji=city_info["emoji"],
            source="Datos simulados",
            real_data=False,
            altitude=city_info["altitude"]
        )

    @staticmethod
    async def get_weather_data(city: str) -> WeatherData:
        """Get weather data - tries real API first, falls back to simulated"""
        return await WeatherService.get_real_weather_data(city)
