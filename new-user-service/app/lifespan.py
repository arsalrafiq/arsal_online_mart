# app/lifespan.py
from fastapi import FastAPI
from kafka import KafkaProducer
from app.settings import settings

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    app.state.kafka_producer = KafkaProducer(bootstrap_servers=settings.kafka_broker)

@app.on_event("shutdown")
async def shutdown_event():
    app.state.kafka_producer.close()
