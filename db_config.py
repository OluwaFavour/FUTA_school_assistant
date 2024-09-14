from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncAttrs,
)
from sqlalchemy.orm import DeclarativeBase

from .settings import SQLALCHEMY_DATABASE_URL, DEBUG

async_engine: AsyncEngine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=DEBUG)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, autoflush=False, expire_on_commit=False
)


# Base class for declarative_base
class Base(AsyncAttrs, DeclarativeBase):
    pass
