# WeatherAPI

WeatherAPI is a FastAPI application that fetches current weather data for a specified city using the OpenWeatherMap API. It supports caching data locally (in JSON files) or on AWS S3 and logging requests to a local SQLite database or AWS DynamoDB, depending on configuration. The application is containerized with Docker for easy setup and deployment.

## Overview

- **Functionality**: Retrieves weather data (temperature, weather description, timestamp) via the `/weather` endpoint.
- **Caching**: Stores data in local JSON files (`weather_data/`) if `USE_LOCAL_STORAGE=1`, or in AWS S3 if `USE_LOCAL_STORAGE=0`.
- **Logging**: Logs requests to a local SQLite database (`weather_logs.db`) if `USE_LOCAL_STORAGE=1`, or to AWS DynamoDB if `USE_LOCAL_STORAGE=0`.
- **Tech Stack**: Python 3.11, FastAPI, Uvicorn, OpenWeatherMap API, AWS S3/DynamoDB, SQLite, Docker.
- **Features**: Asynchronous request handling, Docker support for consistent deployment.

## Prerequisites

- **Python 3.11** (for local execution without Docker).
- **Docker** and **Docker Compose** (for containerized execution).
- **OpenWeatherMap API Key**: Sign up at [OpenWeatherMap](https://openweathermap.org/) to obtain an API key.
- **AWS Credentials** (required if `USE_LOCAL_STORAGE=0`):
  - AWS Access Key ID and Secret Access Key.
  - AWS Region (e.g., `us-east-1`).
  - An existing DynamoDB table named `weather-logs` and an S3 bucket (e.g., `weather-data`).

## Running the Application Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/0101dusica/WeatherAPI.git
   cd WeatherAPI
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   venv/Scripts/activate # Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   - Create a `.env` file in the project root with the following content:
     ```plaintext
     OPENWEATHERMAP_API_KEY=your-api-key-here
     S3_BUCKET=weather-data
     DYNAMODB_TABLE=weather-logs
     AWS_ACCESS_KEY_ID=your-access-key-id
     AWS_SECRET_ACCESS_KEY=your-secret-access-key
     AWS_REGION=us-east-1
     USE_LOCAL_STORAGE=1  # Set to 0 for AWS S3/DynamoDB
     ```

5. **Run the Application**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   - The app will be available at `http://localhost:8000`.

6. **Test the API**:
   ```bash
   curl http://localhost:8000/weather?city=Belgrade
   ```
   - Expected response: A JSON object with weather data (e.g., `{"city": "Belgrade", "temperature": 25.81, ...}`).

## Running the Application with Docker

1. **Ensure Docker is Installed**:
   - Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and ensure it’s running.

2. **Configure Environment Variables**:
   - Ensure the `.env` file exists in the project root (see step 4 in the local setup above).

3. **Build and Run the Container**:
   ```bash
   docker-compose up --build
   ```
   - This builds the Docker image and starts the container.
   - The app will be available at `http://localhost:8000`.

4. **Test the API**:
   ```bash
   curl http://localhost:8000/weather?city=Belgrade
   ```

5. **Stop the Container**:
   ```bash
   docker-compose down
   ```

## Directory Structure

- `app/`: Contains the FastAPI application code.
  - `main.py`: Defines the API endpoints.
  - `models/weather.py`: defines Pydantic models for validating API request and response data.
  - `services/`: Handles caching, logging, and weather data retrieval.
  - `utils/config.py`: Loads environment variables.
- `weather_data/`: Stores cached JSON files (when `USE_LOCAL_STORAGE=1`).
- `weather_logs.db`: SQLite database for request logs (when `USE_LOCAL_STORAGE=1`).
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Defines the Docker image.
- `docker-compose.yml`: Configures the Docker container.

## Notes

- **Local Storage**: Set `USE_LOCAL_STORAGE=1` to use local JSON files and SQLite. The `weather_data/` folder and `weather_logs.db` file are persisted via Docker volumes.
- **AWS Services**: Set `USE_LOCAL_STORAGE=0` to use AWS S3 for caching and DynamoDB for logging. Ensure AWS credentials and resources are configured.
- **Troubleshooting**: Check container logs with `docker-compose logs` if the app fails to start.