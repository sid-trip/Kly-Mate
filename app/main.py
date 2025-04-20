from fastapi import FastAPI
from app.router import weather

app = FastAPI(Title = "Kly-Mate", description="A weather app", version="0.1.0")

@app.get("/")
async def root():
    """
    Root endpoint providing a welcome message.
    """
    return {"message": "Welcome to the Kly-mate API!"}



app.include_router(weather.router)
