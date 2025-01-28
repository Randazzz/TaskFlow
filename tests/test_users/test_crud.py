import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from pytest_mock import MockerFixture
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.crud import UserCRUD
from src.db.models import User
from src.modules.users.schemas.user import UserCreate, UserResponse
from tests.test_data import UserTestData
from tests.utils import check_user


@pytest.mark.asyncio
async def test_create_user(test_session: AsyncSession) -> None:
    test_user_data = UserCreate(**UserTestData.TEST_USER_DATA)
    created_user = await UserCRUD.create_user(user=test_user_data, db=test_session)

    assert isinstance(created_user, UserResponse)

    retrieved_user = await test_session.execute(
        select(User).where(User.username == created_user.username)  # type: ignore
    )
    retrieved_user = retrieved_user.scalar_one_or_none()
    assert retrieved_user is not None
    assert retrieved_user.username == created_user.username

    check_user(test_user_data, created_user)


@pytest.mark.asyncio
async def test_get_user_by_field(test_session: AsyncSession) -> None:
    test_user_data = UserCreate(**UserTestData.TEST_USER_DATA)
    created_user = await UserCRUD.create_user(user=test_user_data, db=test_session)

    user_by_id = await UserCRUD.get_user_by_field(
        field_value=created_user.id, field_name="id", db=test_session
    )
    user_by_email = await UserCRUD.get_user_by_field(
        field_value=created_user.email, field_name="email", db=test_session
    )

    assert isinstance(user_by_id, UserResponse)
    assert isinstance(user_by_email, UserResponse)

    check_user(test_user_data, user_by_id)
    check_user(test_user_data, user_by_email)


@pytest.mark.asyncio
async def test_create_user_duplicate_email(test_session: AsyncSession) -> None:
    test_user_data = UserCreate(**UserTestData.TEST_USER_DATA)
    duplicate_user_data = UserCreate(**UserTestData.DUPLICATE_USER_DATA)

    await UserCRUD.create_user(test_user_data, test_session)

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
    test_user_data = UserCreate(**UserTestData.TEST_USER_DATA)

    mocker.patch.object(test_session, "add", side_effect=SQLAlchemyError("DB Error"))

    with pytest.raises(HTTPException) as exc_info:
        await UserCRUD.create_user(test_user_data, test_session)

    assert exc_info.value.status_code == 500
    assert "An error occurred while processing the request" in exc_info.value.detail

    retrieved_user = await test_session.execute(
        select(User).where(User.email == test_user_data.email)  # type: ignore
    )
    assert retrieved_user.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_get_user_by_field_not_found(test_session: AsyncSession) -> None:
    user_by_id = await UserCRUD.get_user_by_field(
        field_value=1, field_name="id", db=test_session
    )
    user_by_email = await UserCRUD.get_user_by_field(
        field_value="user@example.com", field_name="email", db=test_session
    )

    assert user_by_id is None
    assert user_by_email is None
