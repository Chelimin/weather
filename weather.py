#!/usr/bin/env python3

import json
import sys
from urllib import error, request
from urllib.parse import quote


def fetch_json(url):
    req = request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def get_city_coordinates(city_name):
    encoded_name = quote(city_name)
    url = (
        "https://geocoding-api.open-meteo.com/v1/search?"
        f"name={encoded_name}&count=1&language=en&format=json"
    )
    data = fetch_json(url)

    if "results" not in data or not data["results"]:
        raise ValueError(f"No matching city found for: {city_name}")

    result = data["results"][0]
    return (
        float(result["latitude"]),
        float(result["longitude"]),
        result.get("name", city_name),
        result.get("country", ""),
    )


def get_current_weather(latitude, longitude):
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        "&current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m"
        "&timezone=auto"
    )
    data = fetch_json(url)
    current = data.get("current", {})

    if not current:
        raise ValueError("Weather data was not returned for that location.")

    return current


def weather_description(code):
    conditions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Moderate freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Rain showers",
        81: "Moderate showers",
        82: "Violent showers",
        85: "Snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Severe thunderstorm",
    }
    return conditions.get(code, "Unknown conditions")


def main():
    city_name = input("Enter a city name: ").strip()
    if not city_name:
        print("City name cannot be empty.")
        return 1

    try:
        latitude, longitude, city, country = get_city_coordinates(city_name)
        weather = get_current_weather(latitude, longitude)

        temp = weather.get("temperature_2m")
        humidity = weather.get("relative_humidity_2m")
        precipitation = weather.get("precipitation")
        wind = weather.get("wind_speed_10m")
        code = weather.get("weather_code")

        print(f"\nWeather for {city}, {country}")
        print(f"Condition: {weather_description(code)}")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")
        print(f"Precipitation: {precipitation} mm")
        print(f"Wind speed: {wind} km/h")
        return 0

    except (ValueError, KeyError, TypeError, json.JSONDecodeError, error.URLError) as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
