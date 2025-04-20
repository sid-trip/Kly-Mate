import os
from dotenv import load_dotenv

load_dotenv()


OPENWEATHERMAP_API_KEY:str|None=os.getenv("OPENWEATHERMAP_API_KEY")
if not OPENWEATHERMAP_API_KEY:
    print("Warning : No open weather api key found in .env!")