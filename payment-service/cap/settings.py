from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

DATABASE_URL = config("DATABASE_URL", cast=Secret)
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", cast=Secret)
STRIPE_PUBLISHABLE_KEY= config("STRIPE_PUBLISHABLE_KEY", cast=Secret)
STRIPE_CLIENT_ID = config("STRIPE_CLIENT_ID", cast=Secret)
STRIPE_OAUTH_REDIRECT = config("STRIPE_OAUTH_REDIRECT", cast=Secret)


