from fastapi import FastAPI, HTTPException
from app.models.weather import WeatherResponse
from app.services.weather_api import get_weather_data
from app.services.storage import store_weather_data
from app.services.database import log_weather_request
from app.services.cache import check_cache

app = FastAPI()

@app.get("/weather", response_model=WeatherResponse)
async def get_weather(city: str):
    try:
        # Check cached data - within the last 5 min
        cached_weather_data = await check_cache(city)
        if cached_weather_data:
            return cached_weather_data

        # Fetch new data if no valid cache
        weather_data = await get_weather_data(city)
        
        # Store data locally or in S3/DynamoDB based on config
        path = await store_weather_data(weather_data)
        await log_weather_request(city, weather_data["timestamp"], path)
        
        return weather_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")