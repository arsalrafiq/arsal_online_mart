# import uvicorn
# from fastapi import FastAPI
# from app.router import router
# from app.models import SQLModel
# from app.db import engine

# app = FastAPI()

# @app.on_event("startup")
# async def on_startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)

# app.include_router(router)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

from contextlib import asynccontextmanager
import logging
from app import settings
from sqlmodel import Field, Session, SQLModel, create_engine
from fastapi import FastAPI, Depends, HTTPException
from typing import AsyncGenerator
from aiokafka import AIOKafkaConsumer
import asyncio
from app.kafka_producer import AIOKafkaProducer
from app import payment_pb2
from fastapi import FastAPI
from app.router import router
from app.db import create_db_and_tables, get_session
import asyncio

from app.schemas import PaymentCreate, PaymentResponse
from app.service import PaymentService

connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

engine = create_engine(
    connection_string, connect_args={}, pool_recycle=300
)

async def create_db_and_tables() -> None:
    await asyncio.to_thread(SQLModel.metadata.create_all, engine)

async def consume_messages(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="my-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message: {message.value.decode()} on topic {message.topic}")

            new_payment = payment_pb2.Payment()
            new_payment.ParseFromString(message.value)
            print(f"\n\n Consumer Deserialized data: {new_payment}")

            # Add payment to DB
            # ...

    finally:
        await consumer.stop()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables.")
    task = asyncio.create_task(consume_messages('payments', 'broker:19092'))
    await create_db_and_tables()
    yield

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    lifespan=lifespan,
    title="Payment Service API",
    version="0.0.1",
)

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

@app.post("/payments/", response_model=PaymentResponse)
async def create_payment(payment: PaymentCreate, session: Session = Depends(get_session)):
    try:
        new_payment = await PaymentService.create_payment(session, payment)
        return new_payment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"Hello": "Payment Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

