import unittest
from unittest.mock import patch, MagicMock
from app.gemini_api import GeminiAPI


class TestGeminiAPI(unittest.TestCase):

    @patch("app.config.Config.get_gemini_api_key")
    @patch("google.generativeai.configure")
    def test_configure_api(self, mock_configure, mock_get_api_key):
        # Arrange
        mock_get_api_key.return_value = "mock-api-key"

        # Act
        GeminiAPI.configure_api()

        # Assert
        mock_get_api_key.assert_called_once()
        mock_configure.assert_called_once_with(api_key="mock-api-key")

   
    @patch("app.gemini_api.GeminiAPI.create_model")
    @patch("app.gemini_api.GeminiAPI.configure_api")
    def test_fetch_response_success(self, mock_configure_api, mock_create_model):
        # Arrange
        mock_model = MagicMock()
        mock_model.generate_content.return_value.text = "mock-response-text"
        mock_create_model.return_value = mock_model

        context = "Provide a concise summary of this document."
        user_message = "What is this text about?"

        # Act
        response_text = GeminiAPI.fetch_response(context, user_message)

        # Assert
        mock_configure_api.assert_called_once()
        mock_create_model.assert_called_once_with(
            model_name="gemini-1.5-flash",
            system_instruction="Use source only the text"
        )
        mock_model.generate_content.assert_called_once_with([user_message, context])
        self.assertEqual(response_text, "mock-response-text")

    @patch("app.gemini_api.GeminiAPI.create_model")
    @patch("app.gemini_api.GeminiAPI.configure_api")
    @patch("logging.error")
    def test_fetch_response_failure(self, mock_logging_error, mock_configure_api, mock_create_model):
        # Arrange
        mock_create_model.side_effect = Exception("API request failed")

        context = "Provide a concise summary of this document."
        user_message = "What is this text about?"

        # Act & Assert
        with self.assertRaises(RuntimeError) as context_manager:
            GeminiAPI.fetch_response(context, user_message)

        self.assertEqual(
            str(context_manager.exception),
            "Gemini API error occurred. Please try again later."
        )
        mock_logging_error.assert_called_once_with("Gemini API request failed: API request failed")
