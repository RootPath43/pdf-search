import logging
import json
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the default log level
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.StreamHandler(),  # Log to console
        # logging.FileHandler("app.log", mode='a')  # Log to a file
    ]
)

# Logger instance
logger = logging.getLogger("pdf_app")

# Optional: Add structured logging in JSON format for file handler
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

# file_handler = logging.FileHandler("app.json", mode='a')
# file_handler.setFormatter(JSONFormatter())
# logger.addHandler(file_handler)