import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    @staticmethod
    def get_gemini_api_key():
        """Gemini API anahtarını alır, eğer eksikse hata fırlatır."""
        api_key = Config.GEMINI_API_KEY
        if not api_key:
            raise ValueError("Gemini API key is missing in the .env file.")
        return api_key
