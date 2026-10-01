# WebSocket Weather App

Weather dashboard prototype for Bogotá and Medellín. A FastAPI backend gathers OpenWeatherMap data when configured and falls back to explicitly labeled simulated readings. Background tasks broadcast updates to WebSocket observers. The React/TypeScript frontend includes weather, chat and sign-in interface components.

## What the repository contains

- `backend/main.py` starts the FastAPI app and its background weather tasks.
- `backend/app/services/weather_service.py` selects API readings or simulated fallback data.
- `frontend/` contains the React interface.
- [`README-OAUTH.md`](README-OAUTH.md), [`README-WEATHER-API.md`](README-WEATHER-API.md) and [`SYSTEM_OVERVIEW.md`](SYSTEM_OVERVIEW.md) contain additional implementation notes.

A previous README listed a Vercel demo and Render deployment. Their current availability could not be confirmed, so this README does not present them as live. The repository does not contain a LICENSE file; no license is asserted here.

## Run locally

In `backend/`, create a Python virtual environment, run `pip install -r requirements.txt`, then `python main.py`. In another terminal, run `npm install` and `npm start` in `frontend/`. The backend defaults to port 8000 and the frontend to port 3000. Set `OPENWEATHER_API_KEY` for live weather data; without it, readings may be simulated. These instructions reflect the code and have not been revalidated in this audit.
