import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "Agentic API"
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "pythonji7@gmail.com")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "svkf erlx xlua qnzl")

settings = Settings()