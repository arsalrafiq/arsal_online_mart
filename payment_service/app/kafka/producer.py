# app/kafka/producer.py
from datetime import datetime
from aiokafka import AIOKafkaProducer
import json
from app.core.config import settings

producer = None

async def get_kafka_producer():
    global producer
    if producer is None:
        producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
        await producer.start()
    return producer
class DateTimeEncoder(json.JSONEncoder):
       def default(self, obj):
           if isinstance(obj, datetime):
               return obj.isoformat()
           return super().default(obj)

async def produce_message(topic: str, message: dict):
    producer = await get_kafka_producer()
    value = json.dumps(message).encode()
    await producer.send_and_wait(topic, value)