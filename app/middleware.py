from starlette.middleware.base import BaseHTTPMiddleware
from app.custom_logger import logger
from fastapi import FastAPI, Request, HTTPException
from starlette.responses import JSONResponse

# Custom error handling middleware
class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # Call the request handler and get the response
            response = await call_next(request)
            return response
        except HTTPException as exc:
            logger.error(f"HTTP Exception: {exc.detail}")
            return JSONResponse(
                status_code=exc.status_code,
                content={"message": exc.detail},
            )
        except Exception as exc:
            logger.error(f"Unhandled exception: {str(exc)}")
            return JSONResponse(
                status_code=500,
                content={"message": "Internal Server Error"},
            )
