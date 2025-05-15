from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
import os
import json
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create app directory if it doesn't exist
app_dir = Path("app/data")
app_dir.mkdir(exist_ok=True, parents=True)

# Database setup
DB_PATH = "app/data/weather_cache.db"

def init_db():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables for weather and forecast cache
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_cache (
        city TEXT PRIMARY KEY,
        data TEXT,
        timestamp INTEGER
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS forecast_cache (
        city TEXT PRIMARY KEY,
        data TEXT,
        timestamp INTEGER
    )
    ''')
    
    conn.commit()
    conn.close()

def get_cached_data(table_name, city):
    """Get cached data if it exists and is less than 1 hour old"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Convert city name to lowercase for case-insensitive comparison
    city_lower = city.lower()
    
    cursor.execute(f"SELECT data, timestamp FROM {table_name} WHERE LOWER(city) = ?", (city_lower,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        data, timestamp = result
        current_time = int(time.time())
        
        # Check if the cache is valid (less than 1 hour old)
        if current_time - timestamp < 3600:  # 3600 seconds = 1 hour
            return json.loads(data)
    
    return None

def cache_data(table_name, city, data):
    """Store data in the cache"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Convert to JSON string for storage
    data_json = json.dumps(data)
    timestamp = int(time.time())
    
    # Insert or replace existing data
    cursor.execute(
        f"INSERT OR REPLACE INTO {table_name} (city, data, timestamp) VALUES (?, ?, ?)",
        (city, data_json, timestamp)
    )
    
    conn.commit()
    conn.close()

# Initialize the database
init_db()

app = FastAPI(title="Weather App")

# Mount static directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# OpenWeatherMap API Key
API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
# Current Weather API endpoint
@app.get("/api/weather")
async def get_weather(city: str):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")
    
    # Check if we have cached data
    cached_data = get_cached_data("weather_cache", city)
    if cached_data:
        print(f"Using cached weather data for {city}")
        return cached_data
    
    # If not in cache or expired, fetch from API
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Cache the response
            cache_data("weather_cache", city, data)
            return data
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"City '{city}' not found")
            else:
                raise HTTPException(status_code=500, detail=f"Weather API error: {str(e)}")

# 5-day forecast API endpoint
@app.get("/api/forecast")
async def get_forecast(city: str):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")
    
    # Check if we have cached data
    cached_data = get_cached_data("forecast_cache", city)
    if cached_data:
        print(f"Using cached forecast data for {city}")
        return cached_data
    
    # If not in cache or expired, fetch from API
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Cache the response
            cache_data("forecast_cache", city, data)
            return data
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"City '{city}' not found")
            else:
                raise HTTPException(status_code=500, detail=f"Weather API error: {str(e)}")

# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Health check & cache info endpoint
@app.get("/api/status")
async def get_status():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get weather cache stats
        cursor.execute("SELECT COUNT(*), MAX(timestamp) FROM weather_cache")
        weather_count, latest_weather = cursor.fetchone()
        
        # Get forecast cache stats
        cursor.execute("SELECT COUNT(*), MAX(timestamp) FROM forecast_cache")
        forecast_count, latest_forecast = cursor.fetchone()
        
        conn.close()
        
        # Format timestamps
        latest_weather_time = datetime.fromtimestamp(latest_weather).isoformat() if latest_weather else None
        latest_forecast_time = datetime.fromtimestamp(latest_forecast).isoformat() if latest_forecast else None
        
        return {
            "status": "ok",
            "cache": {
                "weather": {
                    "count": weather_count,
                    "latest": latest_weather_time
                },
                "forecast": {
                    "count": forecast_count,
                    "latest": latest_forecast_time
                }
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
