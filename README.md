# pdf-search

# Overview
Bu proje, kullanıcıların PDF dosyalarını işleyip metin tabanlı sorgulara yanıt verebilmelerini sağlayan bir API sunar. Kullanıcı mesajlarına dayalı olarak PDF'den bilgi çekebilir ve sohbet geçmişini kaydedebilir.

# Features

Projenin Temel Özellikleri:

PDF işleme ve doğrulama
Kullanıcı mesajlarına dayalı içerik oluşturma (Chat API)
Sohbet geçmişini veritabanına kaydetme
Gelişmiş hata yönetimi ve özel middleware
Ayrıntılı logging 

# Technology
Projenin Teknolojileri ve Araçları:

Backend: FastAPI
Veritabanı: PostgreSQL (SQLAlchemy kullanılarak)
Diğer:
    PDF İşleme: PyPDF2 veya pdfplumber
    Model API: Google Gemini API
    Logging: Python logging modülü
    Metni parçalara bölme: langchain
    Migration işlemleri: alembic 


# Project Structure
```bash
.
├── alembic.ini
├── app
│   ├── api.py  :APIların bulunduğu py dosyası
│   ├── chat.py :Chat ile ilgili db işlemlerinin gerçekleştiği ve gemini api çağırıldığı dosya
│   ├── config.py : Gemini key konfigürasyonu kontrol eden dosya
│   ├── custom_logger.py: Log conf içeren dosya
│   ├── database.py: DB bağlantısının oluşturulduğu dosya
│   ├── gemini_api.py: Gemini api kullanıldığı dosya
│   ├── __init__.py
│   ├── main.py : Ana uygulama
│   ├── middleware.py : Özel middleware
│   ├── migrations : Db üzerinde yapılacak değişikliklerin kaydedildiği migrations dosyası
│   │   ├── env.py
│   │   ├── __init__.py
│   │   ├── README
│   │   ├── script.py.mako
│   │   └── versions
│   │       └── e1d99d5144bb_initial_migration.py
│   ├── models.py : Dbde bulunan tabloların bulunduğu dosya
│   ├── pdf_processing.py : Pdf işlemleri 
│   └── validation.py : Mesaj için pydantic classlarının bulunduğu dosya

├── docker-compose.yaml
├── dockerfile
├── LICENSE
├── logs
├── README.md
├── requirements.txt
├── test :Unittestler
│   ├── chat_with_pdf_test.py
│   ├── __init__.py
│   ├── middleware_test.py
│   └── pdf_test.py
├── test.pdf
├── test.txt
└── uploads: Pdflerin yüklendiği klasör
```


# Installation
Uygulamayı iki türlü çalıştırabilirsiniz. İster docker-compose kullanarak, isterseniz lokal bilgisayarızda bir ortam oluşturarak çalıştırabilirsiniz.
1. Docker-compose ile çalıştırma
1.1  Docker Compose'u kullanabilmek için öncelikle Docker'ı sisteminize yüklemeniz gerekiyor. Aşağıdaki linkten kurulum ile ilgili dokümantasyona erişebilirsiniz
https://docs.docker.com/compose/install/

1.2 Repository'i klonlayın ve ilgili klasöre geçin
git clone https://github.com/RootPath43/pdf-search.git
cd pdf-search

1.3 Dosya içersiinde .env dosyası oluşturulmalıdır. Dosyanın içerisinde DATABASE_URL ve GEMINI API_KEY bulundurmalı ve kaydetmelisiniz.
DATABASE_URL=postgresql://username:password@localhost/db-name 
GEMINI_API_KEY=gemini api key

1.4 Docker-compose build işlemi, aşağıdaki komut ile uygulama çalıştırılmaya hazırlanır
sudo docker-compose build 

1.5 Docker-compose run işlemi, aşağıdaki komut ile hem db hem uygulama çalışıtırılır. Uygulama localhost:8000 portunda çalışacaktır

2. Virtual Enviroment kullanarak lokalde çalıştırma

1.1  Repository'i klonlayın ve ilgili klasöre geçin
git clone https://github.com/RootPath43/pdf-search.git
cd pdf-search

1.2  Virtual enviroment oluşturulur. Python 3.11 sürümü için oluşturmanız önerilir.
Python indirmek için https://www.python.org/downloads/ linkinden yardım alabilirsiniz.
Virtual enviroment kurulumu için ilgili linki takip edebilirsiniz.
https://virtualenv.pypa.io/en/latest/

1.3 Postgresql indirin. https://www.postgresql.org/download/   linkinden yardım alabilirsiniz.

1.4 Postgresql indirildikten sonra bir Db oluşturun.

1.5 Proje dosyası içersiinde .env dosyası oluşturulmalıdır. Dosyanın içerisinde DATABASE_URL ve GEMINI API_KEY bulundurmalı ve kaydetmelisiniz.
DATABASE_URL=postgresql://username:password@localhost/db-name 
GEMINI_API_KEY=gemini api key

1.6 Virtualenv aktive edin. Bu linkten yardım alabilirsiniz.
https://virtualenv.pypa.io/en/latest/

1.7 Virtualenv aktive edildikten sonra gereksinimler indilirir. Onun için
pip install -r requirements.txt

1.8 Db migrate yapılması için alembic kullanılmaktadır.
alembic upgrade head    komutu ile migrate işlemini gerçekleştiriyoruz

1.9 Unit Testleri çalıştırma
python -m unittest test

1.9  API çalıştırma
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload komutu ile çalıştırılır. Uygulama localhost:8000 portunda çalışacaktır.

# API request and responses
Uygulama çalıştırıldıktan sonra atılabilecek istekler aşağıdaki gibidir.
1. PDF yüklenmesi . Bu istek ile pdf yüklenir ve uploads klasörüne kaydedilir. Pdf içeriği db ye kaydedilir. Ve içerik langchain ile chunklara ayırılır.
curl -X POST "http://localhost:8000/v1/pdf" -F "file=@/path/to/your/pdf/file.pdf"

Bu isteğin cevabı olarak şöyle bir json döndürülür.

{
    "pdf_id": "c8da9564-85e0-42e1-98af-8787202d49cc",
    "pdf_filename": "yüklediğini_pdf_ismi.pdf"
}

2. Pdf üzerinden chat. Belirtilen pdf db'den getirlir. İçeriği Gemini 1.5 flash'a gönderilir.Dönüt kulanıcıya iletilir. 
curl -X POST "http://localhost:8000/v1/chat/{pdf_id}" \
-H "Content-Type: application/json" \
-d '{"message": "Pdfin konusu nedir"}'

Bu isteğin cevabı olarak şöyle bir json döndürlür.

{
    "response": "Sorduğunuz soruya cevap"
}

![alt text](<Screenshot from 2024-12-02 14-16-02.png>)

