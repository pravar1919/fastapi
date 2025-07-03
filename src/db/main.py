from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import Config
from typing import AsyncGenerator

engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True,
)


# this is to create tables at the runtime
async def initdb():
    async with engine.begin() as conn:
        from src.db.models import Book

        await conn.run_sync(SQLModel.metadata.create_all)


# this is to create session of the engine to use across the project
async def get_sessions() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with Session() as session:
        yield session