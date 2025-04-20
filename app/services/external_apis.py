# app/services/external_apis.py
import requests
from app.core.config import OPENWEATHERMAP_API_KEY # Import your key

# Base URL for OpenWeatherMap API
OWM_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
OWM_AQI_URL = "http://api.openweathermap.org/data/2.5/air_pollution" # Example AQI endpoint

def get_current_weather(lat: float, lon: float) -> dict:
    """Fetches current weather data from OpenWeatherMap."""
    if not OPENWEATHERMAP_API_KEY:
        return {"error": "API key not configured"}

    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": "metric" # Or "imperial"
    }
    try:
        response = requests.get(OWM_WEATHER_URL, params=params, timeout=10) # Add timeout
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {"error": f"Could not fetch weather data: {e}"}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": "An unexpected error occurred"}

def get_current_aqi(lat: float, lon: float) -> dict:
    """Fetches current AQI data from OpenWeatherMap."""
    if not OPENWEATHERMAP_API_KEY:
         return {"error": "API key not configured"}

    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHERMAP_API_KEY,
    }
    try:
        response = requests.get(OWM_AQI_URL, params=params, timeout=10)
        response.raise_for_status()
        # The actual data might be nested, e.g., under a 'list' key
        data = response.json()
        # OWM AQI data is often in a list, return the first element if present
        return data['list'][0] if data.get('list') else {"error": "AQI data format unexpected"}
    except requests.exceptions.RequestException as e:
         print(f"Error fetching AQI data: {e}")
         return {"error": f"Could not fetch AQI data: {e}"}
    except (KeyError, IndexError, TypeError) as e:
         print(f"Error parsing AQI data: {e}")
         return {"error": "Could not parse AQI data"}
    except Exception as e:
         print(f"An unexpected error occurred fetching AQI: {e}")
         return {"error": "An unexpected error occurred"}

# --- You might need a different function/API for AQI if OWM doesn't suffice ---