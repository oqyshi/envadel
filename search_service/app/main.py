import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import es_client
from app.kafka_consumer import consume_events

from elasticsearch import NotFoundError
from fastapi.middleware.cors import CORSMiddleware

# Глобальная переменная для нашей фоновой задачи
consumer_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global consumer_task
    print("🚀 Запуск Search Service...")
    
    # Запускаем консьюмер в фоне
    consumer_task = asyncio.create_task(consume_events())
    
    yield
    
    print("🛑 Остановка Search Service...")
    consumer_task.cancel()        # Отменяем задачу
    await es_client.close()       # Закрываем соединение с Эластиком

app = FastAPI(
    title="Search Service", 
    description="Сервис полнотекстового поиска",
    lifespan=lifespan # <-- Вот эту строчку мы забыли!
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем запросы с любого адреса (включая и localhost, и 127.0.0.1)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST, OPTIONS и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

@app.get("/")
async def root():
    return {"message": "Search Service готов искать!"}




@app.get("/search/")
async def search(query: str, index: str = "books"):
    """
    Полнотекстовый поиск по Эластику.
    index может быть 'books' или 'authors'.
    """
    es_query = {
        "bool": {
            "should": [
                {
                    "multi_match": {
                        "query": query,
                        "fields": ["title", "description", "name"],
                        "fuzziness": "AUTO"
                    }
                },
                {
                    "query_string": {
                        "query": f"*{query}*",
                        "fields": ["title", "description", "name"]
                    }
                }
            ],
            "minimum_should_match": 1
        }
    }

    try:
        response = await es_client.search(index=index, query=es_query)
        documents = [hit["_source"] for hit in response["hits"]["hits"]]
        return documents
    
    except NotFoundError:
        # Если индекса еще нет (ни одной книги не добавлено), 
        # просто возвращаем пустой список, а не роняем сервер!
        return []