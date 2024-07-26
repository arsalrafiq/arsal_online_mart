# from aiokafka import AIOKafkaProducer
# import asyncio
# from app.settings import settings

# async def produce_kafka_message(topic: str, value: str):
#     producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_bootstrap_servers)
#     await producer.start()
#     try:
#         await producer.send_and_wait(topic, value.encode('utf-8'))
#     finally:
#         await producer.stop()

from aiokafka import AIOKafkaProducer
import json
import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = "order_created"

producer = None

async def get_kafka_producer():
    global producer
    if producer is None:
        producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        await producer.start()
    return producer

async def produce_order_created_event(order_id: str):
    producer = await get_kafka_producer()
    value = json.dumps({"order_id": order_id}).encode()
    await producer.send_and_wait(KAFKA_TOPIC, value)
    