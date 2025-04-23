# app/services/ml_pipeline.py
import pandas as pd
import joblib
from pathlib import Path
import numpy as np
from typing import Optional # Added for type hinting

print("DEBUG: ml_pipeline.py loaded") # Add this temporary print

# Define paths relative to this file's location
# Assumes ml_pipeline.py is in app/services/
# Goes up two levels (to app, then to Klymate_backend root) then into 'data'
DATA_DIR = Path(__file__).parent.parent.parent / "data"
# Assumes ml_models folder is inside 'app' directory
MODEL_DIR = Path(__file__).parent.parent / "ml_models"

# !!! IMPORTANT: CHANGE THIS FILENAME if yours is different !!!
SAMPLE_DATA_PATH = DATA_DIR / "Bangalore_1990_2022_BangaloreCity.csv"
MODEL_PATH = MODEL_DIR / "placeholder_model.joblib"

def load_historical_data(csv_path: Path = SAMPLE_DATA_PATH) -> Optional[pd.DataFrame]:
    """Loads historical weather data from the specified CSV file."""
    print(f"DEBUG: Attempting to load data from: {csv_path}") # Add print
    if not csv_path.exists():
        print(f"ERROR: Sample data file not found at {csv_path}")
        return None
    try:
        # Load the CSV
        df = pd.read_csv(csv_path)

        # --- Basic Preprocessing ---
        # 1. Parse the 'time' column into datetime objects
        #    Use errors='coerce' to turn unparseable dates into NaT (Not a Time)
        df['time'] = pd.to_datetime(df['time'], errors='coerce')
        print(f"DEBUG: Parsed 'time' column. Sample: {df['time'].iloc[0]}") # Add print

        # 2. Handle potential missing dates after coercion
        df.dropna(subset=['time'], inplace=True)

        # 3. Set the 'time' column as the index (often useful for time series)
        df.set_index('time', inplace=True)
        print("DEBUG: Set 'time' as index.") # Add print

        # 4. Handle missing values in numeric columns (e.g., fill with forward fill)
        #    Check column names from your CSV screenshot: tavg, tmin, tmax, prcp
        numeric_cols = ['tavg', 'tmin', 'tmax', 'prcp']
        # Check which columns actually exist before trying to fill
        cols_to_fill = [col for col in numeric_cols if col in df.columns]
        if cols_to_fill:
             df[cols_to_fill] = df[cols_to_fill].fillna(method='ffill').fillna(method='bfill') # Forward fill then back fill
             print(f"DEBUG: Filled NA in columns: {cols_to_fill}") # Add print

        # 5. Optional: Sort by date index (good practice)
        df.sort_index(inplace=True)
        print(f"DEBUG: Data sorted by index. Shape: {df.shape}") # Add print

        print(f"INFO: Successfully loaded and preprocessed data from {csv_path}")
        return df
    except Exception as e:
        print(f"ERROR: Failed during loading/processing of {csv_path}: {e}")
        return None

# --- Model loading and prediction functions will go below ---





# Add these functions BELOW load_historical_data in app/services/ml_pipeline.py

def load_prediction_model(model_path: Path = MODEL_PATH):
    """Loads the prediction model from the specified joblib file."""
    print(f"DEBUG: Attempting to load model from: {model_path}") # Add print
    if not model_path.exists():
        print(f"ERROR: Model file not found at {model_path}")
        return None
    try:
        model = joblib.load(model_path)
        print(f"INFO: Model loaded successfully from {model_path}")
        print(f"DEBUG: Loaded model content: {model}") # See what was loaded
        return model
    except Exception as e:
        print(f"ERROR: Failed to load model from {model_path}: {e}")
        return None

# --- Load the model when this module is first imported ---
# This means the model is loaded once when the FastAPI app starts,
# rather than every time a prediction is made.
print("DEBUG: Attempting to load model globally...")
loaded_placeholder_model = load_prediction_model()
if loaded_placeholder_model is None:
     print("WARNING: Global model loading failed.")
else:
     print("INFO: Global model loaded successfully.")
# ---

def make_prediction(current_weather_data: dict) -> Optional[float]:
    """
    Uses the loaded placeholder 'model' to simulate a weather prediction.

    Args:
        current_weather_data: A dictionary containing current weather info,
                              likely from the get_current_weather service call.

    Returns:
        A float representing the predicted temperature, or None if prediction fails.
    """
    print(f"DEBUG: make_prediction called with data: {current_weather_data}") # Add print
    if loaded_placeholder_model is None:
        print("ERROR: Prediction impossible: Model not loaded.")
        return None

    # --- Placeholder Prediction Logic ---
    # In a real scenario:
    # 1. Extract relevant features from current_weather_data.
    # 2. Preprocess/transform features into the format the *real* model expects (e.g., scaling, numpy array).
    # 3. Call loaded_model.predict(processed_features)

    # For THIS DEMO using the placeholder:
    try:
        # Let's use the logic described in the dummy model dictionary
        # Get current temperature from the input data
        current_temp = current_weather_data.get("main", {}).get("temp")
        print(f"DEBUG: Current temp from input: {current_temp}") # Add print

        if current_temp is not None and isinstance(current_temp, (int, float)):
             # Simple demo logic: predict current temp + 1
             predicted_temp = float(current_temp) + 1.0
             print(f"DEBUG: Predicted temp: {predicted_temp}") # Add print
             return round(predicted_temp, 2)
        else:
             # Fallback if current temp isn't available or not a number
             print("WARN: Current temperature not found or invalid in input, returning default prediction.")
             return 25.0 # Default prediction
    except Exception as e:
        print(f"ERROR: Exception during prediction logic: {e}")
        return None