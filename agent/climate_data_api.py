"""Climate Data API module to fetch weather data from WeatherAPI."""
import os
import requests

class ClimateDataAPI:
    """A class to fetch weather data from the WeatherAPI."""

    def __init__(self):
        self.api_key = os.getenv('WEATHERAPI_KEY')
        self.base_url = 'http://api.weatherapi.com/v1'

    def get_current_weather(self, location):
        """Fetch the current weather for a specific location."""
        url = f"{self.base_url}/current.json?key={self.api_key}&q={location}"
        response = requests.get(url, timeout=5)
        return response.json()

    def get_forecast(self, location, days=1):
        """Fetch the weather forecast for a specific location."""
        url = f"{self.base_url}/forecast.json?key={self.api_key}&q={location}&days={days}"
        response = requests.get(url, timeout=5)
        return response.json()

    def get_historical_weather(self, location, date):
        """Fetch the historical weather data for a specific location and date."""
        url = f"{self.base_url}/history.json?key={self.api_key}&q={location}&dt={date}"
        response = requests.get(url, timeout=5)
        return response.json()
