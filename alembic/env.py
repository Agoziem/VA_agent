import os
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv
from app.core.database import Base
from app.api.v1.todos.models import *

# Load environment variables from .env
load_dotenv()

# Get the database URL from .env
POSTGRES_URL = os.getenv("POSTGRES_URL", "your_default_postgres_url")

# Ensure the POSTGRES_URL starts with "postgresql+asyncpg://"
if not POSTGRES_URL.startswith("postgresql+asyncpg://"):
    raise ValueError(
        "POSTGRES_URL must use asyncpg driver (postgresql+asyncpg://)")

# Alembic Config object
config = context.config

# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for autogeneration
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=POSTGRES_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode with async support."""
    connectable = create_async_engine(POSTGRES_URL, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    """Run migrations in a synchronous transaction."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    # Use asyncio to run the async function
    asyncio.run(run_migrations_online())
