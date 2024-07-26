# main.py
from contextlib import asynccontextmanager
from typing import Annotated
from sqlmodel import Session, SQLModel
from fastapi import FastAPI, Depends, HTTPException
from typing import AsyncGenerator
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
import json

from app import settings
from app.db_engine import engine
from app.models.inventory_model import InventoryItem
from app.crud.inventory_crud import add_new_inventory_item, delete_inventory_item_by_id, get_all_inventory_items, get_inventory_item_by_id, update_inventory_item_by_id
from app.deps import get_session, get_kafka_producer
from app.consumers.add_stock_consumer import consume_messages

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables...")
    create_db_and_tables()
    print("\n\n LIFESPAN created!! \n\n")
    task = asyncio.create_task(consume_messages("inventory-add-stock-response", 'broker:19092'))
    yield
    await task

app = FastAPI(
    lifespan=lifespan,
    title="Inventory-service API with DB",
    version="0.0.1",
)

@app.get("/")
def read_root():
    return {"Hello": "Inventory Service"}

@app.post("/manage-inventory/", response_model=InventoryItem)
async def create_new_inventory_item(item: InventoryItem, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    """ Create a new inventory item and send it to Kafka"""
    try:
        print(f"Received item: {item.dict()}")
        item_dict = item.dict()
        item_json = json.dumps(item_dict).encode("utf-8")
        print(f"Encoded item JSON: {item_json}")
        await producer.send_and_wait("AddStock", item_json)
        print("Message sent to Kafka")
        new_item = add_new_inventory_item(item, session)
        print(f"New item added to database: {new_item.dict()}")
        session.commit()
        print("Session committed")
        return {"message": "Inventory Item Created Successfully", "data": new_item}
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        session.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/manage-inventory/all", response_model=list[InventoryItem])
def all_inventory_items(session: Annotated[Session, Depends(get_session)]):
    """ Get all inventory items from the database"""
    try:
        items = get_all_inventory_items(session)
        print(f"Retrieved {len(items)} items from database")
        return items
    except Exception as e:
        print(f"Error retrieving items: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/manage-inventory/{item_id}", response_model=InventoryItem)
def single_inventory_item(item_id: int, session: Annotated[Session, Depends(get_session)]):
    """ Get a single inventory item by ID"""
    try:
        return get_inventory_item_by_id(inventory_item_id=item_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/manage-inventory/{item_id}", response_model=dict)
def delete_single_inventory_item(item_id: int, session: Annotated[Session, Depends(get_session)]):
    """ Delete a single inventory item by ID"""
    try:
        return delete_inventory_item_by_id(inventory_item_id=item_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
#update Inventory Item by ID
@app.patch("/manage-inventory/{item_id}", response_model=InventoryItem)
def update_single_inventory_item(item_id: int, item: InventoryItem, session: Annotated[Session, Depends(get_session)]):
    """ Update a single inventory item by ID"""
    try:
        updated_item = update_inventory_item_by_id(item_id=item_id, to_update_item_data=item, session=session)
        return {"message": "Inventory Item Updated Successfully", "data": updated_item}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))