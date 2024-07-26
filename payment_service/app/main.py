# app/main.py
from fastapi import FastAPI
from app.api.payment import router as payment_router
from app.core.config import settings
from app.db.session import engine
from app.models.payment import SQLModel
from app.kafka.consumer import consume_messages
import asyncio

app = FastAPI(title=settings.PROJECT_NAME)

@app.on_event("startup")
async def startup_event():
    # Create database tables
    SQLModel.metadata.create_all(engine)
    
    # Start Kafka consumer
    asyncio.create_task(consume_messages("payment_events"))

app.include_router(payment_router, prefix=settings.API_V1_STR)