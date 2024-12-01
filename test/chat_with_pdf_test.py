import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app  # Import the FastAPI app
from app.chat import ChatProcessor
from fastapi import HTTPException
import uuid

class TestChatWithPDF(unittest.TestCase):

    def setUp(self):
        # Initialize TestClient for FastAPI
        self.client = TestClient(app)
        self.uuid=uuid.uuid4()

    @patch.object(ChatProcessor, 'process_chat')
    def test_chat_with_pdf_valid(self, mock_process_chat):
        # Mock the behavior of ChatProcessor
        pdf_id = self.uuid  # Mock a valid PDF ID
        user_message = "Hello, how are you?"

        mock_response = "Hello, I am fine."
        mock_process_chat.return_value = mock_response

        response = self.client.post(f"/v1/chat/{pdf_id}", json={"message": user_message})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["response"], "Hello, I am fine.")

    def test_chat_with_pdf_missing_message(self):
        # Simulate sending a request with a missing message field
        pdf_id = uuid.uuid4()
        response = self.client.post(f"/v1/chat/{pdf_id}", json={"message":""}, headers={"Content-Type": "application/json"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Message is required.")

    @patch.object(ChatProcessor, 'process_chat')
    def test_chat_with_pdf_not_found(self, mock_process_chat):
        # Simulate a scenario where the PDF is not found
        pdf_id = self.uuid
        user_message = "What is this PDF about?"

        mock_process_chat.side_effect = ValueError("PDF not found")

        response = self.client.post(f"/v1/chat/{pdf_id}", json={"message": user_message})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "PDF not found.")

    @patch.object(ChatProcessor, 'process_chat')
    def test_chat_with_pdf_processing_error(self, mock_process_chat):
        # Simulate an internal error during chat processing
        pdf_id = self.uuid
        user_message = "Tell me about the PDF"

        mock_process_chat.side_effect = Exception("Error generating response")

        response = self.client.post(f"/v1/chat/{pdf_id}", json={"message": user_message})
        print(response)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["detail"], "Error generating response.")
