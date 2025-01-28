import logging

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.models import User
from src.modules.users.schemas.user import UserCreate, UserResponse

logger = logging.getLogger(__name__)


class UserCRUD:

    @staticmethod
    async def create_user(user: UserCreate, db: AsyncSession) -> UserResponse:
        # hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            full_name=user.full_name,
            email=user.email,
            age=user.age,
            hashed_password=user.password,
        )
        try:

            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)

        except SQLAlchemyError as e:
            await db.rollback()
            logging.error(e)
            raise HTTPException(
                status_code=500,
                detail="An error occurred while processing the request",
            )

        return UserResponse(
            id=db_user.id,
            username=db_user.username,
            full_name=db_user.full_name,
            email=db_user.email,
            age=db_user.age,
        )

    @staticmethod
    async def get_user_by_field(
        field_value: int | EmailStr, field_name: str, db: AsyncSession
    ) -> UserResponse | None:
        if field_name == "id":
            user_id = field_value
            query = select(User).where(User.id == user_id)  # type: ignore
        else:
            user_email = field_value
            query = select(User).where(User.email == user_email)  # type: ignore
        try:
            result = await db.execute(query)
            user = result.scalars().first()

        except SQLAlchemyError as e:
            logging.error(e)
            raise HTTPException(
                status_code=500,
                detail="An error occurred while processing the request",
            )

        if user is None:
            return None

        return UserResponse(
            id=user.id,
            username=user.username,
            full_name=user.full_name,
            email=user.email,
            age=user.age,
        )

    @staticmethod
    async def get_user_by_id(user_id: int, db: AsyncSession) -> UserResponse | None:
        return await UserCRUD.get_user_by_field(user_id, "id", db)

    @staticmethod
    async def get_user_by_email(
        user_email: EmailStr, db: AsyncSession
    ) -> UserResponse | None:
        return await UserCRUD.get_user_by_field(user_email, "email", db)


user_crud = UserCRUD()
