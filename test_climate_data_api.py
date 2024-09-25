import os
from agent.climate_data_api import ClimateDataAPI

def test_climate_data_api():
    # Initialize the API
    climate_api = ClimateDataAPI()

    # Test current weather
    current_weather = climate_api.get_current_weather('London')
    assert 'location' in current_weather, "Current weather data should contain 'location'"
    assert 'current' in current_weather, "Current weather data should contain 'current'"
    print("Current weather test passed.")

    # Test forecast
    forecast = climate_api.get_forecast('London', days=3)
    assert 'location' in forecast, "Forecast data should contain 'location'"
    assert 'forecast' in forecast, "Forecast data should contain 'forecast'"
    print("Forecast test passed.")

    # Test historical weather
    historical_weather = climate_api.get_historical_weather('London', '2023-01-01')
    assert 'location' in historical_weather, "Historical weather data should contain 'location'"
    assert 'forecast' in historical_weather, "Historical weather data should contain 'forecast'"
    print("Historical weather test passed.")

if __name__ == "__main__":
    test_climate_data_api()