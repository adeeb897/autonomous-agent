import requests
import json

# Placeholder for OpenWeatherMap API Key
API_KEY = 'YOUR_API_KEY_HERE'

# Base URL for OpenWeatherMap API
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Function to fetch weather data for a given city
def fetch_weather_data(city_name):
    params = {
        'q': city_name,
        'appid': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Example usage
if __name__ == '__main__':
    city = 'London'
    weather_data = fetch_weather_data(city)
    if weather_data:
        print(json.dumps(weather_data, indent=4))
    else:
        print('Failed to fetch weather data')