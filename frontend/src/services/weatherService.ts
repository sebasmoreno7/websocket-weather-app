// src/services/weatherService.ts
import { CityType, WeatherData, CityCoordinates } from '../types';

const CITY_COORDINATES: Record<CityType, CityCoordinates> = {
  bogota: { lat: 4.61, lon: -74.08, timezone: 'America/Bogota' },
  medellin: { lat: 6.25, lon: -75.56, timezone: 'America/Bogota' }
};

const FALLBACK_TEMPS: Record<CityType, number> = {
  bogota: 15,
  medellin: 24
};

export class WeatherService {
  static async getCityWeatherData(city: CityType): Promise<WeatherData> {
    try {
      const coord = CITY_COORDINATES[city];
      const response = await fetch(
        `https://api.open-meteo.com/v1/forecast?latitude=${coord.lat}&longitude=${coord.lon}&current=temperature_2m&timezone=${coord.timezone}`
      );
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      const currentTime = new Date().toLocaleTimeString('es-CO', {
        timeZone: coord.timezone,
        hour: '2-digit',
        minute: '2-digit'
      });
      
      return {
        temp: Math.round(data.current.temperature_2m),
        time: currentTime
      };
    } catch (err) {
      console.error(`Error obteniendo datos de ${city}:`, err);
      
      const fallbackTime = new Date().toLocaleTimeString('es-CO', {
        hour: '2-digit', 
        minute: '2-digit'
      });
      
      return {
        temp: FALLBACK_TEMPS[city],
        time: fallbackTime
      };
    }
  }

  static getCurrentColombianTime(): string {
    return new Date().toLocaleTimeString('es-CO', {
      timeZone: 'America/Bogota',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  }
}
