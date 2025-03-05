from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


from sqlalchemy.orm import Query


async_engine = create_async_engine(settings.DATABASE_URL, future=True)
sync_engine = create_engine(
    settings.DATABASE_URL.replace("+aiomysql", "+pymysql"), echo=True, future=True
)


SyncSessionLocal = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)

AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
