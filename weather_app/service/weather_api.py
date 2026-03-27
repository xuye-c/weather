# services/weatherApi.py

import requests
import os
from dotenv import load_dotenv
import os

load_dotenv("weather.env")  # 指定你的文件

API_KEY = os.getenv("OPENWEATHER_API_KEY")

class WeatherAPI:

    @staticmethod
    def get_current_weather(city):
        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        try:
            res = requests.get(url, params=params)
            data = res.json()

            if res.status_code != 200:
                return {
                    "status": "error",
                    "message": data.get("message", "API error")
                }

            return {
                "status": "success",
                "data": {
                    "city": data["name"],
                    "temp": data["main"]["temp"],
                    "weather": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"]
                }
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }