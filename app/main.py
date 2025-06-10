from fastapi import FastAPI, HTTPException
from app.models.weather import WeatherResponse
from app.services.weather_api import get_weather_data
from app.services.storage import store_weather_data

app = FastAPI()

@app.get("/weather", response_model=WeatherResponse)
async def get_weather(city: str):
    try:
        # Check cached data (last 5 min)
        pass

        # Fetch new data if no valid cache
        weather_data = await get_weather_data(city)
        
        # Store data locally or in S3/DynamoDB based on config
        path = await store_weather_data(weather_data)
        
        return weather_data
    except ValueError as e:
        # City not found or API error
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Unexpected server error
        raise HTTPException(status_code=500, detail="Internal server error")