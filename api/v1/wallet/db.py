from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from api.v1.wallet.models import Base


DATABASE_URL: str = 'postgresql+asyncpg://postgres:postgres@db:5432/edelweiss_wallet'


engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(bind=engine, autoflush=False, autocommit=False)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
