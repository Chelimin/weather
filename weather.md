# Weather App

This app is a simple command-line tool that asks the user for a city name, fetches the current weather from a free public API, and prints a clean summary in the terminal.

## How it works

1. The script prompts the user to enter a city.
2. It searches for the city using the Open-Meteo geocoding API.
3. It fetches the current weather for the matching latitude and longitude.
4. It displays a concise summary including:
   - city and country
   - weather condition
   - temperature
   - humidity
   - precipitation
   - wind speed

## Run it

From the project folder, run:

```bash
python weather.py
```

Then enter a city name, for example:

```text
London
```

## Notes

- The app uses a free API and does not require an API key.
- It handles invalid city names and network issues gracefully.
