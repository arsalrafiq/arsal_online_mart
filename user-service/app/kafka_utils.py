# app/kafka_utils.py
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
from app.config import settings
import json

async def get_kafka_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

async def consume_messages():
    consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="user_service_group",
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message: {message.value} on topic {message.topic}")
            # Process the message as needed
    finally:
        await consumer.stop()

async def start_kafka_consumer():
    asyncio.create_task(consume_messages())