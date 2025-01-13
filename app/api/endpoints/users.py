from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user import UserCreate, UserResponse
from app.db.crud import user_crud
from app.db.database import get_db

user_router = APIRouter()


@user_router.post('/', response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserResponse:
    user = await user_crud.create_user(user=user, db=db)
    return user


@user_router.get('/{user_id}', response_model=UserResponse)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)) -> UserResponse:
    user = await user_crud.get_user_by_id(user_id=user_id, db=db)
    return user
