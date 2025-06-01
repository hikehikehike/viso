import requests
import os
from .cache import redis_client


def get_weather(city: str) -> str:
    cache_key = f"weather:{city.lower()}"
    cached = redis_client.get(cache_key)
    if cached:
        return f"(from cache)\n{cached}"

    api_key = os.getenv("WEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ua"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error while fetching weather: {str(e)}"

    try:
        data = response.json()
        description = data["weather"][0]["description"].capitalize()
        temp = round(data["main"]["temp"])
        wind = data["wind"]["speed"]
        humidity = data["main"]["humidity"]
        result = (
            f"В {city.capitalize()} зараз:\n"
            f"🌡️ Температура: {temp}°C\n"
            f"☁️ Опис: {description}\n"
            f"💨 Вітер: {wind} м/с\n"
            f"💧 Вологість: {humidity}%"
        )

        redis_client.setex(cache_key, 1800, result)

        return result
    except (KeyError, ValueError):
        return "Invalid response format from the weather service."
