from fastapi import APIRouter, UploadFile, File
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunking_service import chunk_pages
from app.services.embedding_service import generate_embeddings

router = APIRouter()

@router.post("/upload", tags=["Document Upload"])
async def upload_document(file: UploadFile = File(...)):

    content = await file.read()

    save_path = f"app/storage/uploads/{file.filename}"
    with open(save_path, "wb") as f:
        f.write(content)

    pages = extract_text_from_pdf(save_path)

    chunks = chunk_pages(pages, document_id=file.filename)

    chunk_texts = [chunk["text"] for chunk in chunks]
    embeddings = generate_embeddings(chunk_texts)



    return {"filename": file.filename, "page_count": len(pages), "preview": pages[0]["text"][:200],
             "chunk_count": len(chunks), "first_chunk": chunks[0],
             "embedding_count": len(embeddings), "embedding_dim": len(embeddings[0]) if embeddings else 0}

