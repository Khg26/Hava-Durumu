# Weather App

A simple weather application built with FastAPI and JavaScript that displays current weather information and forecasts for any city. This project is perfect for junior developers looking to understand full-stack development concepts including REST APIs, frontend/backend integration, asynchronous programming, and data caching.

![Weather App Screenshot](https://via.placeholder.com/800x450.png?text=Weather+App+Screenshot)

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Running the Application](#running-the-application)
  - [Local Development](#local-development)
  - [Using Docker](#using-docker)
- [API Documentation](#api-documentation)
- [Caching System](#caching-system)
- [Frontend Architecture](#frontend-architecture)
- [Cache Management](#cache-management)
- [Learning Opportunities](#learning-opportunities)
- [Common Issues and Troubleshooting](#common-issues-and-troubleshooting)
- [Next Steps for Improvement](#next-steps-for-improvement)
- [Dependencies](#dependencies)

## Features

- **City-based Weather Search**: Search for weather by city name
- **Current Weather Display**: View temperature, weather description, humidity, wind speed, and more metrics
- **5-Day Weather Forecast**: See upcoming weather forecasts for the next 5 days
- **Persistent Preferences**: Your last searched city is remembered between sessions
- **User-friendly Interface**: Loading indicators provide feedback during API calls
- **Responsive Design**: Works on both desktop and mobile devices
- **Error Handling**: Clear feedback when a city cannot be found
- **Data Caching**: SQLite database stores weather data to reduce API calls (1 hour cache duration)
- **API Monitoring**: Status endpoint to view cache statistics

## Project Structure

```
weather-app/
├── app/                          # Application directory
│   ├── data/                     # SQLite database storage
│   │   └── weather_cache.db      # Cache database
│   ├── static/                   # Static assets
│   │   ├── css/                  # CSS styles
│   │   │   └── styles.css        # Main stylesheet
│   │   └── js/                   # JavaScript files
│   │       └── script.js         # Frontend logic
│   └── templates/                # HTML templates
│       └── index.html            # Main page template
├── .env                          # Environment variables (API keys)
├── .gitignore                    # Git ignore file
├── cache_manager.py              # Utility for managing the cache
├── docker-compose.yml            # Docker Compose configuration
├── Dockerfile                    # Docker build instructions
├── main.py                       # FastAPI application entry point
├── README.md                     # Project documentation
└── requirements.txt              # Python dependencies
```

## Technology Stack

- **Backend**:
  - FastAPI (Python web framework)
  - Uvicorn (ASGI server)
  - SQLite (Database for caching)
  - Python 3.8+ (Programming language)
- **Frontend**:
  - HTML5 / CSS3
  - JavaScript (ES6+)
  - Bootstrap 5 (UI framework)
- **DevOps**:
  - Docker (Containerization)
  - Docker Compose (Container orchestration)

## Getting Started

### Prerequisites

To run this application, you'll need:

- Python 3.8 or newer
- pip (Python package installer)
- An OpenWeatherMap API key (free tier available)
- Git (optional, for cloning the repository)
- Docker and Docker Compose (optional, for containerized deployment)

### Installation

1. Clone this repository or download the source code:

   ```bash
   git clone https://github.com/yourusername/weather-app.git
   cd weather-app
   ```

2. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Get an API key from [OpenWeatherMap](https://openweathermap.org/api):

   - Register for a free account
   - Navigate to "API keys" section
   - Generate or copy your API key

2. Create a `.env` file in the project root directory:
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```

## Running the Application

### Local Development

Start the FastAPI server with:

```bash
uvicorn main:app --reload
```

The `--reload` flag enables hot reloading, which automatically restarts the server when code changes are detected. This is useful during development.

Then open your browser and navigate to `http://localhost:8000`

### Using Docker

1. Make sure Docker and Docker Compose are installed on your system

2. Build and start the container:

   ```bash
   docker compose up -d
   ```

3. The application will be available at `http://localhost:8000`

4. To stop the containers:
   ```bash
   docker compose down
   ```

## API Documentation

FastAPI automatically generates interactive API documentation. You can access it at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### API Endpoints

- `GET /api/weather?city={city_name}`

  - **Description**: Get current weather data for a specific city
  - **Query Parameters**: `city` (required) - Name of the city
  - **Response**: JSON with current weather data
  - **Example**: `/api/weather?city=London`

- `GET /api/forecast?city={city_name}`

  - **Description**: Get 5-day weather forecast for a specific city
  - **Query Parameters**: `city` (required) - Name of the city
  - **Response**: JSON with forecast data
  - **Example**: `/api/forecast?city=New%20York`

- `GET /api/status`
  - **Description**: View cache status and statistics
  - **Response**: JSON with cache information
  - **Example**: `/api/status`

## Caching System

This application implements a SQLite-based caching system to minimize API calls to OpenWeatherMap:

- **Cache Duration**: Weather data is cached for 1 hour
- **Storage**: Cached data is stored in `app/data/weather_cache.db`
- **Tables**:
  - `weather_cache`: Stores current weather data
  - `forecast_cache`: Stores forecast data
- **How It Works**:
  1. When a request comes in, the app first checks if cached data exists for the requested city
  2. If valid cached data exists (less than 1 hour old), it is returned
  3. If no valid cache exists, the app makes a request to the OpenWeatherMap API
  4. The new data is stored in the cache for future use
- **Docker Integration**: When using Docker, the cache database is persisted using a named volume

## Frontend Architecture

The frontend is built using vanilla JavaScript with Bootstrap 5 for styling:

- **HTML Structure**: Single page application with responsive layout
- **CSS**: Custom styles extend Bootstrap for a clean and modern UI
- **JavaScript**:
  - Fetches data from the backend API
  - Handles user interactions
  - Updates the UI with weather data
  - Implements local storage for remembering the last searched city

### Key Frontend Features:

1. **City Search**:

   - Input field for city name
   - Search button triggers API request
   - Enter key support for form submission

2. **Weather Display**:

   - Current temperature with large icon
   - Weather description
   - Additional metrics (humidity, wind speed, etc.)

3. **Forecast Display**:

   - 5-day forecast section
   - Daily temperature and conditions
   - Visual icons representing weather conditions

4. **User Experience Enhancements**:
   - Loading indicators during API requests
   - Error messages for city not found
   - Automatic loading of last searched city

## Cache Management

The application includes a `cache_manager.py` utility script to help manage the cache database:

1. View cache statistics:

   ```bash
   python cache_manager.py view
   ```

2. Clear the cache:
   ```bash
   python cache_manager.py clear
   ```

## Learning Opportunities

This project offers several learning opportunities for junior developers:

1. **FastAPI Framework**: Learn how to build modern Python APIs with automatic documentation
2. **Asynchronous Programming**: Understand async/await patterns in Python
3. **Frontend/Backend Integration**: See how JavaScript frontend communicates with Python backend
4. **SQLite Database**: Learn basic database operations without complex setup
5. **API Integration**: Practice working with third-party APIs (OpenWeatherMap)
6. **Data Caching**: Understand caching concepts and implementation
7. **Docker Containerization**: Learn container-based deployment
8. **Environment Variables**: Understand secure configuration management
9. **Error Handling**: Both frontend and backend error handling patterns

## Common Issues and Troubleshooting

1. **"API key not configured" error**:

   - Ensure you've created a `.env` file with your OpenWeatherMap API key
   - Check that the key is correctly formatted

2. **"City not found" error**:

   - Verify the city name spelling
   - Try adding country code for specificity (e.g., "London,UK")

3. **Missing module errors when running the app**:

   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Verify you're using Python 3.8 or newer

4. **Cache not working**:

   - Ensure the `app/data` directory exists and is writable
   - Check permissions if using Docker

5. **Docker issues**:
   - Verify Docker and Docker Compose are installed
   - Check if port 8000 is already in use by another application

## Next Steps for Improvement

Consider these enhancements as learning exercises:

1. Add user accounts to save favorite cities
2. Implement unit and integration tests
3. Add more detailed weather information (UV index, air quality)
4. Create a dark mode theme option
5. Add multiple language support
6. Implement geolocation to automatically detect user's city
7. Add weather alerts and notifications
8. Create a mobile app version using a framework like React Native

## Dependencies

- **FastAPI** - Modern web framework for building APIs
- **Uvicorn** - ASGI server for running the application
- **Jinja2** - Templating engine for HTML generation
- **HTTPX** - Asynchronous HTTP client for API requests
- **SQLite3** - Lightweight database for caching
- **Python-dotenv** - Environment variable management
- **Bootstrap 5** - Frontend CSS framework

---

This project was created as a learning resource for junior developers. Feel free to modify and extend it as you learn and grow your skills!
