import asyncio
from unittest.mock import AsyncMock, MagicMock, patch


async def test_consume_book_created_event():
    mock_es = AsyncMock()

    msg = MagicMock()
    msg.value = {
        "event": "book_created",
        "data": {
            "_id": "book123",
            "title": "Test Book",
            "description": "Desc",
            "author_ids": [],
        },
    }

    mock_consumer = MagicMock()
    mock_consumer.start = AsyncMock()
    mock_consumer.stop = AsyncMock()

    async def mock_aiter(self):
        yield msg

    mock_consumer.__aiter__ = mock_aiter

    with (
        patch("app.kafka_consumer.AIOKafkaConsumer", return_value=mock_consumer),
        patch("app.kafka_consumer.es_client", mock_es),
    ):
        from app.kafka_consumer import consume_events

        task = asyncio.create_task(consume_events())
        await asyncio.sleep(0.05)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    mock_es.index.assert_called_once_with(
        index="books",
        id="book123",
        document={"title": "Test Book", "description": "Desc", "author_ids": []},
    )


async def test_consume_author_created_event():
    mock_es = AsyncMock()

    msg = MagicMock()
    msg.value = {
        "event": "author_created",
        "data": {"_id": "author123", "name": "Test Author", "book_ids": []},
    }

    mock_consumer = MagicMock()
    mock_consumer.start = AsyncMock()
    mock_consumer.stop = AsyncMock()

    async def mock_aiter(self):
        yield msg

    mock_consumer.__aiter__ = mock_aiter

    with (
        patch("app.kafka_consumer.AIOKafkaConsumer", return_value=mock_consumer),
        patch("app.kafka_consumer.es_client", mock_es),
    ):
        from app.kafka_consumer import consume_events

        task = asyncio.create_task(consume_events())
        await asyncio.sleep(0.05)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    mock_es.index.assert_called_once_with(
        index="authors",
        id="author123",
        document={"name": "Test Author", "book_ids": []},
    )


async def test_consume_unknown_event_ignores():
    mock_es = AsyncMock()

    msg = MagicMock()
    msg.value = {"event": "unknown_event", "data": {"foo": "bar"}}

    mock_consumer = MagicMock()
    mock_consumer.start = AsyncMock()
    mock_consumer.stop = AsyncMock()

    async def mock_aiter(self):
        yield msg

    mock_consumer.__aiter__ = mock_aiter

    with (
        patch("app.kafka_consumer.AIOKafkaConsumer", return_value=mock_consumer),
        patch("app.kafka_consumer.es_client", mock_es),
    ):
        from app.kafka_consumer import consume_events

        task = asyncio.create_task(consume_events())
        await asyncio.sleep(0.05)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    mock_es.index.assert_not_called()
