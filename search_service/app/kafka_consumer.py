import json

from aiokafka import AIOKafkaConsumer

from app.config import settings
from app.database import es_client


async def consume_events():
    consumer = AIOKafkaConsumer(
        "library.events",
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,  # Берем из настроек
        group_id="search_group",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    await consumer.start()
    try:
        print("🎧 Консьюмер запущен, слушаем топик 'library.events'...")
        # Бесконечный цикл чтения сообщений
        async for msg in consumer:
            event = msg.value
            event_type = event.get("event")
            data = event.get("data")

            print(f"📥 Получено событие: {event_type}")

            # Индексируем данные в Elasticsearch
            if event_type in ["book_created", "author_created"]:
                # Определяем индекс (таблицу) в Эластике
                index_name = "books" if "book" in event_type else "authors"

                # Забираем _id из словаря, чтобы использовать его как ID документа в Эластике
                doc_id = data.pop("_id", None)

                # Сохраняем документ
                await es_client.index(index=index_name, id=doc_id, document=data)
                print(f"✅ Документ {doc_id} сохранен в индекс {index_name}!")

    finally:
        # Корректно завершаем работу, если приложение останавливается
        await consumer.stop()
