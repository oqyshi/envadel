from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Если переменной нет в окружении, берем значение по умолчанию (для локалхоста)
    MONGO_URL: str = "mongodb://localhost:27017"
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"

    # Говорим Pydantic, что можно читать из файла .env (если он есть)
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Создаем глобальный объект настроек
settings = Settings()
