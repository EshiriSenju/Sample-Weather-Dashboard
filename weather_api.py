import requests
from datetime import datetime


class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_weather(self, city, units):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units={units}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def fetch_forecast(self, city, units):
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.api_key}&units={units}"
        forecast_response = requests.get(forecast_url)
        forecast_response.raise_for_status()
        return forecast_response.json()
