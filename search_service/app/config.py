from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ELASTIC_URL: str = "http://localhost:9200"
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
