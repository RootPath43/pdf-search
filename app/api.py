from fastapi import (
    FastAPI, 
    UploadFile, 
    File, 
    HTTPException, 
    Depends,
    APIRouter
)
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.pdf_processing import PDFProcessor
from app.chat import ChatProcessor
from app.database import get_db
import logging
import uuid 
from app.custom_logger import logger
from app.validation import MessageRequest
# Create the router for v1
v1_router = APIRouter()

@v1_router.post("/pdf")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    PDF dosyasını yükler, işleyip veritabanına kaydeder.
    """
    try:
        logger.info(f"Received file upload: {file.filename}")
        PDFProcessor.validate_pdf(file.filename)
    
        pdf = await PDFProcessor.process_pdf(file, db)
        
        return JSONResponse(content={"pdf_id": str(pdf.id), "pdf_filename": pdf.filename})
    except ValueError as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error processing PDF.")

@v1_router.post("/chat/{pdf_id}")
async def chat_with_pdf(pdf_id: uuid.UUID, message: MessageRequest, db: Session = Depends(get_db)):
    """
    Kullanıcı mesajına dayalı olarak PDF ile etkileşime girer ve veritabanında chat geçmişini saklar.
    """
    user_message = message.message
    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required.")

    try:
        response = ChatProcessor.process_chat(pdf_id, user_message, db)
        return JSONResponse(content={"response": response})
    except ValueError as e:
        logging.error(f"Error retrieving PDF or processing chat: {str(e)}")
        raise HTTPException(status_code=404, detail="PDF not found.")
    except Exception as e:
        logging.error(f"Error generating response for {pdf_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating response.")


