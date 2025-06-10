import aiobotocore.session
import sqlite3
from app.utils.config import settings

# Logs the weather request either in a local SQLite database or DynamoDB.
# The storage method depends on the USE_LOCAL_STORAGE environment variable.
async def log_weather_request(city: str, timestamp: str, s3_path: str):
    use_local = settings.USE_LOCAL_STORAGE == "1"
    if use_local:
        # Connect to SQLite database and ensure the logs table exists
        conn = sqlite3.connect("weather_logs.db")
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS logs (city TEXT, timestamp TEXT, s3_path TEXT)"
        )
        
        cursor.execute(
            "INSERT INTO logs (city, timestamp, s3_path) VALUES (?, ?, ?)",
            (city, timestamp, s3_path)
        )
        conn.commit()
        conn.close()
        return
    
    # Log data in DynamoDB if not using local storage
    try:
        session = aiobotocore.session.get_session()
        async with session.create_client("dynamodb", region_name = settings.AWS_REGION) as dynamodb_client:
            item = {
                "city": {"S": city},     
                "timestamp": {"S": timestamp}, 
                "s3_path": {"S": s3_path}
            }
            await dynamodb_client.put_item(TableName=settings.DYNAMODB_TABLE, Item=item)
    except Exception as e:
        print(f"Error writing to DynamoDB: {str(e)}")