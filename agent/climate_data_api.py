import requests
import os

class ClimateDataAPI:
    def __init__(self):
        self.api_key = os.getenv('WEATHERAPI_KEY')
        self.base_url = 'http://api.weatherapi.com/v1'

    def get_current_weather(self, location):
        url = f"{self.base_url}/current.json?key={self.api_key}&q={location}"
        response = requests.get(url)
        return response.json()

    def get_forecast(self, location, days=1):
        url = f"{self.base_url}/forecast.json?key={self.api_key}&q={location}&days={days}"
        response = requests.get(url)
        return response.json()

    def get_historical_weather(self, location, date):
        url = f"{self.base_url}/history.json?key={self.api_key}&q={location}&dt={date}"
        response = requests.get(url)
        return response.json()