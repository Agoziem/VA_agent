# pyright: strict = false
# type: ignore
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .config import settings
from sqlalchemy.ext.declarative import declarative_base

# Create Async Engine
engine = create_async_engine(settings.POSTGRES_URL, echo=False)

Base = declarative_base()

# Create Async Session
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency to get DB Session
async def async_get_db():
    async with AsyncSessionLocal() as session:
        yield session
