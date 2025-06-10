import json
import os
import glob
from datetime import datetime, timedelta, timezone
import aiobotocore
from app.utils.config import settings

# Checks for cached weather data from local storage or S3.
# Returns cached data if a valid entry exists within the last 5 minutes.
async def check_cache(city: str) -> dict | None:
    five_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=5)
    
    use_local = settings.USE_LOCAL_STORAGE == "1"
    if use_local:
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
    session = aiobotocore.session.get_session()
    async with session.create_client("s3", region_name=settings.AWS_REGION) as s3_client:
        try:
            response = await s3_client.list_objects_v2(
                Bucket=settings.S3_BUCKET,
                Prefix=city
            )
            for obj in response.get("Contents", []):
                timestamp_str = obj["Key"].split("_")[1].replace(".json", "")

                try:
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H-%M-%S").replace(tzinfo=timezone.utc)
                    
                    # Return S3 cached file if it's recent - within the last 5 minutes
                    if timestamp > five_minutes_ago:
                        file_obj = await s3_client.get_object(
                            Bucket=settings.S3_BUCKET,
                            Key=obj["Key"]
                        )
                        data = json.loads(await file_obj["Body"].read())
                        return data
                except ValueError:
                    continue  # Skip files with invalid timestamps
        except Exception as e:
            print(f"Error checking S3 cache: {str(e)}")
            return None
    return None