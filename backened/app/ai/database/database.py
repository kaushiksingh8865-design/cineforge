"""from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , DeclarativeBase , Session
from app.ai.core.settings import settings
from collections.abc import Generator

engine =create_engine(
    settings.database_url,
    pool_pre_ping =True,
)
SessionLocal = sessionmaker(
    bind = engine,
    autoflush=False,
    autocommit = False,
    )
class Base(DeclarativeBase):
    pass

def get_db() -> Generator[Session , None , None]:
    db = SessionLocal()

    try:
        yield db
    finally: 
        db.close()



if __name__ == "__main__":
    with engine.connect() as connection:
        print("PostgreSQL connection successful")"""



from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.ai.core.settings import settings


engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        yield db


async def test_connection():
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))
        print("PostgreSQL async connection successful")


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_connection())