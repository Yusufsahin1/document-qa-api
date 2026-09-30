import json
import os
from app.services.embedding_service import generate_query_embedding
from app.services.vector_service import load_index, search_vectors


def search_similar_chunks(question: str, document_id: str, top_k: int = 3) -> list[dict]:
    """
    Searches FAISS and JSON metadata to retrieve the top_k most relevant chunks for a question.
    """

    index_path = f"app/storage/faiss_index/{document_id}.faiss"
    metadata_path = f"app/storage/metadata/{document_id}.json"

    if not os.path.exists(index_path):
        raise ValueError("Index file not found")
    if not os.path.exists(metadata_path):
        raise ValueError("Metadata file not found")

    query_vector = generate_query_embedding(question)

    index = load_index(index_path)

    distances, indices = search_vectors(index, query_vector, top_k)

    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    results = []
    for i, idx in enumerate(indices):
        if 0 <= idx < len(metadata):
            chunk_data = metadata[idx].copy()
            chunk_data["score"] = distances[i]
            results.append(chunk_data)

    return results