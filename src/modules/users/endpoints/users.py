from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.crud import user_crud
from src.db.database import get_db
from src.modules.users.schemas.user import UserCreate, UserResponse

user_router = APIRouter()


@user_router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
async def create_user(
    user: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    existing_user = await user_crud.get_user_by_email(user_email=user.email, db=db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    user = await user_crud.create_user(user=user, db=db)
    return user


@user_router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a user by their ID",
)
async def get_user_by_id(
    user_id: int, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    user = await user_crud.get_user_by_id(user_id=user_id, db=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
