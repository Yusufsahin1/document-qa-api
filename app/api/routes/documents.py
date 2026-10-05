from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunking_service import chunk_pages
from app.services.embedding_service import generate_embeddings
from app.services.vector_service import create_index, add_vectors, save_index
import json
from pathlib import Path
from uuid import uuid4


router = APIRouter()

@router.post("/upload", tags=["Document Upload"])
async def upload_document(file: UploadFile = File(...)):

    content = await file.read()

    document_id = str(uuid4())
    original_filename = file.filename

    save_path = f"app/storage/uploads/{document_id}"
    with open(save_path, "wb") as f:
        f.write(content)

    pages = extract_text_from_pdf(save_path)

    chunks = chunk_pages(pages, document_id=document_id)

    for chunk in chunks:
        chunk["original_filename"] = original_filename

    chunk_texts = [chunk["text"] for chunk in chunks]
    embeddings = generate_embeddings(chunk_texts)

    index = create_index(dimension=len(embeddings[0]))
    add_vectors(index, embeddings)
    index_path = f"app/storage/faiss_index/{document_id}.faiss"
    save_index(index, index_path)
    metadata_path = f"app/storage/metadata/{document_id}.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    return {
        "document_id": document_id,
        "filename": original_filename,
        "page_count": len(pages),
        "preview": pages[0]["text"][:200],
        "chunk_count": len(chunks),
        "first_chunk": chunks[0],
        "embedding_count": len(embeddings),
        "embedding_dim": len(embeddings[0]) if embeddings else 0,
        "index_saved": True,
        "metadata_saved": True
        }


METADATA_DIR = Path("app/storage/metadata")

@router.get("/", tags=["Documents"])
async def list_documents():
    documents = []
    
    for json_file in METADATA_DIR.glob("*.json"):
        document_id = json_file.stem
        
        with open(json_file, "r", encoding="utf-8") as f:
            chunks = json.load(f)
        
        original_filename = chunks[0].get("original_filename", document_id) if chunks else document_id
        
        documents.append({
            "document_id": document_id,
            "filename": original_filename
        })
    return {"documents": documents}


UPLOAD_DIR = Path("app/storage/uploads")
FAISS_DIR = Path("app/storage/faiss_index")

@router.delete("/{document_id}", tags=["Documents"])
async def delete_document(document_id: str):
    pdf_path   = UPLOAD_DIR / document_id
    faiss_path = FAISS_DIR  / f"{document_id}.faiss"
    meta_path  = METADATA_DIR / f"{document_id}.json"

    if not any([pdf_path.exists(), faiss_path.exists(), meta_path.exists()]):
        raise HTTPException(status_code=404, detail="Document not found")

    if pdf_path.exists():
        pdf_path.unlink()
    if faiss_path.exists():
        faiss_path.unlink()
    if meta_path.exists():
        meta_path.unlink()

    return {"message": f"Document '{document_id}' deleted successfully"}