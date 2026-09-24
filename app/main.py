from fastapi import FastAPI
from app.models.schemas import HealthResponse, AskRequest
from app.api.routes.documents import router as documents_router

app = FastAPI(title="Document Q&A Application",
              version="1.0.0",
              description="A simple application for document-based question answering using FastAPI.")

app.include_router(documents_router, prefix="/documents")

@app.get("/health", tags=["Health Check"], response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok", message="Document QA API is running")