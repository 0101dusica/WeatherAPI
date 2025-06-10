from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
    USE_LOCAL_STORAGE= os.getenv("USE_LOCAL_STORAGE")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    S3_BUCKET = os.getenv("S3_BUCKET")
    DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE")

settings = Settings()