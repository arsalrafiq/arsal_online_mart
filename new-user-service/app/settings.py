from starlette.config import Config
from datetime import timedelta

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

# Database configuration
DATABASE_URL = config("DATABASE_URL")


# JWT settings
ALGORITHM = config.get("ALGORITHM")
SECRET_KEY = config.get("SECRET_KEY")

ACCESS_TOKEN_EXPIRE_TIME = timedelta(
    days=int(config.get("ACCESS_TOKEN_EXPIRE_TIME")))

ADMIN_SECRET_KEY = config.get("ADMIN_SECRET_KEY")

ADMIN_EXPIRE_TIME = timedelta(minutes=int(
    config.get("ACCESS_TOKEN_EXPIRE_TIME")))


# Kong url
KONG_ADMIN_URL = config.get("KONG_ADMIN_URL")

# topics for produce and consume messages
NOTIFICATION_TOPIC = config.get("NOTIFICATION_TOPIC")

# from starlette.config import Config
# from datetime import timedelta

# try:
#     config = Config(".env")
# except FileNotFoundError:
#     config = Config()

# # Database configuration
# DATABASE_URL = config("DATABASE_URL")

# # JWT settings
# ALGORITHM = config("ALGORITHM")
# SECRET_KEY = config("SECRET_KEY")
# ACCESS_TOKEN_EXPIRE_TIME = timedelta(days=int(config.get("ACCESS_TOKEN_EXPIRE_TIME", 30)))

# # Admin JWT credentials
# ADMIN_SECRET_KEY = config.get("ADMIN_SECRET_KEY")
# ADMIN_EXPIRE_TIME = timedelta(minutes=int(config.get("ADMIN_EXPIRY_TIME", 60)))

# # Kong URL
# KONG_ADMIN_URL = config.get("KONG_ADMIN_URL")

# # Topics for producing and consuming messages
# NOTIFICATION_TOPIC = config.get("NOTIFICATION_TOPIC")
# USER_TOPIC = config.get("USER_TOPIC")
# KONG_TOPIC = config.get("KONG_TOPIC")
