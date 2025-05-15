# Getting Started with the Weather App

Welcome to the Weather App project! This guide will help you get the application up and running on your local machine in just a few minutes.

## Quick Start Guide

### Step 1: Prerequisites

Before you begin, make sure you have the following installed:

- Python 3.8 or newer
- pip (Python package installer)
- Git (optional, for cloning the repository)

### Step 2: Download the Project

Clone the repository or download the source code:

```bash
git clone https://github.com/yourusername/weather-app.git
cd weather-app
```

### Step 3: Set Up a Virtual Environment (Recommended)

Creating a virtual environment keeps your project dependencies isolated:

```bash
# On macOS/Linux
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 4: Install Dependencies

Install all the required packages:

```bash
pip install -r requirements.txt
```

### Step 5: Get an API Key

1. Follow the instructions in `API_KEY_GUIDE.md` to obtain your free OpenWeatherMap API key
2. Create a `.env` file in the project root directory
3. Add your API key to the `.env` file:
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```

### Step 6: Run the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

### Step 7: Access the Application

Open your web browser and navigate to:

```
http://localhost:8000
```

You should now see the Weather App interface!

## Next Steps

Once you have the application running:

1. Search for a city to see the current weather and forecast
2. Explore the codebase to understand how it works
3. Check out `DEVELOPER_GUIDE.md` for information on extending the app
4. Try adding new features or improving existing ones

## Troubleshooting

### Problem: "Module not found" errors

Solution: Make sure you've installed all dependencies with `pip install -r requirements.txt`

### Problem: No weather data appears

Solution: Verify your API key is correctly set in the `.env` file and that it's active (see API_KEY_GUIDE.md)

### Problem: Application doesn't start

Solution: Check that port 8000 is not already in use by another application

### Problem: "No module named 'uvicorn'"

Solution: Make sure you've activated your virtual environment and installed all dependencies

---

Happy weather forecasting!
