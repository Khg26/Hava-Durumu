# Getting Your OpenWeatherMap API Key

This guide will walk you through the step-by-step process of obtaining a free API key from OpenWeatherMap for use with the Weather App.

## Step 1: Create an OpenWeatherMap Account

1. Go to the [OpenWeatherMap Sign Up page](https://home.openweathermap.org/users/sign_up)
2. Fill in your details:
   - Email address
   - Username
   - Password
3. Click "Create Account"
4. Check your email and confirm your account if required

## Step 2: Navigate to the API Keys Section

1. Log in to your OpenWeatherMap account
2. Click on your username in the top-right corner
3. Select "My API Keys" from the dropdown menu

## Step 3: Get Your API Key

1. You should see a default API key already generated for you in the "API key" section
2. If you don't see a key, you can create one by entering a name in the "Create key" field and clicking "Generate"
3. Copy the generated API key

## Step 4: Add the API Key to Your Weather App

1. In the root directory of your Weather App project, create a file named `.env` (or rename `.env.example` to `.env`)
2. Add your API key to the file:
   ```
   OPENWEATHERMAP_API_KEY=your_api_key_here
   ```
3. Replace `your_api_key_here` with the API key you copied from OpenWeatherMap

## Step 5: Verify the API Key

1. Start your Weather App application
2. Search for a city (e.g., "London")
3. If you see weather data appear, your API key is working correctly

## Important Notes

- The free tier of OpenWeatherMap allows up to 1,000 API calls per day (or about 60 calls per hour)
- New API keys may take a few hours to activate (up to 2 hours in some cases)
- Never share your API key publicly or commit it to version control
- If you need more API calls, OpenWeatherMap offers various paid subscription tiers

## Troubleshooting

### "API key not configured" error

Check that:

- The `.env` file exists in the root directory
- The environment variable is named correctly (`OPENWEATHER_API_KEY`)
- There are no typos in your API key

### "API key not activated" error

- New API keys might take up to 2 hours to activate
- Verify your key in the OpenWeatherMap dashboard
- Try again after a few hours

### Rate limiting issues

If you exceed the API call limits:

- Reduce the frequency of your requests
- Implement better caching
- Consider upgrading to a paid plan if needed

---

With your API key set up, you're ready to use the Weather App and start exploring its features!
