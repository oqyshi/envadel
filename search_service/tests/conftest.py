from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.fixture
def mock_es_client():
    mock = MagicMock()
    mock.search = AsyncMock()
    mock.index = AsyncMock()
    mock.close = AsyncMock()
    return mock


@pytest.fixture
async def client(mock_es_client):
    with (
        patch("app.database.es_client", mock_es_client),
        patch("app.main.es_client", mock_es_client),
        patch("app.main.consume_events", new_callable=AsyncMock),
    ):
        from app.main import app

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            yield ac
