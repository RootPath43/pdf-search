from app.gemini_api import GeminiAPI
from app.models import ChatHistory, PDF
from app.database import get_db
from sqlalchemy.orm import Session
import logging
import uuid 

class ChatProcessor:
    @staticmethod
    def save_chat_history(pdf_id: uuid.UUID, user_message: str, response: str, db: Session):
        """Kullanıcı mesajını ve yanıtını veritabanına kaydeder."""
        chat_history = ChatHistory(pdf_id=pdf_id, user_message=user_message, response=response)
        db.add(chat_history)
        db.commit()
        db.refresh(chat_history)

    @staticmethod
    def process_chat(pdf_id: uuid.UUID, user_message: str, db: Session) -> str:
        """PDF ile etkileşim kurarak yanıt döndürür."""
        # PDF içeriğini al
        pdf = db.query(PDF).filter(PDF.id == pdf_id).first()

        if not pdf:
            raise ValueError("PDF not found in the database.")
        
        # PDF içeriği ile Gemini API'ye istek gönder
        response = GeminiAPI.fetch_response(pdf.content, user_message)

        # Chat geçmişini kaydet
        ChatProcessor.save_chat_history(pdf_id, user_message, response, db)

        return response
