import os
import httpx
from fastapi import FastAPI, HTTPException
from loggers.logger_req import logger

WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather?'
API_KEY =  os.environ.get('WEATHER_API_KEY')

if not API_KEY:
    raise ValueError('WEATHER_API_KEY environment variable not set')

async def get_weather_summary(city:str) -> str:
    logger.debug(f'Fetching weather summary for {city}')
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(WEATHER_URL,params={'q':city,'appid':API_KEY,'units':'metric'})
    except httpx.RequestError as exc:
        logger.error(f'Weather service unreachable {exc}')
        raise HTTPException(status_code=502, detail='Weather service unreachable') from exc

    if resp.status_code == 404:
        logger.warning(f'City not found: {city}')
        raise HTTPException(status_code=404, detail=f'City {city} not found')

    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        logger.error(f'Error fetching weather data {exc}')
        raise HTTPException(status_code=500, detail=f'Error fetching weather data {exc}')
    data = resp.json()
    temp = data['main']['temp']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    condition = data['weather'][0]['description']
    return f"Weather in {city}: {condition}, {temp}°C, {humidity}% humidity, {wind_speed} m/s wind"