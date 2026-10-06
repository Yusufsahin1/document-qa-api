from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_ask_non_existent_document_returns_404():
    payload = {
        "question": "What is this document about?",
        "document_id": "non-existent-doc-12345"
    }
    response = client.post("/query/ask", json=payload)
    assert response.status_code == 404