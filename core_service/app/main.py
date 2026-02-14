import json
from fastapi import FastAPI
from contextlib import asynccontextmanager
from aiokafka import AIOKafkaProducer

from app.database import client
from app.routers import router as library_router
import app.kafka_producer as kafka_module  # Импортируем наш модуль
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Приложение запускается. MongoDB подключена.")
    
    # Инициализируем и запускаем Kafka Producer
    print("🚀 Подключение к Kafka...")
    kafka_module.producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS, # Забираем из настроек
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await kafka_module.producer.start()
    
    yield
    
    # Корректно всё тушим при остановке сервера
    print("🛑 Отключение от Kafka...")
    await kafka_module.producer.stop()
    print("🛑 Закрытие соединения с MongoDB...")
    client.close()

app = FastAPI(
    title="Library Core Service",
    description="Управляет книгами и авторами, отправляет события в Kafka",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(library_router)

@app.get("/")
async def root():
    return {"message": "Core Service работает!"}