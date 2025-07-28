// src/types/index.ts
export type MessageType = 'robot' | 'system' | 'user' | 'notification';

export interface Message {
  sender: string;
  content: string;
  timestamp: Date;
  type: MessageType;
}

export interface WeatherData {
  temp: number;
  time: string;
}

export interface RobotConnections {
  observer: boolean;
  robotA: boolean;
  robotB: boolean;
}

export type CityType = 'bogota' | 'medellin';

export interface CityCoordinates {
  lat: number;
  lon: number;
  timezone: string;
}
