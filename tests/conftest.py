import logging
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app.core.config import settings
from app.db.models import Base

DATABASE_URL_TEST: str = (
    f"postgresql+asyncpg://{settings.DATABASE_USER_TEST}:"
    f"{settings.DATABASE_PASSWORD_TEST}@{settings.DATABASE_HOST_TEST}:"
    f"{settings.DATABASE_PORT_TEST}/{settings.DATABASE_NAME_TEST}"
)

engine_test = create_async_engine(DATABASE_URL_TEST, echo=False)
async_session_test = async_sessionmaker(bind=engine_test, expire_on_commit=False)


@pytest.fixture(scope="function")
async def test_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_test() as session:
        yield session

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine_test.dispose()


@pytest.fixture(scope="session", autouse=True)
def disable_logging() -> None:
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)
