# Developer Guide: Extending the Weather App

This guide is designed for junior developers who want to understand and extend the Weather App project. Here, you'll find detailed explanations of the codebase and step-by-step instructions for adding new features.

## Table of Contents

- [Understanding the Codebase](#understanding-the-codebase)
- [Backend Architecture](#backend-architecture)
- [Frontend Architecture](#frontend-architecture)
- [The Caching System](#the-caching-system)
- [Tutorial: Adding New Features](#tutorial-adding-new-features)
- [Common Challenges](#common-challenges)
- [Best Practices](#best-practices)

## Understanding the Codebase

The Weather App is structured as a modern web application with a clear separation of concerns:

1. **Backend (FastAPI)** - Handles API requests, data fetching, and caching
2. **Frontend (HTML/CSS/JS)** - Provides the user interface and interacts with the backend
3. **Data Storage (SQLite)** - Caches weather data to reduce API calls

## Backend Architecture

The backend is built using FastAPI, a modern Python web framework that makes it easy to build APIs. Here's how it's organized:

### `main.py`

This is the entry point of the application. It:

- Sets up the FastAPI application
- Configures routes for API endpoints
- Handles API requests
- Manages data caching

Key components:

1. **API Routes**:

   - `/api/weather` - Gets current weather for a city
   - `/api/forecast` - Gets 5-day forecast for a city
   - `/api/status` - Gets cache statistics

2. **Caching Functions**:

   - `init_db()` - Creates the database tables
   - `get_cached_data()` - Retrieves cached data if available
   - `cache_data()` - Stores new data in the cache

3. **API Handler Functions**:
   - `get_weather()` - Handles current weather requests
   - `get_forecast()` - Handles forecast requests

### How the Backend Works

1. When a request comes in (e.g., `/api/weather?city=London`):
   - The application first checks if it has a valid cache for "London"
   - If valid cached data exists, it returns it immediately
   - If no cache exists or it's expired, it makes an API call to OpenWeatherMap
   - It then caches the result for future requests

## Frontend Architecture

The frontend is built with vanilla JavaScript and Bootstrap for styling:

### `index.html`

The main HTML template defining the page structure, including:

- Search form
- Weather display area
- Forecast display area
- Loading indicators
- Error messages

### `script.js`

Handles all frontend interactions:

1. User input handling
2. API requests to the backend
3. Rendering weather and forecast data
4. Managing loading states and errors
5. Saving user preferences (last searched city)

### `styles.css`

Custom styling to enhance the Bootstrap framework, including:

- Card styling
- Weather icon formatting
- Forecast display
- Responsive design adjustments

## The Caching System

The caching system uses SQLite to store weather data and reduce API calls:

1. **Database Schema**:

   - `weather_cache` table: Stores current weather data
   - `forecast_cache` table: Stores forecast data

2. **Cache Logic**:

   - Each record has a city name, data (JSON), and timestamp
   - Cache is valid for 1 hour (3600 seconds)
   - The system compares the current time to the timestamp to determine validity

3. **Cache Management**:
   - `cache_manager.py` provides utilities for viewing and clearing the cache

## Tutorial: Adding New Features

### Feature 1: Adding Air Quality Data

Let's add air quality information to our weather display:

1. **Update the Backend**:

```python
# Add to main.py
@app.get("/api/air-quality")
async def get_air_quality(city: str):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")

    # Check cache first
    cached_data = get_cached_data("air_quality_cache", city)
    if cached_data:
        print(f"Using cached air quality data for {city}")
        return cached_data

    # Get coordinates first (required for air quality API)
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

    async with httpx.AsyncClient() as client:
        try:
            # First get the coordinates
            weather_response = await client.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']

            # Then get air quality
            air_quality_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
            air_response = await client.get(air_quality_url)
            air_response.raise_for_status()

            data = air_response.json()

            # Cache the response
            cache_data("air_quality_cache", city, data)
            return data
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"City '{city}' not found")
            else:
                raise HTTPException(status_code=500, detail=f"Air quality API error: {str(e)}")
```

2. **Update the Database Initialization**:

```python
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

    # Add air quality table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS air_quality_cache (
        city TEXT PRIMARY KEY,
        data TEXT,
        timestamp INTEGER
    )
    ''')

    conn.commit()
    conn.close()
```

3. **Update the Frontend to Fetch and Display Air Quality**:

Add to script.js:

```javascript
// Function to fetch air quality data
async function getAirQuality(city) {
  try {
    const response = await fetch(
      `/api/air-quality?city=${encodeURIComponent(city)}`
    );

    if (!response.ok) {
      throw new Error("City not found");
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching air quality data:", error);
    throw error;
  }
}

// Update the search button handler
searchBtn.addEventListener("click", async function () {
  const city = cityInput.value.trim();

  if (!city) {
    return;
  }

  // Show loading indicator, hide weather info and error message
  loadingIndicator.classList.remove("d-none");
  weatherInfo.classList.add("d-none");
  errorMessage.classList.add("d-none");

  try {
    // Fetch weather, forecast, and air quality data in parallel
    const [weatherData, forecastData, airQualityData] = await Promise.all([
      getWeather(city),
      getForecast(city),
      getAirQuality(city),
    ]);

    // Update UI with all data
    updateWeatherUI(weatherData);
    updateForecastUI(forecastData);
    updateAirQualityUI(airQualityData);
  } catch (error) {
    weatherInfo.classList.add("d-none");
    errorMessage.classList.remove("d-none");
  } finally {
    // Hide loading indicator
    loadingIndicator.classList.add("d-none");
  }
});

// Function to update the UI with air quality data
function updateAirQualityUI(data) {
  // Create air quality display element if it doesn't exist
  let airQualitySection = document.getElementById("air-quality-section");
  if (!airQualitySection) {
    airQualitySection = document.createElement("div");
    airQualitySection.id = "air-quality-section";
    airQualitySection.className = "mt-4 pt-3 border-top";

    const heading = document.createElement("h4");
    heading.className = "text-center mb-3";
    heading.textContent = "Air Quality";

    const container = document.createElement("div");
    container.id = "air-quality-container";
    container.className = "text-center";

    airQualitySection.appendChild(heading);
    airQualitySection.appendChild(container);

    // Add it after the current weather info
    document.getElementById("weather-info").appendChild(airQualitySection);
  }

  const container = document.getElementById("air-quality-container");

  // Get air quality index
  const aqi = data.list[0].main.aqi;

  // Define AQI levels
  const aqiLevels = [
    { level: "Good", color: "success" },
    { level: "Fair", color: "info" },
    { level: "Moderate", color: "warning" },
    { level: "Poor", color: "warning" },
    { level: "Very Poor", color: "danger" },
  ];

  // Update container content
  container.innerHTML = `
    <div class="card bg-light">
      <div class="card-body">
        <h5 class="card-title">Air Quality Index</h5>
        <span class="badge bg-${aqiLevels[aqi - 1].color} p-2 mb-3 fs-6">
          ${aqiLevels[aqi - 1].level}
        </span>
        <div class="row">
          <div class="col-6">
            <p>CO: ${data.list[0].components.co} μg/m³</p>
            <p>NO₂: ${data.list[0].components.no2} μg/m³</p>
          </div>
          <div class="col-6">
            <p>PM2.5: ${data.list[0].components.pm2_5} μg/m³</p>
            <p>PM10: ${data.list[0].components.pm10} μg/m³</p>
          </div>
        </div>
      </div>
    </div>
  `;
}
```

4. **Add HTML and CSS for the Air Quality Display**:

Add to index.html (inside the weather-info div, after the forecast section):

```html
<!-- Air Quality Section will be added dynamically by JavaScript -->
```

Add to styles.css:

```css
/* Air Quality styles */
#air-quality-section .card {
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.badge {
  font-size: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
}
```

### Feature 2: Adding Weather Alerts

If the OpenWeatherMap API returns weather alerts for a location, let's display them:

1. **Add Alert UI to the Frontend**:

Add to script.js:

```javascript
// Function to update alerts UI
function updateAlertsUI(weatherData) {
  // Check if alerts exist
  if (!weatherData.alerts || weatherData.alerts.length === 0) {
    return;
  }

  // Create alerts section if it doesn't exist
  let alertsSection = document.getElementById("alerts-section");
  if (!alertsSection) {
    alertsSection = document.createElement("div");
    alertsSection.id = "alerts-section";
    alertsSection.className = "mt-4";

    // Add it at the top of weather info
    const weatherInfo = document.getElementById("weather-info");
    weatherInfo.prepend(alertsSection);
  }

  // Clear previous alerts
  alertsSection.innerHTML = "";

  // Add each alert
  weatherData.alerts.forEach((alert) => {
    const alertCard = document.createElement("div");
    alertCard.className = "alert alert-danger mb-3";

    // Format the alert dates
    const start = new Date(alert.start * 1000).toLocaleString();
    const end = new Date(alert.end * 1000).toLocaleString();

    alertCard.innerHTML = `
      <h5 class="alert-heading">${alert.event}</h5>
      <p>${alert.description}</p>
      <hr>
      <p class="mb-0">From: ${start}</p>
      <p class="mb-0">Until: ${end}</p>
    `;

    alertsSection.appendChild(alertCard);
  });
}
```

## Common Challenges

### 1. Rate Limiting

OpenWeatherMap has API call limits. If you're getting errors, check:

- Your API call frequency
- Your subscription tier limits

Solution: Implement better caching or throttling.

### 2. Error Handling

When API calls fail, ensure you're handling errors gracefully:

- Display user-friendly messages
- Log detailed errors for debugging
- Add retry mechanisms for transient failures

### 3. Performance Optimization

As the app grows, watch for performance issues:

- Minimize unnecessary API calls
- Optimize database queries
- Consider client-side caching strategies

## Best Practices

1. **Code Organization**:

   - Keep related functionality grouped
   - Use meaningful function and variable names
   - Add comments for complex logic

2. **Error Handling**:

   - Always handle both frontend and backend errors
   - Provide meaningful error messages to users
   - Log detailed errors for debugging

3. **API Usage**:

   - Respect rate limits
   - Cache responses to reduce API calls
   - Handle API changes gracefully

4. **Testing**:

   - Write tests for your backend functions
   - Test with different cities and scenarios
   - Verify cache functionality

5. **Security**:
   - Never expose API keys in frontend code
   - Validate user inputs
   - Consider implementing CORS protections

---

Happy coding! This guide should help you understand and extend the Weather App project. If you have questions or need further guidance, please reach out to the project maintainers.
