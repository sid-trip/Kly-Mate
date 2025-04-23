from fastapi import FastAPI
from app.router import weather
from app.router import predict

app = FastAPI(title = "Kly-Mate", description="A weather app", version="0.1.0")

@app.get("/")
async def root():
    """
    Root endpoint providing a welcome message.
    """
    return {"message": "Welcome to the Kly-mate API!"}



app.include_router(weather.router)
app.include_router(predict.router)
