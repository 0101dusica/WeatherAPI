import json
import os
import glob
from datetime import datetime, timedelta, timezone
from app.utils.config import settings

# Checks for cached weather data from local storage or S3.
# Returns cached data if a valid entry exists within the last 5 minutes.
async def check_cache(city: str) -> dict | None:
    five_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=5)
    
    if os.getenv("USE_LOCAL_STORAGE"):
        try:
            # Look for cached JSON files in local storage
            os.makedirs("weather_data", exist_ok=True)
            files = glob.glob(f"weather_data/{city}_*.json")
            
            for file_path in files:
                filename = os.path.basename(file_path)
                timestamp_str = filename.split("_")[1].replace(".json", "")                

                try:
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H-%M-%S").replace(tzinfo=timezone.utc)
                    
                    # Check if the cached file is recent - within the last 5 minutes
                    if timestamp > five_minutes_ago:
                        with open(file_path, "r") as f:
                            data = json.load(f)
                        return data
                except ValueError as e:
                    continue  # Skip files with invalid timestamp format
        except Exception as e:
            print(f"Error checking local cache: {str(e)}")
            return None
        return None

    # Check S3 cache if local storage is disabled
    pass