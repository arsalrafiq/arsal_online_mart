# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Payment Service"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str
    STRIPE_SECRET_KEY: str
    KAFKA_BOOTSTRAP_SERVERS: str

    class Config:
        env_file = ".env"

settings = Settings()