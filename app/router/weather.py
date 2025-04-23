
from fastapi import APIRouter, Query, HTTPException
from app.services import external_apis
from app.models import schemas 


router = APIRouter(
    prefix="/data", 
    tags=["Weather & AQI"]
)

@router.get("/now", response_model=schemas.WeatherAQIResponse)
async def get_current_weather_and_aqi(
    lat: float = Query(..., example=12.9716, description="Latitude of the location"),
    lon: float = Query(..., example=77.5946, description="Longitude of the location")
):
    """
    Fetches and returns the current weather and Air Quality Index (AQI)
    for the specified geographical coordinates.
    """
    weather_data = external_apis.get_current_weather(lat, lon)
    aqi_data = external_apis.get_current_aqi(lat, lon)

    # --- Error Handling ---
    weather_error = weather_data.get("error")
    aqi_error = aqi_data.get("error")
    combined_error = None
    if weather_error and aqi_error:
         combined_error = f"Weather Error: {weather_error}; AQI Error: {aqi_error}"
         # If both fail critically, maybe raise exception or return error response
         # Option 1: Raise exception (stops execution here)
         # raise HTTPException(status_code=503, detail=f"Could not fetch external data. Weather: {weather_error}, AQI: {aqi_error}")
         # Option 2: Return error within the response model (allows partial success)
    elif weather_error:
         combined_error = f"Weather Error: {weather_error}"
    elif aqi_error:
         combined_error = f"AQI Error: {aqi_error}"


    # --- Data Mapping (Map raw API dicts to Pydantic models) ---
    # Use .get() with defaults to avoid errors if keys are missing in API response
    location_info = schemas.Location(
        city=weather_data.get("name"), # Get city name from weather data if available
        latitude=lat,
        longitude=lon
    )

    current_weather_info = None
    if not weather_error:
         main_weather = weather_data.get("main", {})
         weather_details = weather_data.get("weather", [{}])[0] # Get first weather condition
         wind_details = weather_data.get("wind", {})
         current_weather_info = schemas.CurrentWeather(
             temperature=main_weather.get("temp"),
             feels_like=main_weather.get("feels_like"),
             temp_min=main_weather.get("temp_min"),
             temp_max=main_weather.get("temp_max"),
             pressure=main_weather.get("pressure"),
             humidity=main_weather.get("humidity"),
             description=weather_details.get("description"),
             icon=weather_details.get("icon"),
             wind_speed=wind_details.get("speed")
         )

    current_aqi_info = None
    if not aqi_error:
         # OWM AQI main components are nested under 'components' key
         # The main 'aqi' value is under the 'main' key in the response list item
         aqi_components = aqi_data.get("components", {})
         current_aqi_info = schemas.CurrentAQI(
             aqi=aqi_data.get("main", {}).get("aqi"),
             co=aqi_components.get("co"),
             no2=aqi_components.get("no2"),
             o3=aqi_components.get("o3"),
             so2=aqi_components.get("so2"),
             pm2_5=aqi_components.get("pm2_5"),
             pm10=aqi_components.get("pm10"),
             # Note: OWM doesn't typically provide NH3 in the main AQI call's components
         )

    # --- Construct final response ---
    response = schemas.WeatherAQIResponse(
        location=location_info,
        current_weather=current_weather_info,
        current_aqi=current_aqi_info,
        error_message=combined_error # Pass any errors back in the response
        # Data source fields have default values in the Pydantic model
    )

    return response