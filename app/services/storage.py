import json
import os
import aiobotocore.session
from app.utils.config import settings    

# Stores weather data locally or in S3, depending on configuration.
# Returns the file path or S3 URL after saving.
async def store_weather_data(weather_data: dict) -> str:
    city = weather_data["city"]
    timestamp = weather_data["timestamp"].replace(":", "-")
    filename = f"{city}_{timestamp}.json"

    # Check environment setting for local storage
    if settings.USE_LOCAL_STORAGE == "1":
        os.makedirs("weather_data", exist_ok=True)
        with open(f"weather_data/{filename}", "w") as f:
            json.dump(weather_data, f)
        return f"weather_data/{filename}"  # Returning local path
    
    # Upload data to S3 (session created only when needed)
    session = aiobotocore.session.get_session()
    async with session.create_client("s3", region_name=settings.AWS_REGION) as s3_client:
        await s3_client.put_object(
            Bucket=settings.S3_BUCKET,
            Key=filename,
            Body=json.dumps(weather_data)
        )
        return f"s3://{settings.S3_BUCKET}/{filename}"  # Returning S3 URL