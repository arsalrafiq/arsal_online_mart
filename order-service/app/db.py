# app/db.py
from sqlmodel import create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from app import settings

# Create the async engine
connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+asyncpg"
)
engine: AsyncEngine = create_async_engine(connection_string, echo=True, future=True)

# Create an async session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session