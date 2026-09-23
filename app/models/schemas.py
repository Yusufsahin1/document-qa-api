from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    message: str

class AskRequest(BaseModel):
    question: str
    document_id: str