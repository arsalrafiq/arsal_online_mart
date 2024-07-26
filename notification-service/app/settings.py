import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
KAFKA_BROKER = os.getenv("KAFKA_BROKER")
USER_TOPIC = os.getenv("USER_TOPIC") 
ORDER_TOPIC = os.getenv("ORDER_TOPIC")
PAYMENT_TOPIC = os.getenv("PAYMENT_TOPIC")

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# from starlette.config import Config
# from starlette.datastructures import Secret

# try:
#     config = Config(".env")
# except FileNotFoundError:
#     config = Config()

# DATABASE_URL = config("DATABASE_URL", cast=Secret)
# KAFKA_BROKER = config("KAFKA_BROKER", cast=str)
# USER_TOPIC  = config("USER_TOPIC ", cast=str)
# ORDER_TOPIC = config("ORDER_TOPIC", cast=str)
# PAYMENT_TOPIC=config("PAYMENT_TOPIC",cast=Secret)
# TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)
# SMTP_SERVER = config("SMTP_SERVER",cast=Secret)
# SMTP_PORT = config("SMTP_PORT",cast=Secret)
# SMTP_USERNAME  = config("SMTP_USERNAME ",cast=Secret)
# SMTP_PASSWORD = config("SMTP_PASSWORD",cast=Secret)


