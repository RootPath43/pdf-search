from fastapi import FastAPI
import logging
from app.api import v1_router
from app.middleware import ErrorHandlingMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Logger kurulumu
logging.basicConfig(level=logging.INFO)

# V1 version
app.include_router(v1_router, prefix="/v1", tags=["v1"])

#custom middleware
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(   
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

    )