from elasticsearch import AsyncElasticsearch
from app.config import settings

es_client = AsyncElasticsearch(settings.ELASTIC_URL) # Берем из настроек