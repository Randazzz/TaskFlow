from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.config import settings
from app.db.models import Base

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DATABASE_USER}:"
    f"{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:"
    f"{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
)

engine = create_async_engine(
    DATABASE_URL, echo=settings.DEBUG
)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with async_session() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
