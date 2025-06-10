import aiohttp
from app.utils.config import settings
from datetime import datetime, timezone

# Fetches current weather data for the given city using OpenWeather API.
# Returns structured data including name, temperature, description, and timestamp.
async def get_weather_data(city: str) -> dict:
    async with aiohttp.ClientSession() as session:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.OPENWEATHERMAP_API_KEY}&units=metric"
        
        async with session.get(url) as response:
            if response.status != 200:
                raise ValueError(f"API request failed: {response.status} {await response.text()}")
            
            data = await response.json()

            return {
                "city": city,
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
            }
