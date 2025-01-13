from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str | None
    email: EmailStr
    age: int


class UserCreate(BaseModel):
    username: str
    full_name: str | None
    email: EmailStr
    age: int
    password: str
