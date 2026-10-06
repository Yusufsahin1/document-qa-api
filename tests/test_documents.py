from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_documents_returns_200():
    response = client.get("/documents")
    assert response.status_code == 200


def test_list_documents_returns_list():
    response = client.get("/documents")
    data = response.json()
    assert "documents" in data
    assert isinstance(data["documents"], list)


def test_delete_non_existent_document_returns_404():
    response = client.delete("/documents/non-existent-doc-12345")
    assert response.status_code == 404