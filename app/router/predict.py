# app/router/predict.py
from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional
from app.services import external_apis, ml_pipeline # Import both services
from app.models import schemas # Import schemas for request/response if needed

# Define a new router specifically for predictions
router = APIRouter(
    prefix="/predict",       # All routes here start with /predict
    tags=["Predictions"]    # Group in API docs
)

# Define a simple response model for the prediction
class PredictionResponse(schemas.BaseModel):
    location: schemas.Location
    predicted_temperature_next_day: Optional[float] = None
    prediction_source: str = "Kly-mate Placeholder Model"
    error_message: Optional[str] = None

@router.get("/nextday/temperature", response_model=PredictionResponse)
async def predict_next_day_temperature(
    lat: float = Query(..., example=12.9716, description="Latitude"),
    lon: float = Query(..., example=77.5946, description="Longitude")
):
    """
    Predicts the approximate average temperature for the next day
    using a placeholder model based on current conditions.
    """
    # 1. Get current weather data to use as input for the placeholder
    current_weather_data = external_apis.get_current_weather(lat, lon)
    location_info = schemas.Location(
        city=current_weather_data.get("name"),
        latitude=lat,
        longitude=lon
    )

    # Handle potential error fetching current weather
    weather_error = current_weather_data.get("error")
    if weather_error:
        return PredictionResponse(location=location_info, error_message=f"Could not get current weather for prediction input: {weather_error}")
        # Or alternatively: raise HTTPException(status_code=503, detail=f"Could not get current weather for prediction input: {weather_error}")

    # 2. Call the placeholder prediction function from ml_pipeline
    predicted_temp = ml_pipeline.make_prediction(current_weather_data)

    # Handle potential error/None from prediction
    pred_error = None
    if predicted_temp is None:
        pred_error = "Prediction failed (model not loaded or internal error)."
        # Decide: return error in response or raise exception
        # raise HTTPException(status_code=500, detail="Prediction failed")

    # 3. Return the prediction
    return PredictionResponse(
        location=location_info,
        predicted_temperature_next_day=predicted_temp,
        error_message=pred_error
    )