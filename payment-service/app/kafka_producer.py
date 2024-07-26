from app.kafka_producer import KafkaProducer
import json
from app.settings import settings

producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def produce_kafka_message(topic, message):
    producer.send(topic, message)
    producer.flush()

#payment-service/app/kafka_producer.py



# from aiokafka import AIOKafkaProducer
# import json
# import os

# KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
# KAFKA_TOPIC = "order_created"

# producer = None

# async def get_kafka_producer():
#     global producer
#     if producer is None:
#         producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
#         await producer.start()
#     return producer

# async def produce_order_created_event(order_id: str):
#     producer = await get_kafka_producer()
#     value = json.dumps({"order_id": order_id}).encode()
#     await producer.send_and_wait(KAFKA_TOPIC, value)
