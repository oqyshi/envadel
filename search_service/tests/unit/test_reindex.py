from unittest.mock import AsyncMock, MagicMock, patch


async def test_reindex_indexes_books_and_authors(client, mock_es_client):
    books_resp = MagicMock()
    books_resp.status_code = 200
    books_resp.json.return_value = [
        {"_id": "b1", "title": "Book 1", "description": "D1", "author_ids": []},
        {"_id": "b2", "title": "Book 2", "description": "D2", "author_ids": []},
    ]

    authors_resp = MagicMock()
    authors_resp.status_code = 200
    authors_resp.json.return_value = [
        {"_id": "a1", "name": "Author 1", "book_ids": []},
    ]

    mock_http = AsyncMock()
    mock_http.get = AsyncMock(side_effect=[books_resp, authors_resp])

    with patch("httpx.AsyncClient") as mock_cls:
        mock_cls.return_value.__aenter__ = AsyncMock(return_value=mock_http)
        mock_cls.return_value.__aexit__ = AsyncMock()

        resp = await client.post("/reindex/")

    assert resp.status_code == 200
    data = resp.json()
    assert data["indexed"]["books"] == 2
    assert data["indexed"]["authors"] == 1
    assert mock_es_client.index.call_count == 3


async def test_reindex_handles_core_service_error(client, mock_es_client):
    error_resp = MagicMock()
    error_resp.status_code = 500

    mock_http = AsyncMock()
    mock_http.get = AsyncMock(return_value=error_resp)

    with patch("httpx.AsyncClient") as mock_cls:
        mock_cls.return_value.__aenter__ = AsyncMock(return_value=mock_http)
        mock_cls.return_value.__aexit__ = AsyncMock()

        resp = await client.post("/reindex/")

    assert resp.status_code == 200
    data = resp.json()
    assert data["indexed"]["books"] == 0
    assert data["indexed"]["authors"] == 0
    mock_es_client.index.assert_not_called()
