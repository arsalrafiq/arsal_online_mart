# from sqlmodel import create_engine, Session, SQLModel
# from contextlib import contextmanager

# # Import your settings module
# from . import settings

# # Create the engine
# connection_string = str(settings.DATABASE_URL).replace(
#     "postgresql", "postgresql+psycopg"
# )
# engine = create_engine(
#     connection_string, connect_args={}, pool_recycle=300
# )

# # Create a context manager for the session
# @contextmanager
# def get_db():
#     db = Session(engine)
#     try:
#         yield db
#     finally:
#         db.close()

# # Define the create_db_and_tables function
# # def create_db_and_tables():
# #     SQLModel.metadata.create_all(engine)


# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)

# # Define the get_session function
# def get_session():
#     with get_db() as session:
#         yield session


# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# from app.settings import settings

# DATABASE_URL = settings.database_url

# engine = create_async_engine(DATABASE_URL, echo=True)

# async_session = sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False
# )

# # Dependency
# async def get_db():
#     async with async_session() as session:
#         yield session

from sqlmodel import SQLModel, create_engine, Session
from app.settings import settings

DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL, echo=True)

# Create all tables in the database
def init_db():
    SQLModel.metadata.create_all(engine)

# Dependency
def get_session():
    with Session(engine) as session:
        yield session
