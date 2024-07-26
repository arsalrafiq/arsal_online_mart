# # main.py
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi import FastAPI
from app.router import router


async def consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="my-todos-group",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"Received message: {message.value.decode()} on topic {message.topic}")
            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()

@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    # print("Creating tables..")
    task = asyncio.create_task(consume_messages('notificatios', 'broker:19092'))
    yield


app = FastAPI(lifespan=lifespan, title="Notification API with DB", 
    version="0.0.1"
        )


@app.get("/")
def read_root():
    return {"App": "notification-service"}

# Kafka Producer as a dependency
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

app.include_router(router)
# import logging
# from fastapi import FastAPI
# from app.router import router
# from app.db import create_db_and_tables
# import asyncio
# from app.kafka_producer import user_consumer, order_consumer, payment_consumer

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# app = FastAPI()

# @app.on_event("startup")
# async def on_startup():
#     create_db_and_tables()
#     logger.info("Database and tables created.")
#     asyncio.create_task(user_consumer())
#     asyncio.create_task(order_consumer())
#     asyncio.create_task(payment_consumer())
#     logger.info("Kafka consumers started.")

# app.include_router(router)
# from contextlib import asynccontextmanager
# from fastapi import FastAPI
# from typing import AsyncGenerator
# from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
# import asyncio
# from app.router import router 
# from app.kafka_producer import user_consumer, order_consumer, payment_consumer

# import json

# async def consume_messages(topic, bootstrap_servers):
#     # Create a consumer instance.
#     consumer = AIOKafkaConsumer(
#         topic,
#         bootstrap_servers=bootstrap_servers,
#         group_id="my-todos-group",
#         auto_offset_reset='earliest'
#     )

#     # Start the consumer.
#     await consumer.start()
#     try:
#         # Continuously listen for messages.
#         async for message in consumer:
#             print(f"Received message: {message.value.decode()} on topic {message.topic}")
#             # Here you can add code to process each message.
#             # Example: parse the message, store it in a database, etc.
#     finally:
#         # Ensure to close the consumer when done.
#         await consumer.stop()


# # The first part of the function, before the yield, will
# # be executed before the application starts.
# # https://fastapi.tiangolo.com/advanced/events/#lifespan-function
# # loop = asyncio.get_event_loop()
# @asynccontextmanager
# async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
#     # print("Creating tables..")
#     task = asyncio.create_task(consume_messages('todos', 'broker:19092'))
#     yield


# app = FastAPI(lifespan=lifespan, title="Notification API with DB", 
#     version="0.0.1"
#         )


# @app.get("/")
# def read_root():
#     return {"App": "notification-service"}

# # Kafka Producer as a dependency
# async def get_kafka_producer():
#     producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
#     await producer.start()
#     try:
#         yield producer
#     finally:
#         await producer.stop()

#     asyncio.create_task(user_consumer())
#     asyncio.create_task(order_consumer())
#     asyncio.create_task(payment_consumer())        

# app.include_router(router)        





