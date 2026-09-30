from fastapi import APIRouter, HTTPException
from app.models.schemas import AskRequest
from app.services.retrieval_service import search_similar_chunks
from app.services.llm_service import generate_answer

router = APIRouter()

@router.post("/ask", tags=["Query"])
async def ask_question(request: AskRequest):
    try:
        relevant_chunks = search_similar_chunks(
            question=request.question,
            document_id=request.document_id,
            top_k=5
        )
        answer = generate_answer(request.question, relevant_chunks)
        return {
            "question": request.question,
            "document_id": request.document_id,
            "answer": answer,
            "sources": relevant_chunks
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")