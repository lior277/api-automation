import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
    USERNAME = os.getenv("USERNAME", "demo")
    PASSWORD = os.getenv("PASSWORD", "demo")
