import json
import os
import aiobotocore.session
from datetime import datetime
from app.utils.config import settings

# Stores weather data locally or in S3, depending on configuration.
# Returns the file path or S3 URL after saving.
async def store_weather_data(weather_data: dict) -> str:
    session = aiobotocore.session.get_session()
    async with session.create_client("s3") as s3_client:
        city = weather_data["city"]
        timestamp = weather_data["timestamp"].replace(":", "-")
        filename = f"{city}_{timestamp}.json"
        
        # Check environment setting for local storage
        if os.getenv("USE_LOCAL_STORAGE"):
            os.makedirs("weather_data", exist_ok=True)
            with open(f"weather_data/{filename}", "w") as f:
                json.dump(weather_data, f)
            return f"weather_data/{filename}" # Returning local path
        
        # Upload data to S3
        pass