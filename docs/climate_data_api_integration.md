# Climate Data API Integration

## Overview

This document provides an overview of the integration with WeatherAPI.com to gather climate data.

## API Key Setup

To use the WeatherAPI.com, you need to set up an API key. Follow these steps:
1. Sign up at [WeatherAPI.com](http://api.weatherapi.com) and obtain an API key.
2. Set the API key as an environment variable:
   ```bash
   export WEATHERAPI_KEY='your_api_key'
   ```

## Usage

### Initialization

Create an instance of the `ClimateDataAPI` class:

```python
from agent.climate_data_api import ClimateDataAPI

climate_api = ClimateDataAPI()
```

### Get Current Weather

Fetch the current weather for a specific location:

```python
location = 'London'
current_weather = climate_api.get_current_weather(location)
print(current_weather)
```

### Get Weather Forecast

Fetch the weather forecast for a specific location:

```python
location = 'London'
forecast_days = 3
forecast = climate_api.get_forecast(location, forecast_days)
print(forecast)
```

### Get Historical Weather

Fetch the historical weather data for a specific location and date:

```python
location = 'London'
date = '2023-01-01'
historical_weather = climate_api.get_historical_weather(location, date)
print(historical_weather)
```