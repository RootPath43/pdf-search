from sqlalchemy.orm import Session
from app.models import PDF
from app.database import get_db
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
import uuid
import os
from app.custom_logger import logger

UPLOAD_DIRECTORY = "./uploads"

class PDFProcessor:
    
    @staticmethod
    def validate_pdf(file: str) -> bool:
        """PDF dosyasının geçerliliğini kontrol eder."""
        if not file.endswith(".pdf"):
            logger.warning("Invalid file type uploaded.")
            raise ValueError("Invalid file format. Only PDF files are allowed.")
        return True

    @staticmethod
    async def process_pdf(file, db: Session) -> PDF:
        """PDF dosyasını işler ve veritabanına kaydeder."""
        if not os.path.exists(UPLOAD_DIRECTORY):
            logger.info("Invalid file type uploaded.")
            os.makedirs(UPLOAD_DIRECTORY)

        # UUID oluşturulması
        name = uuid.uuid4()
        
        # Dosyayı kaydet
        file_path = await PDFProcessor._save_file(file, name)
        
        # PDF dosyasını yükleyin
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        # Metni parçalara ayırma
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)

        # PDF'in içerik metni
        pdf_content = " ".join([doc.page_content for doc in texts])
        page_count = len(documents)
        
        # Veritabanına kaydet
        pdf = PDF(id=name, filename=file.filename, content=pdf_content, page_count=page_count)
        db.add(pdf)
        db.commit()
        db.refresh(pdf)

        return pdf

    @staticmethod
    async def _save_file(file, name):
        """PDF dosyasını belirtilen dizine kaydeder."""
        file_location = os.path.join(UPLOAD_DIRECTORY, f"{name}.pdf")
        # Asenkron dosya okuma
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())  # Dosyayı asenkron okuma işlemi
        return file_location
