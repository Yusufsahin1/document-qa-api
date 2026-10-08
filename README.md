# 📄 Document QA API (RAG-based Document Question Answering)

[English](#english) | [Türkçe](#türkçe)

---

<a name="english"></a>
# English

A production-ready **Retrieval-Augmented Generation (RAG)** API built with **FastAPI**, **FAISS**, **SentenceTransformers**, and **OpenAI GPT-4o-mini**.

This system allows users to upload PDF documents, automatically index their content using dense vector embeddings, and ask questions to receive precise, context-aware answers backed by source citations (page numbers, score, and original filenames).

## ✨ Key Features

- **PDF Ingestion & Processing:** Text extraction using `PyMuPDF` with sliding-window chunking.
- **Local Vector Embeddings:** Generated via `SentenceTransformers` (`all-MiniLM-L6-v2`) without external embedding API costs.
- **FAISS Vector Indexing:** Fast similarity search with persistent `.faiss` indices and JSON metadata storage.
- **UUID-based Storage:** Conflict-free, safe file storage supporting special/international characters (e.g., Turkish).
- **Anti-Hallucination RAG Prompting:** OpenAI `gpt-4o-mini` answers questions strictly based on retrieved context.
- **Source Attribution:** API JSON responses include a detailed `sources` array containing page numbers, similarity scores, and original filenames for full transparency.
- **Document Management:** Full CRUD support for listing (`GET /documents`) and deleting (`DELETE /documents/{id}`) documents and their associated indices.
- **Automated Testing:** Unit and endpoint test coverage using `pytest` and `httpx`.

## 🏗️ Project Architecture

```
document-qa-api/
├── app/
│   ├── main.py                  # FastAPI application entry point
│   ├── api/
│   │   └── routes/
│   │       ├── documents.py     # Upload, List, Delete endpoints
│   │       └── query.py         # RAG query ask endpoint
│   ├── core/
│   │   └── config.py            # Environment variables configuration
│   ├── models/
│   │   └── schemas.py           # Pydantic schemas (AskRequest, etc.)
│   ├── services/
│   │   ├── pdf_service.py       # PyMuPDF text extraction
│   │   ├── chunking_service.py  # Text chunking logic
│   │   ├── embedding_service.py # SentenceTransformer singleton
│   │   ├── vector_service.py    # FAISS CRUD operations
│   │   ├── retrieval_service.py # Similar chunk search logic
│   │   └── llm_service.py       # RAG prompt engineering & OpenAI client
│   └── storage/                 # Local filesystem storage (Git ignored)
│       ├── uploads/
│       ├── faiss_index/
│       └── metadata/
├── tests/                       # Pytest test suite
│   ├── test_health.py
│   ├── test_documents.py
│   └── test_query.py
├── .env                         # API keys (Not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.11+
- Conda (Recommended)

### 2. Environment Setup

Clone the repository and create the Conda environment:

```bash
conda create -n document-qa python=3.11 -y
conda activate document-qa
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the project root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 🏃 Running the Application

Start the FastAPI development server with Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

- **Interactive API Documentation (Swagger UI):** `http://127.0.0.1:8000/docs`
- **ReDoc Documentation:** `http://127.0.0.1:8000/redoc`

### 🐋 Running with Docker (Alternative)

Build and run the application using Docker Compose:

```bash
docker compose up --build
```

## 🧪 Running Tests

Execute the automated test suite using `pytest`:

```bash
pytest -v
```

## 📌 API Endpoints Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Application health check |
| `POST` | `/documents/upload` | Upload a PDF document and build FAISS index |
| `GET` | `/documents/` | List all indexed documents |
| `DELETE` | `/documents/{document_id}` | Delete a document and its FAISS index |
| `POST` | `/query/ask` | Ask a question against an indexed document |

---

<a name="türkçe"></a>
# Türkçe

**FastAPI**, **FAISS**, **SentenceTransformers** ve **OpenAI GPT-4o-mini** kullanılarak geliştirilmiş, canlı ortama hazır **Retrieval-Augmented Generation (RAG)** tabanlı doküman soru-cevap API'si.

Bu sistem, kullanıcıların PDF dokümanlarını yüklemesine, içeriklerini yoğun vektör gömmeleri (dense embeddings) ile indekslemesine ve kaynak atıfları (sayfa numaraları, benzerlik puanı ve orijinal dosya adı) içeren kesin, bağlama duyarlı yanıtlar almasına olanak tanır.

## ✨ Öne Çıkan Özellikler

- **PDF İşleme & Parçalama:** `PyMuPDF` ile metin çıkarma ve kayan pencere (sliding-window) metoduyla chunking.
- **Yerel Vektör Gömme (Embeddings):** Dış API maliyeti olmadan `SentenceTransformers` (`all-MiniLM-L6-v2`) ile yerel vektör üretimi.
- **FAISS Vektör İndeksleme:** Kalıcı `.faiss` indeksleri ve JSON metadata depolaması ile hızlı benzerlik araması.
- **UUID Tabanlı Depolama:** Özel/Türkçe karakter içeren dosya adlarını destekleyen güvenli ve çakışmasız dosya depolama altyapısı.
- **Yanlış Bilgi (Hallucination) Önleyici RAG Prompting:** OpenAI `gpt-4o-mini` modeli yalnızca getirilen bağlama dayalı olarak yanıt verir.
- **Kaynak Atıfları (Sources Metadata):** API JSON yanıtları; sayfa numaraları, benzerlik puanları (scores) ve orijinal dosya adlarını içeren detaylı bir `sources` dizisi sunar.
- **Doküman Yönetimi:** Dokümanları listeleme (`GET /documents`) ve silme (`DELETE /documents/{id}`) için tam CRUD desteği.
- **Otomatik Testler:** `pytest` ve `httpx` kullanılarak yazılmış birim ve endpoint test kapsamı.

## 🏗️ Proje Mimarisi

```
document-qa-api/
├── app/
│   ├── main.py                  # FastAPI uygulama giriş noktası
│   ├── api/
│   │   └── routes/
│   │       ├── documents.py     # Yükleme, Listeleme ve Silme endpoint'leri
│   │       └── query.py         # RAG soru sorma endpoint'i
│   ├── core/
│   │   └── config.py            # Ortam değişkenleri konfigürasyonu
│   ├── models/
│   │   └── schemas.py           # Pydantic şemaları (AskRequest vb.)
│   ├── services/
│   │   ├── pdf_service.py       # PyMuPDF metin çıkarma servisi
│   │   ├── chunking_service.py  # Metin parçalama servisi
│   │   ├── embedding_service.py # SentenceTransformer servisi
│   │   ├── vector_service.py    # FAISS CRUD işlemleri
│   │   ├── retrieval_service.py # Benzerlik araması servisi
│   │   └── llm_service.py       # RAG prompt mühendisliği & OpenAI istemcisi
│   └── storage/                 # Yerel dosya depolama alanı (Git ignored)
│       ├── uploads/
│       ├── faiss_index/
│       └── metadata/
├── tests/                       # Pytest test paketi
│   ├── test_health.py
│   ├── test_documents.py
│   └── test_query.py
├── .env                         # API anahtarları (Git'e eklenmez)
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚀 Hızlı Başlangıç

### 1. Ön gereksinimler
- Python 3.11+
- Conda (Tavsiye edilen)

### 2. Ortam Kurulumu

Depoyu klonlayın ve Conda ortamını oluşturun:

```bash
conda create -n document-qa python=3.11 -y
conda activate document-qa
pip install -r requirements.txt
```

### 3. Ortam Değişkenleri

Proje kök dizininde bir `.env` dosyası oluşturun:

```env
OPENAI_API_KEY=openai_api_anahtariniz_buraya
```

## 🏃 Uygulamayı Çalıştırma

Uvicorn ile FastAPI geliştirme sunucusunu başlatın:

```bash
uvicorn app.main:app --reload
```

API `http://127.0.0.1:8000` adresinde çalışacaktır.

- **İnteraktif API Dokümantasyonu (Swagger UI):** `http://127.0.0.1:8000/docs`
- **ReDoc Dokümantasyonu:** `http://127.0.0.1:8000/redoc`

### 🐋 Docker ile Çalıştırma (Alternatif)

Docker Compose kullanarak uygulamayı derleyin ve çalıştırın:

```bash
docker compose up --build
```

## 🧪 Testleri Çalıştırma

Otomatik test paketini `pytest` ile çalıştırın:

```bash
pytest -v
```

## 📌 API Endpoint Özet Tablosu

| Metot | Endpoint | Açıklama |
|---|---|---|
| `GET` | `/health` | Uygulama sağlık kontrolü |
| `POST` | `/documents/upload` | PDF dokümanı yükler ve FAISS indeksini oluşturur |
| `GET` | `/documents/` | İndekslenmiş tüm dokümanları listeler |
| `DELETE` | `/documents/{document_id}` | Dokümanı ve ilişkili FAISS indeksini siler |
| `POST` | `/query/ask` | İndekslenmiş dokümana soru sorar |
