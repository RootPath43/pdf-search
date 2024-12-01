import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app  # Import the FastAPI app
from app.pdf_processing import PDFProcessor
from fastapi import HTTPException


class TestUploadPDF(unittest.TestCase):

    def setUp(self):
        # Initialize TestClient for FastAPI
        self.client = TestClient(app)

    @patch.object(PDFProcessor, 'validate_pdf')
    @patch.object(PDFProcessor, 'process_pdf')
    def test_upload_pdf_valid(self, mock_process_pdf, mock_validate_pdf):
        # Mock the behavior of PDFProcessor methods
        file_mock = MagicMock()
        file_mock.filename = "test.pdf"
        
        # Mock the processing step
        mock_process_pdf.return_value = MagicMock(id=1, filename="test.pdf")

        # Simulate a POST request to upload a PDF file
        response = self.client.post("/v1/pdf", files={"file": ("test.pdf", open("test.pdf", "rb"))})

        self.assertEqual(response.status_code, 200)
        self.assertIn("pdf_id", response.json())
        self.assertEqual(response.json()["pdf_filename"], "test.pdf")

    @patch.object(PDFProcessor, 'validate_pdf')
    def test_upload_pdf_invalid_file(self, mock_validate_pdf):
        # Simulate uploading an invalid file (non-PDF)
        file_mock = MagicMock()
        file_mock.filename = "test.txt"

        # Validate the invalid file to trigger a ValueError
        mock_validate_pdf.side_effect = ValueError("Invalid file format. Only PDF files are allowed.")

        response = self.client.post("/v1/pdf", files={"file": ("test.txt", open("test.txt", "rb"))})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Invalid file format. Only PDF files are allowed.")

    @patch.object(PDFProcessor, 'validate_pdf')
    def test_upload_pdf_processing_error(self, mock_validate_pdf):
        # Simulate an exception during PDF processing
        file_mock = MagicMock()
        file_mock.filename = "test.pdf"
        mock_validate_pdf.return_value = True

        # Simulate an internal server error during PDF processing
        with patch.object(PDFProcessor, 'process_pdf', side_effect=Exception("Error processing PDF")):
            response = self.client.post("/v1/pdf", files={"file": ("test.pdf", open("test.pdf", "rb"))})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["detail"], "Error processing PDF.")
