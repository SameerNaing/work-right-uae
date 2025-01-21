from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

__all__ = ["Base", "get_db"]

# Create the async engine
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# Create the async session factory
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base for the ORM models
Base = declarative_base()


# Async dependency for the database session
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
