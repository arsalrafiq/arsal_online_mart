# app/db.py
from sqlmodel import SQLModel, create_engine, Session
from app.models import User
from app.settings import settings

engine = create_engine(settings.database_url)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
