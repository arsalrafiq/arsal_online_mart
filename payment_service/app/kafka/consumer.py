# app/kafka/consumer.py
from aiokafka import AIOKafkaConsumer
import json
from app.core.config import settings

async def consume_messages(topic: str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="payment-service-group"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Received message: {msg.value.decode()} on topic {msg.topic}")
            # Process the message as needed
    finally:
        await consumer.stop()
