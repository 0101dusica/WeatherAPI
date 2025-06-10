import os
import aiobotocore.session
import sqlite3
from app.utils.config import settings

# Logs the weather request either in a local SQLite database or DynamoDB.
# The storage method depends on the USE_LOCAL_STORAGE environment variable.
async def log_weather_request(city: str, timestamp: str, s3_path: str):
    if os.getenv("USE_LOCAL_STORAGE"):
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
    pass