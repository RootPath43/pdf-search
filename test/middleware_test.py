import unittest
from unittest.mock import patch
from starlette.testclient import TestClient

from fastapi import FastAPI, HTTPException
from app.middleware import ErrorHandlingMiddleware
app = FastAPI()
app.add_middleware(
    ErrorHandlingMiddleware
)
@app.get("/test")
async def test_route():
    return {"message": "Hello World"}

@app.get("/error")
async def error_route():
    raise HTTPException(status_code=400, detail="Bad Request")

@app.get("/unhandled")
async def unhandled_route():
    raise Exception("Unhandled error")


class TestErrorHandlingMiddleware(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        patch("app.custom_logger.logger").start()  # Mock the logger
        cls.client = TestClient(app)

    def test_no_error(self):
        """Test a normal request that doesn't raise an error."""
        response = self.client.get("/test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello World"})

    def test_http_exception(self):
        """Test a route that raises an HTTPException."""
        response = self.client.get("/error")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Bad Request"})

    def test_unhandled_exception(self):
        """Test a route that raises a generic exception."""
        response = self.client.get("/unhandled")
        self.assertEqual(response.status_code, 500)
        print(response.json())
        self.assertEqual(response.json(), {"message": "Internal Server Error"})

  