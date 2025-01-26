import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from pytest_mock import MockerFixture
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user import UserCreate
from app.db.crud import UserCRUD
from app.db.models import User
from tests.test_data import UserTestData


@pytest.mark.asyncio
async def test_create_user(test_session: AsyncSession) -> None:
    test_user = UserCreate(**UserTestData.TEST_USER)
    created_user = await UserCRUD.create_user(user=test_user, db=test_session)

    assert created_user.username == test_user.username
    assert created_user.full_name == test_user.full_name
    assert created_user.email == test_user.email
    assert created_user.age == test_user.age

    retrieved_user = await test_session.execute(
        select(User).where(User.username == created_user.username)  # type: ignore
    )
    retrieved_user = retrieved_user.scalar_one_or_none()
    assert retrieved_user is not None
    assert retrieved_user.username == created_user.username


@pytest.mark.asyncio
async def test_create_user_duplicate_email(test_session: AsyncSession) -> None:
    test_user = UserCreate(**UserTestData.TEST_USER)
    duplicate_user_data = UserCreate(**UserTestData.DUPLICATE_USER_DATA)

    await UserCRUD.create_user(test_user, test_session)

    with pytest.raises(HTTPException) as exc_info:
        await UserCRUD.create_user(duplicate_user_data, test_session)

    assert exc_info.value.status_code == 500
    assert "An error occurred while processing the request" in exc_info.value.detail

    retrieved_users = await test_session.execute(
        select(User).where(User.email == "user1@example.com")  # type: ignore
    )
    assert len(retrieved_users.scalars().all()) == 1


@pytest.mark.asyncio
async def test_create_user_invalid_data(test_session: AsyncSession) -> None:
    with pytest.raises(ValidationError) as exc_info:
        invalid_user_data = UserCreate(**UserTestData.INVALID_USER_DATA)
        await UserCRUD.create_user(user=invalid_user_data, db=test_session)

    errors = exc_info.value.errors()

    assert any(
        error["loc"] == ("username",) for error in errors
    ), "Expected username validation error, but not found"
    assert any(
        error["loc"] == ("full_name",) for error in errors
    ), "Expected full_name validation error, but not found"
    assert any(
        error["loc"] == ("email",) for error in errors
    ), "Expected email validation error, but not found"
    assert any(
        error["loc"] == ("age",) for error in errors
    ), "Expected age validation error, but not found"
    assert any(
        error["loc"] == ("password",) for error in errors
    ), "Expected password validation error, but not found"


@pytest.mark.asyncio
async def test_create_user_db_error(
    test_session: AsyncSession, mocker: MockerFixture
) -> None:
    user_data = UserCreate(**UserTestData.TEST_USER)

    mocker.patch.object(test_session, "add", side_effect=SQLAlchemyError("DB Error"))

    with pytest.raises(HTTPException) as exc_info:
        await UserCRUD.create_user(user_data, test_session)

    assert exc_info.value.status_code == 500
    assert "An error occurred while processing the request" in exc_info.value.detail

    retrieved_user = await test_session.execute(
        select(User).where(User.email == user_data.email)  # type: ignore
    )
    assert retrieved_user.scalar_one_or_none() is None
