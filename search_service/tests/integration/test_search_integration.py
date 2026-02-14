import asyncio

import pytest
import httpx

pytestmark = pytest.mark.integration

CORE_URL = "http://localhost:8000"
SEARCH_URL = "http://localhost:8001"


async def test_root():
    async with httpx.AsyncClient(base_url=SEARCH_URL) as client:
        resp = await client.get("/")
    assert resp.status_code == 200


async def test_reindex_and_search():
    async with httpx.AsyncClient(base_url=CORE_URL) as core:
        author = (
            await core.post("/authors/", json={"name": "Search Test Author"})
        ).json()
        await core.post(
            "/books/",
            json={
                "title": "Searchable Book",
                "description": "A very unique description",
                "author_ids": [author["_id"]],
            },
        )

    async with httpx.AsyncClient(base_url=SEARCH_URL) as search:
        resp = await search.post("/reindex/")
        assert resp.status_code == 200

        # Give ES a moment to index
        await asyncio.sleep(1)

        resp = await search.get("/search/", params={"query": "Searchable"})
        assert resp.status_code == 200
        results = resp.json()
        assert any("Searchable" in r.get("title", "") for r in results)


async def test_search_all_indices():
    async with httpx.AsyncClient(base_url=SEARCH_URL) as search:
        await search.post("/reindex/")
        await asyncio.sleep(1)

        resp = await search.get("/search/all/", params={"query": "Search Test"})
        assert resp.status_code == 200
        data = resp.json()
        assert "books" in data
        assert "authors" in data
