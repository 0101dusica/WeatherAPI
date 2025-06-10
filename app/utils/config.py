from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

settings = Settings()