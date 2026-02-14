from unittest.mock import AsyncMock, patch

from app.kafka_producer import send_event


async def test_send_event_with_producer():
    mock_producer = AsyncMock()
    with patch("app.kafka_producer.producer", mock_producer):
        await send_event("library.events", "book_created", {"title": "Test"})

    mock_producer.send_and_wait.assert_called_once_with(
        "library.events",
        {"event": "book_created", "data": {"title": "Test"}},
    )


async def test_send_event_without_producer():
    with patch("app.kafka_producer.producer", None):
        # Should not raise
        await send_event("library.events", "book_created", {"title": "Test"})
