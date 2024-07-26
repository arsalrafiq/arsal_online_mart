# app/db/session.py
# from sqlmodel import create_engine, Session

# from app.core.config import settings

# engine = create_engine(settings.DATABASE_URL, echo=True)

# def get_session():
#     with Session(engine) as session:
#         yield session
from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings

def get_engine():
    connection_string = str(settings.DATABASE_URL).replace("postgresql", "postgresql+psycopg")
    return create_engine(connection_string, connect_args={}, pool_recycle=300)

engine = get_engine()

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session