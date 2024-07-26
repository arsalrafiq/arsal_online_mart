from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=Secret)
SECRET_KEY = config("SECRET_KEY", cast=Secret)
BOOTSTRAP_SERVER = config("BOOTSTRAP_SERVER", cast=Secret)
STRIPE_API_KEY = config("STRIPE_API_KEY", cast=Secret)