from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=Secret)
KAFKA_BOOTSTRAP_SERVERS= config("KAFKA_BOOTSTRAP_SERVERS", cast=Secret)
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", cast=Secret)
PROJECT_NAME: str = "Payment Service"
API_V1_STR: str = "/api/v1"
