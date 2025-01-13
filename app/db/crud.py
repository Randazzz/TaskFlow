from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.schemas.user import UserCreate, UserResponse
from app.db.models import User


class UserCRUD:

    @staticmethod
    async def get_user_by_id(user_id: int, db: AsyncSession) -> UserResponse:
        query = select(User).where(User.id == user_id)  # type: ignore
        result = await db.execute(query)
        user = result.scalars().first()

        return UserResponse(
            id=user.id,
            username=user.username,
            full_name=user.full_name,
            email=user.email,
            age=user.age,
        )

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

        db.add(db_user)

        await db.commit()

        await db.refresh(db_user)

        return UserResponse(
            id=db_user.id,
            username=db_user.username,
            full_name=db_user.full_name,
            email=db_user.email,
            age=db_user.age,
        )


user_crud = UserCRUD()
