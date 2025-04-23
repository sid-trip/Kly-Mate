from pydantic import BaseModel
from typing import Optional

class Location(BaseModel):
    city: Optional[str] = None # City name might not always come from API
    latitude: float
    longitude: float

# Define a model for the current weather data points you care about
class CurrentWeather(BaseModel):
    temperature: Optional[float] = None
    feels_like: Optional[float] = None
    temp_min: Optional[float] = None
    temp_max: Optional[float] = None
    pressure: Optional[int] = None
    humidity: Optional[int] = None
    description: Optional[str] = None
    wind_speed: Optional[float] = None

# Define a model for the current AQI data points
class CurrentAQI(BaseModel):
    aqi: Optional[int] = None # Main AQI value (e.g., US EPA standard 1-5)
    co: Optional[float] = None # Carbon Monoxide
    no2: Optional[float] = None # Nitrogen Dioxide
    o3: Optional[float] = None # Ozone
    so2: Optional[float] = None # Sulphur Dioxide
    pm2_5: Optional[float] = None # Fine Particulate Matter
    pm10: Optional[float] = None # Coarse Particulate Matter

# Define the overall response model combining all parts
class WeatherAQIResponse(BaseModel):
    location: Location
    current_weather: Optional[CurrentWeather] = None # Use Optional in case fetching fails
    current_aqi: Optional[CurrentAQI] = None # Use Optional in case fetching fails
    weather_data_source: str = "OpenWeatherMap" # Identify where data came from
    aqi_data_source: str = "OpenWeatherMap" # Identify where data came from
    error_message: Optional[str] = None # Field to pass errors back if needed
    