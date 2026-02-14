from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings  # Импортируем настройки

client = AsyncIOMotorClient(settings.MONGO_URL)
db = client.library_database

# Определяем коллекции
books_collection = db.get_collection("books")
authors_collection = db.get_collection("authors")
