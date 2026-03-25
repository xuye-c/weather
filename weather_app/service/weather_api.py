# services/weatherApi.py

import requests
import os

API_KEY = "6254bdfa168f19b9a37838ab44be6134"

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