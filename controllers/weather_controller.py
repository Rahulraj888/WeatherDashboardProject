from utils.api_client import WeatherAPIClient
from utils.database import Database
from models.weather_data import WeatherData
import logging

logger = logging.getLogger(__name__)

class WeatherController:
    def __init__(self, api_key):
        self.api_client = WeatherAPIClient(api_key)
        self.db = Database()

    def get_current_weather(self, location):
        try:
            data = self.api_client.fetch_current_weather(location)
            logger.debug(f"Weather API response: {data}")
            weather_info = WeatherData(
                location=location,
                temperature=data['main']['temp'],
                humidity=data['main']['humidity'],
                wind_speed=data['wind']['speed'],
                timestamp=data['dt']
            )
            return weather_info
        except Exception as e:
            logger.error(f"Error fetching current weather: {e}")
            return None

    def get_forecast(self, location):
        try:
            data = self.api_client.fetch_forecast(location)
            logger.debug(f"Forecast API response: {data}")
            if 'list' in data:
                return data['list']
            else:
                logger.error(f"API response missing 'list' key: {data}")
                return []
        except Exception as e:
            logger.error(f"Error fetching forecast: {e}")
            return None

    def get_historical_weather(self, lat, lon, timestamp):
        try:
            data = self.api_client.fetch_historical_weather(lat, lon, timestamp)
            return data  # Process and parse the data as needed
        except Exception as e:
            logger.error(f"Error fetching historical weather: {e}")
            return None

    def save_weather_data(self, weather_data: WeatherData):
        try:
            cursor = self.db.get_cursor()
            if cursor:
                cursor.execute("""
                    INSERT INTO weather_data (location, temperature, humidity, wind_speed, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (weather_data.location, weather_data.temperature, weather_data.humidity, weather_data.wind_speed,
                      weather_data.timestamp))
                self.db.connection.commit()
                logger.info("Weather data saved successfully.")
            else:
                logger.error("Failed to get database cursor.")
        except Exception as e:
            logger.error(f"Error saving weather data: {e}")
            self.db.connection.rollback()
