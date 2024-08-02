from dataclasses import dataclass


@dataclass
class WeatherData:
    location: str
    temperature: float
    humidity: float
    wind_speed: float
    timestamp: int
