import logging
from app.config import Config
import google.generativeai as genai


class GeminiAPI:
    @staticmethod
    def configure_api():
        """
        Configures the Gemini API with the API key from the configuration.
        """
        api_key = Config.get_gemini_api_key()
        genai.configure(api_key=api_key)

    @staticmethod
    def create_model(model_name: str, system_instruction: str):
        """
        Creates and returns a Gemini generative model.
        """
        return genai.GenerativeModel(
            model_name=model_name, 
            system_instruction=system_instruction
        )

    @staticmethod
    def fetch_response(context: str, user_message: str) -> str:
        """
        Sends a request to the Gemini API and returns the response.
        """
        GeminiAPI.configure_api()

        try:
            model = GeminiAPI.create_model(
                model_name="gemini-1.5-flash",
                system_instruction="Use source only the text"
            )
            response = model.generate_content([user_message, context])
            return response.text

        except Exception as e:
            error_message = f"Gemini API request failed: {e}"
            logging.error(error_message)
            raise RuntimeError("Gemini API error occurred. Please try again later.") from e
