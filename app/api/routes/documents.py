from fastapi import APIRouter, UploadFile, File
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunking_service import chunk_pages
from app.services.embedding_service import generate_embeddings
from app.services.vector_service import create_index, add_vectors, save_index
import json

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

    index = create_index(dimension=len(embeddings[0]))
    add_vectors(index, embeddings)
    index_path = f"app/storage/faiss_index/{file.filename}.faiss"
    save_index(index, index_path)
    metadata_path = f"app/storage/metadata/{file.filename}.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    return {"filename": file.filename, "page_count": len(pages), "preview": pages[0]["text"][:200],
             "chunk_count": len(chunks), "first_chunk": chunks[0],
             "embedding_count": len(embeddings), "embedding_dim": len(embeddings[0]) if embeddings else 0,
             "index_saved": True, "metadata_saved": True}