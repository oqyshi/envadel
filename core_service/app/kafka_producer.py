import json
from aiokafka import AIOKafkaProducer

# Глобальная переменная для хранения нашего продюсера
producer: AIOKafkaProducer = None

async def send_event(topic: str, event_type: str, data: dict):
    """
    Отправляет сообщение в указанный топик Kafka.
    """
    global producer
    if producer:
        # Формируем структуру сообщения (Event)
        message = {
            "event": event_type,
            "data": data
        }
        # Отправляем сообщение
        await producer.send_and_wait(topic, message)
        print(f"✅ Событие {event_type} отправлено в топик {topic}!")