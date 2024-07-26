# app/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.models import UserCreate, UserRead, UserUpdate
from app.crud import create_user, get_user, update_user, delete_user, get_users
from app.db import get_session
from app.auth import create_access_token
from app.kafka_utils import get_kafka_producer
from aiokafka import AIOKafkaProducer
from pydantic import ValidationError

router = APIRouter()

@router.post("/users/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    user: UserCreate,
    session: Session = Depends(get_session),
    producer: AIOKafkaProducer = Depends(get_kafka_producer)
):
    try:
        db_user = create_user(session, user)
        await producer.send_and_wait("user_events", {"event": "user_created", "user_id": db_user.id})
        return db_user
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, session: Session = Depends(get_session)):
    db_user = get_user(session, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=UserRead)
async def update_existing_user(
    user_id: int,
    user: UserUpdate,
    session: Session = Depends(get_session),
    producer: AIOKafkaProducer = Depends(get_kafka_producer)
):
    db_user = update_user(session, user_id, user)
    await producer.send_and_wait("user_events", {"event": "user_updated", "user_id": db_user.id})
    return db_user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_user(
    user_id: int,
    session: Session = Depends(get_session),
    producer: AIOKafkaProducer = Depends(get_kafka_producer)
):
    delete_user(session, user_id)
    await producer.send_and_wait("user_events", {"event": "user_deleted", "user_id": user_id})

@router.get("/users/", response_model=list[UserRead])
def read_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    users = get_users(session, skip=skip, limit=limit)
    return users