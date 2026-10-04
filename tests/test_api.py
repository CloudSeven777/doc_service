import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.mark.asyncio
async def test_openapi():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        response = await client.get("/openapi.json")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_search_documents():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        response = await client.get(
            "/documents/search",
            params={"q": "Россия"}
        )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_document():
    transport = ASGITransport(app=app)

    document = {
        "id": 99999,
        "rubrics": ["test"],
        "text": "Test document for API",
        "created_date": "2026-10-04"
    }

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        await client.delete("/documents/99999")

        response = await client.post(
            "/documents",
            json=document
        )

        assert response.status_code == 200

        delete_response = await client.delete(
            "/documents/99999"
        )

        assert delete_response.status_code == 200
        assert (
            delete_response.json()["message"]
            == "Document deleted successfully"
        )