from elasticsearch import NotFoundError


async def test_root(client):
    resp = await client.get("/")
    assert resp.status_code == 200
    assert "message" in resp.json()


async def test_search_returns_results(client, mock_es_client):
    mock_es_client.search.return_value = {
        "hits": {
            "hits": [
                {"_source": {"title": "War and Peace", "description": "A novel"}},
                {"_source": {"title": "Anna Karenina", "description": "Another novel"}},
            ]
        }
    }

    resp = await client.get("/search/", params={"query": "war", "index": "books"})
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) == 2
    assert results[0]["title"] == "War and Peace"


async def test_search_default_index_is_books(client, mock_es_client):
    mock_es_client.search.return_value = {"hits": {"hits": []}}

    await client.get("/search/", params={"query": "test"})
    call_kwargs = mock_es_client.search.call_args.kwargs
    assert call_kwargs["index"] == "books"


async def test_search_not_found_returns_empty(client, mock_es_client):
    mock_es_client.search.side_effect = NotFoundError(404, "index_not_found_exception", body={})

    resp = await client.get("/search/", params={"query": "test"})
    assert resp.status_code == 200
    assert resp.json() == []


async def test_search_all_returns_both_indices(client, mock_es_client):
    mock_es_client.search.side_effect = [
        {"hits": {"hits": [{"_source": {"title": "Book 1"}}]}},
        {"hits": {"hits": [{"_source": {"name": "Author 1"}}]}},
    ]

    resp = await client.get("/search/all/", params={"query": "test"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["books"]) == 1
    assert len(data["authors"]) == 1
    assert mock_es_client.search.call_count == 2


async def test_search_all_handles_missing_index(client, mock_es_client):
    mock_es_client.search.side_effect = [
        NotFoundError(404, "index_not_found_exception", body={}),
        {"hits": {"hits": [{"_source": {"name": "Author 1"}}]}},
    ]

    resp = await client.get("/search/all/", params={"query": "test"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["books"] == []
    assert len(data["authors"]) == 1
