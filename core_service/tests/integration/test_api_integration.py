import pytest
import httpx

pytestmark = pytest.mark.integration

CORE_URL = "http://localhost:8000"


async def test_root():
    async with httpx.AsyncClient(base_url=CORE_URL) as client:
        resp = await client.get("/")
    assert resp.status_code == 200


async def test_author_crud():
    async with httpx.AsyncClient(base_url=CORE_URL) as client:
        resp = await client.post(
            "/authors/", json={"name": "Integration Author", "book_ids": []}
        )
        assert resp.status_code == 201
        author_id = resp.json()["_id"]

        resp = await client.get("/authors/")
        assert resp.status_code == 200
        assert any(a["_id"] == author_id for a in resp.json())


async def test_book_crud_with_many_to_many():
    async with httpx.AsyncClient(base_url=CORE_URL) as client:
        # Create two authors
        a1 = (await client.post("/authors/", json={"name": "Author A"})).json()
        a2 = (await client.post("/authors/", json={"name": "Author B"})).json()

        # Create book linked to both
        book = (
            await client.post(
                "/books/",
                json={
                    "title": "Multi-author Book",
                    "description": "Test",
                    "author_ids": [a1["_id"], a2["_id"]],
                },
            )
        ).json()
        book_id = book["_id"]

        # Verify authors have the book_id
        authors = (await client.get("/authors/")).json()
        authors_map = {a["_id"]: a for a in authors}
        assert book_id in authors_map[a1["_id"]]["book_ids"]
        assert book_id in authors_map[a2["_id"]]["book_ids"]


async def test_book_with_no_authors():
    async with httpx.AsyncClient(base_url=CORE_URL) as client:
        resp = await client.post(
            "/books/",
            json={"title": "Orphan Book", "description": "No authors", "author_ids": []},
        )
        assert resp.status_code == 201
        assert resp.json()["author_ids"] == []
