from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from app.models import AuthorBase, AuthorDB, BookBase, BookDB
from app.database import authors_collection, books_collection
from app.kafka_producer import send_event

router = APIRouter(tags=["Library"])

# ==========================================
# ✍️ АВТОРЫ
# ==========================================

@router.post("/authors/", response_model=AuthorDB, status_code=status.HTTP_201_CREATED)
async def create_author(author: AuthorBase):
    author_dict = author.model_dump()
    new_author = await authors_collection.insert_one(author_dict)
    created_author = await authors_collection.find_one({"_id": new_author.inserted_id})
    
    # Подготавливаем данные для Кафки (превращаем ObjectId в строку)
    event_data = {**created_author, "_id": str(created_author["_id"])}
    
    # Отправляем событие в топик 'library.events'
    await send_event(topic="library.events", event_type="author_created", data=event_data)
    
    return created_author
@router.get("/authors/", response_model=List[AuthorDB])
async def get_authors():
    # Достаем всех авторов (для пет-проекта пока без пагинации)
    authors = await authors_collection.find().to_list(100)
    return authors


# ==========================================
# 📖 КНИГИ (Здесь магия связи Многие-ко-многим)
# ==========================================

@router.post("/books/", response_model=BookDB, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookBase):
    book_dict = book.model_dump()
    new_book = await books_collection.insert_one(book_dict)
    created_book = await books_collection.find_one({"_id": new_book.inserted_id})
    
    if book.author_ids:
        author_object_ids = [ObjectId(aid) for aid in book.author_ids]
        await authors_collection.update_many(
            {"_id": {"$in": author_object_ids}},
            {"$addToSet": {"book_ids": str(new_book.inserted_id)}} 
        )
        
    # Подготавливаем данные для Кафки
    event_data = {**created_book, "_id": str(created_book["_id"])}
    
    # Отправляем событие
    await send_event(topic="library.events", event_type="book_created", data=event_data)
        
    return created_book

@router.get("/books/", response_model=List[BookDB])
async def get_books():
    books = await books_collection.find().to_list(100)
    return books