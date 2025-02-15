import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine

from api.v1.auth.models import Base


DATABASE_URL: str = 'postgresql+asyncpg://postgres:postgres@db:5432/edelweiss_auth'

engine: AsyncEngine = create_async_engine(DATABASE_URL)
SessionLocal: async_sessionmaker = async_sessionmaker(bind=engine, autoflush=False, autocommit=False)


async def get_db():
    db: AsyncSession = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
