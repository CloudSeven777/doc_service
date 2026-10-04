from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_openapi():
    response = client.get("/openapi.json")

    assert response.status_code == 200

def test_search_documents():
    response = client.get("/documents/search?q=Россия")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_document():
    client.delete("/documents/99999")
    document = {
        "id": 99999,
        "rubrics": ["test"],
        "text": "Test document for API",
        "created_date": "2026-10-04"
    }

    response = client.post("/documents", json=document)

    assert response.status_code == 200

    delete_response = client.delete("/documents/99999")

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Document deleted successfully"


