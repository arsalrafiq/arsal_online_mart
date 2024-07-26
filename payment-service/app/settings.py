from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    STRIPE_SECRET_KEY: str
    KAFKA_BOOTSTRAP_SERVERS: str

    class Config:
        env_file = ".env"

settings = Settings()
