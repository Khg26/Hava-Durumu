document.addEventListener("DOMContentLoaded", function () {
  const cityInput = document.getElementById("city-input");
  const searchBtn = document.getElementById("search-btn");
  const weatherInfo = document.getElementById("weather-info");
  const errorMessage = document.getElementById("error-message");
  const loadingIndicator = document.getElementById("loading-indicator");
  const cityName = document.getElementById("city-name");
  const weatherIcon = document.getElementById("weather-icon");
  const temperature = document.getElementById("temperature");
  const weatherDescription = document.getElementById("weather-description");
  const humidity = document.getElementById("humidity");
  const windSpeed = document.getElementById("wind-speed");
  const feelsLike = document.getElementById("feels-like");
  const pressure = document.getElementById("pressure");
  const forecastContainer = document.getElementById("forecast-container");

  // Function to fetch current weather data
  async function getWeather(city) {
    try {
      const response = await fetch(
        `/api/weather?city=${encodeURIComponent(city)}`
      );

      if (!response.ok) {
        throw new Error("City not found");
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching weather data:", error);
      throw error;
    }
  }

  // Function to fetch forecast data
  async function getForecast(city) {
    try {
      const response = await fetch(
        `/api/forecast?city=${encodeURIComponent(city)}`
      );

      if (!response.ok) {
        throw new Error("City not found");
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching forecast data:", error);
      throw error;
    }
  }

  // Function to update the UI with current weather data
  function updateWeatherUI(data) {
    cityName.textContent = `${data.name}, ${data.sys.country}`;
    weatherIcon.src = `https://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png`;
    temperature.textContent = `${Math.round(data.main.temp)}°C`;
    weatherDescription.textContent = data.weather[0].description;
    humidity.textContent = data.main.humidity;
    windSpeed.textContent = (data.wind.speed * 3.6).toFixed(1); // Convert m/s to km/h
    feelsLike.textContent = Math.round(data.main.feels_like);
    pressure.textContent = data.main.pressure;

    // Store the last searched city in localStorage for convenience
    localStorage.setItem("lastSearchedCity", data.name);

    weatherInfo.classList.remove("d-none");
    errorMessage.classList.add("d-none");
  }

  // Function to update the UI with forecast data
  function updateForecastUI(data) {
    // Clear previous forecast data
    forecastContainer.innerHTML = "";

    // Group forecast data by day (we want to show 5 days)
    const dailyData = {};

    // OpenWeatherMap forecast returns data every 3 hours, so we need to group by day
    data.list.forEach((item) => {
      // Get the date part only
      const date = item.dt_txt.split(" ")[0];

      // If we haven't stored this day yet, add it
      if (!dailyData[date]) {
        dailyData[date] = item;
      }
    });

    // Create a forecast card for each day (max 5 days)
    let count = 0;
    for (const date in dailyData) {
      if (count >= 5) break;

      const item = dailyData[date];
      const dateObj = new Date(date);
      const dayName = new Intl.DateTimeFormat("en-US", {
        weekday: "short",
      }).format(dateObj);
      const monthDay = dateObj.getDate();

      // Create forecast card element
      const forecastCard = document.createElement("div");
      forecastCard.className = "col forecast-card";
      forecastCard.innerHTML = `
        <div class="forecast-day">${dayName} ${monthDay}</div>
        <img class="forecast-icon" src="https://openweathermap.org/img/wn/${
          item.weather[0].icon
        }.png" alt="${item.weather[0].description}">
        <div class="forecast-temp">${Math.round(item.main.temp)}°C</div>
        <div class="forecast-min-max">${Math.round(
          item.main.temp_min
        )}° / ${Math.round(item.main.temp_max)}°</div>
        <div class="forecast-description">${item.weather[0].description}</div>
      `;

      forecastContainer.appendChild(forecastCard);
      count++;
    }
  }

  // Handle search button click
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
      // Fetch both current weather and forecast data in parallel
      const [weatherData, forecastData] = await Promise.all([
        getWeather(city),
        getForecast(city),
      ]);

      // Update UI with both data
      updateWeatherUI(weatherData);
      updateForecastUI(forecastData);
    } catch (error) {
      weatherInfo.classList.add("d-none");
      errorMessage.classList.remove("d-none");
    } finally {
      // Hide loading indicator
      loadingIndicator.classList.add("d-none");
    }
  });

  // Handle Enter key press
  cityInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      searchBtn.click();
    }
  });

  // Load the last searched city if available
  const lastSearchedCity = localStorage.getItem("lastSearchedCity");
  if (lastSearchedCity) {
    cityInput.value = lastSearchedCity;
    // Automatically search after a short delay to allow the page to fully load
    setTimeout(() => {
      searchBtn.click();
    }, 500);
  }
});
