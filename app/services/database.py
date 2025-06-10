import os
import aiobotocore.session
import aiohttp
import aiosqlite
from app.utils.config import settings

# Logs the weather request either in a local SQLite database or DynamoDB.
# The storage method depends on the USE_LOCAL_STORAGE environment variable.
async def log_weather_request(city: str, timestamp: str, s3_path: str):
    use_local = settings.USE_LOCAL_STORAGE == "1"
    if use_local:
        try:
            os.makedirs("logs", exist_ok=True)
            async with aiosqlite.connect("logs/weather_logs.db") as conn:
                cursor = await conn.cursor()
                await cursor.execute(
                    "CREATE TABLE IF NOT EXISTS logs (city TEXT, timestamp TEXT, s3_path TEXT)"
                )
                await cursor.execute(
                    "INSERT INTO logs (city, timestamp, s3_path) VALUES (?, ?, ?)",
                    (city, timestamp, s3_path)
                )
                await conn.commit()
        except Exception as e:
            print(f"Error logging to SQLite for city {city}: {str(e)}")
        return
    
    # Log data in DynamoDB if not using local storage
    try:
        session = aiobotocore.session.get_session()
        async with session.create_client("dynamodb", region_name = settings.AWS_REGION, timeout=aiohttp.ClientTimeout(total=10)) as dynamodb_client:
            item = {
                "city": {"S": city},     
                "timestamp": {"S": timestamp}, 
                "s3_path": {"S": s3_path}
            }
            await dynamodb_client.put_item(TableName=settings.DYNAMODB_TABLE, Item=item)
    except aiobotocore.exceptions.ClientError as e:
        print(f"DynamoDB client error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error writing to DynamoDB: {str(e)}")