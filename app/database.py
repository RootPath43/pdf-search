from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str
    GEMINI_API_KEY: str
    
    class Config:
        env_file = ".env"

# .env dosyasından veritabanı URL'sini al
settings = Settings()

# SQLAlchemy veritabanı motoru
engine = create_engine(settings.DATABASE_URL, echo=True)

# SQLAlchemy oturum sınıfı
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tüm modellerin temel sınıfı
Base = declarative_base()

# Veritabanı bağlantısını almak için yardımcı fonksiyon
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
