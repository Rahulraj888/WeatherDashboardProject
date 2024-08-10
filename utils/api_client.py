import requests
import logging

logger = logging.getLogger(__name__)

class WeatherAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_current_weather(self, location):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            if 'main' in data:
                return data
            else:
                logger.error(f"API response missing 'main' key: {data}")
                return {}
        else:
            logger.error(f"Error fetching data from API: {data}")
            return {}

    def fetch_forecast(self, location):
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error fetching forecast data from API: {response.json()}")
            return {}

    def fetch_historical_weather(self, lat, lon, timestamp):
        url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={timestamp}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        return response.json()
