import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
cookies = {
    "token": os.getenv("JWT_TOKEN")
}

MODEL = "qwen2.5:0.5b"