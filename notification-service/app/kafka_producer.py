from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError
from fastapi import HTTPException
import json
from app.settings import KAFKA_BROKER, USER_TOPIC, ORDER_TOPIC, PAYMENT_TOPIC
from app.service import user_notification_func_map, order_notification_func_map, payment_notification_func_map

async def get_kafka_consumer(topics):
    consumer = AIOKafkaConsumer(
        *topics,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest'
    )
    await consumer.start()
    return consumer

async def process_messages(consumer, notification_func_map):
    try:
        async for msg in consumer:
            data = json.loads(msg.value)
            notification_func = notification_func_map.get(data["notification_type"])
            if notification_func:
                notification_func(data["email"])
            else:
                print(f"Unknown notification type: {data['notification_type']}")
    except KafkaConnectionError as e:
        raise HTTPException(status_code=500, detail=f"Kafka connection error: {str(e)}")
    finally:
        await consumer.stop()

async def user_consumer():
    consumer = await get_kafka_consumer([USER_TOPIC])
    await process_messages(consumer, user_notification_func_map)

async def order_consumer():
    consumer = await get_kafka_consumer([ORDER_TOPIC])
    await process_messages(consumer, order_notification_func_map)

async def payment_consumer():
    consumer = await get_kafka_consumer([PAYMENT_TOPIC])
    await process_messages(consumer, payment_notification_func_map)
