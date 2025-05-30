import requests
import os


def get_weather(city: str) -> str:
    try:
        api_key = os.getenv("WEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ua"
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
        return (
            f"В {city.capitalize()} зараз:\n"
            f"🌡️ Температура: {temp}°C\n"
            f"☁️ Опис: {description}\n"
            f"💨 Вітер: {wind} м/с\n"
            f"💧 Вологість: {humidity}%"
        )
    except (KeyError, ValueError):
        return "Invalid response format from the weather service."
