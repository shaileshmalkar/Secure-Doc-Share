from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base
from app.core.config import DATABASE_URL

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

# For SQLAlchemy 1.4, we create sessions directly from the engine
# This is compatible with both 1.4 and 2.0

# Base class for models
Base = declarative_base()

# Dependency to get database session
async def get_db():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        try:
            yield session
        finally:
            await session.close()
