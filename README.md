# Kly-mate Backend API ☁️🌡️

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/) [![Framework](https://img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)

The backend API service for the Kly-mate project. It provides current weather conditions, Air Quality Index (AQI) data, and placeholder weather predictions based on geographical coordinates.

**Live Website:** [https://kly-mate.streamlit.app/](https://kly-mate.streamlit.app/)

**Live API Base URL:** [https://kly-mate.onrender.com/](https://kly-mate.onrender.com/),

**Live API Docs (Swagger UI):** [https://kly-mate.onrender.com/docs](https://kly-mate.onrender.com/docs),

## ✨ Features

* Fetches real-time weather data from OpenWeatherMap.
* Fetches real-time Air Quality Index (AQI) data from OpenWeatherMap.
* Provides a placeholder endpoint demonstrating a future ML temperature prediction.
* Uses Pydantic for data validation and serialization.
* Automatic interactive API documentation via Swagger UI and ReDoc.

## 🛠️ Technologies Used

* **Framework:** FastAPI
* **Server:** Uvicorn
* **Data Handling:** Pandas, NumPy
* **External APIs:** Requests
* **ML (Structure):** Scikit-learn, Joblib (currently uses a placeholder model)
* **Configuration:** Python-dotenv
* **Language:** Python 3.10+
* **Deployment:** Render

## 📂 Project Structure

<pre>
Klymate_backend/
├── venv/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── router/
│   │   ├── __init__.py
│   │   ├── predict.py
│   │   └── weather.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── external_apis.py
│   │   └── ml_pipeline.py
│   └── ml_models/
│       └── placeholder_model.joblib
├── data/
│   └── Bangalore_1990_2022_BangaloreCity.csv
├── .env
├── .gitignore
├── create_dummy_model.py
└── requirements.txt
</pre>

## 🚀 Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/Kly-mate.git](https://github.com/YourUsername/Kly-mate.git)
    "
    cd Klymate_backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows (PowerShell): .\venv\Scripts\Activate.ps1
    # On Linux/macOS: source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

1.  **API Keys:** This application requires an API key from [OpenWeatherMap](https://openweathermap.org/api).
2.  **Create `.env` file:** Create a file named `.env` in the project root (`Klymate_backend/`).
3.  **Add Keys:** Add your API key to the `.env` file:
    ```dotenv
    OPENWEATHERMAP_API_KEY=YOUR_ACTUAL_OPENWEATHERMAP_KEY
    ```
    *(Note: The `.env` file is listed in `.gitignore` and should not be committed.)*

4.  **Placeholder Model:** Ensure the placeholder model exists. If not, run the creation script (ensure `app/ml_models` dir exists):
    ```bash
    python create_dummy_model.py
    ```

## ▶️ Running Locally

1.  Ensure your virtual environment is activated.
2.  Ensure your `.env` file is configured.
3.  Run the Uvicorn development server:
    ```bash
    uvicorn app.main:app --reload
    ```
4.  Access the API at `http://127.0.0.1:8000`.
5.  Access the interactive documentation at `http://127.0.0.1:8000/docs`.

## 🔗 API Endpoints

* **`GET /`**: Welcome message.
* **`GET /data/now`**: Retrieves current weather and AQI data.
    * Query Parameters: `lat` (float), `lon` (float).
* **`GET /predict/nextday/temperature`**: Retrieves a *placeholder* temperature prediction for the next day based on current conditions.
    * Query Parameters: `lat` (float), `lon` (float).

*Refer to the interactive `/docs` endpoint for detailed request/response schemas.*

## ☁️ Deployment

This API is automatically deployed on [Render](https://render.com/) from the `main` branch.

* **Live API:** [https://kly-mate.onrender.com/](https://kly-mate.onrender.com/)
* **Live Docs:** [https://kly-mate.onrender.com/docs](https://kly-mate.onrender.com/docs)

## 🔮 Future Work

* Implement actual ML model training pipeline using historical data.
* Replace placeholder prediction with real ML model output.
* Add endpoint for comparing Kly-mate prediction with external forecasts.
* Add database integration for storing historical data or user preferences.
* Enhance error handling and logging.

---
