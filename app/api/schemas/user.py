import re

from pydantic import BaseModel, EmailStr, field_validator


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

    @field_validator("password")
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", password):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[\W_]", password):
            raise ValueError("Password must contain at least one special character")
        return password
