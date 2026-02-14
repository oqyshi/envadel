import asyncio
from contextlib import asynccontextmanager

import httpx
from elasticsearch import NotFoundError
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import es_client
from app.kafka_consumer import consume_events

consumer_task = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global consumer_task
    print("Starting Search Service...")

    consumer_task = asyncio.create_task(consume_events())

    yield

    print("Stopping Search Service...")
    consumer_task.cancel()
    await es_client.close()


app = FastAPI(
    title="Search Service",
    description="Full-text search service",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Search Service is ready!"}


@app.get("/search/")
async def search(query: str, index: str = "books"):
    es_query = {
        "bool": {
            "should": [
                {
                    "multi_match": {
                        "query": query,
                        "fields": ["title", "description", "name"],
                        "fuzziness": "AUTO",
                    }
                },
                {
                    "query_string": {
                        "query": f"*{query}*",
                        "fields": ["title", "description", "name"],
                    }
                },
            ],
            "minimum_should_match": 1,
        }
    }

    try:
        response = await es_client.search(index=index, query=es_query)
        documents = [hit["_source"] for hit in response["hits"]["hits"]]
        return documents
    except NotFoundError:
        return []


@app.get("/search/all/")
async def search_all(query: str):
    es_query = {
        "bool": {
            "should": [
                {
                    "multi_match": {
                        "query": query,
                        "fields": ["title", "description", "name"],
                        "fuzziness": "AUTO",
                    }
                },
                {
                    "query_string": {
                        "query": f"*{query}*",
                        "fields": ["title", "description", "name"],
                    }
                },
            ],
            "minimum_should_match": 1,
        }
    }

    results = {"books": [], "authors": []}

    for index in ("books", "authors"):
        try:
            response = await es_client.search(index=index, query=es_query)
            results[index] = [hit["_source"] for hit in response["hits"]["hits"]]
        except NotFoundError:
            pass

    return results


@app.post("/reindex/")
async def reindex():
    """Fetch all books and authors from Core Service and index them into Elasticsearch."""
    indexed = {"books": 0, "authors": 0}

    async with httpx.AsyncClient() as client:
        # Reindex books
        resp = await client.get(f"{settings.CORE_API_URL}/books/")
        if resp.status_code == 200:
            for book in resp.json():
                doc_id = book.pop("_id", None) or book.pop("id", None)
                await es_client.index(index="books", id=doc_id, document=book)
                indexed["books"] += 1

        # Reindex authors
        resp = await client.get(f"{settings.CORE_API_URL}/authors/")
        if resp.status_code == 200:
            for author in resp.json():
                doc_id = author.pop("_id", None) or author.pop("id", None)
                await es_client.index(index="authors", id=doc_id, document=author)
                indexed["authors"] += 1

    return {"message": "Reindex complete", "indexed": indexed}
