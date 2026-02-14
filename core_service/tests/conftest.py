from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.fixture
def mock_books_collection():
    col = MagicMock()
    col.insert_one = AsyncMock()
    col.find_one = AsyncMock()
    cursor = MagicMock()
    cursor.to_list = AsyncMock(return_value=[])
    col.find = MagicMock(return_value=cursor)
    col.update_many = AsyncMock()
    return col


@pytest.fixture
def mock_authors_collection():
    col = MagicMock()
    col.insert_one = AsyncMock()
    col.find_one = AsyncMock()
    cursor = MagicMock()
    cursor.to_list = AsyncMock(return_value=[])
    col.find = MagicMock(return_value=cursor)
    col.update_many = AsyncMock()
    return col


@pytest.fixture
def mock_kafka_producer():
    producer = MagicMock()
    producer.send_and_wait = AsyncMock()
    return producer


@pytest.fixture
async def client(mock_books_collection, mock_authors_collection, mock_kafka_producer):
    with (
        patch("app.routers.books_collection", mock_books_collection),
        patch("app.routers.authors_collection", mock_authors_collection),
        patch("app.kafka_producer.producer", mock_kafka_producer),
        patch("app.routers.send_event", new_callable=AsyncMock) as mock_send,
    ):
        from app.main import app

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            ac.mock_send_event = mock_send
            yield ac
