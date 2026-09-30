from fastapi import APIRouter, HTTPException
from app.models.schemas import AskRequest
from app.services.retrieval_service import search_similar_chunks

router = APIRouter()

@router.post("/ask", tags=["Query"])
async def ask_question(request: AskRequest):
    try:
        relevant_chunks = search_similar_chunks(
            question=request.question,
            document_id=request.document_id,
            top_k=3
        )
        return {
            "question": request.question,
            "document_id": request.document_id,
            "relevant_chunks": relevant_chunks
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))