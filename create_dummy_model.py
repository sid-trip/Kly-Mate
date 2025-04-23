# create_dummy_model.py
import joblib
from pathlib import Path
import os

print("Attempting to save dummy model...")

# Define where the model should be saved (inside app/ml_models/)
# Use absolute path or ensure correct relative path from where you run this script
MODEL_DIR = Path(__file__).parent / "app" / "ml_models"
MODEL_PATH = MODEL_DIR / "placeholder_model.joblib"

# Ensure the target directory exists
try:
    os.makedirs(MODEL_DIR, exist_ok=True)
    print(f"Directory {MODEL_DIR} ensured.")
except Exception as e:
    print(f"ERROR: Could not create directory {MODEL_DIR}: {e}")
    exit() # Stop if we can't create the directory

# Create a very simple placeholder object (a dictionary is fine)
dummy_model_object = {
    "model_type": "Placeholder",
    "description": "This is not a real ML model. Replace with actual trained model later.",
    "prediction_info": "Returns input temp + 1 for demo."
}

# Save the dummy object using joblib
try:
    joblib.dump(dummy_model_object, MODEL_PATH)
    print(f"SUCCESS: Dummy model saved to {MODEL_PATH}")
except Exception as e:
    print(f"ERROR: Failed to save dummy model to {MODEL_PATH}: {e}")