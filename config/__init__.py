import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
cookies = {
    "token": os.getenv("JWT_TOKEN")
}

MODELS = ["openai/gpt-oss-120b:free", "z-ai/glm-4.5-air:free"]
