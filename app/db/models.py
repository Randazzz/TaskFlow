from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import ForeignKey, String, func, mapped_column
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    full_name: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    age: Mapped[int]
    hashed_password: Mapped[bytes]
    tasks: Mapped[List["Task"]] = relationship(back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}), fullname={self.full_name!r})"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped[User] = relationship(back_populates="tasks")

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, title={self.title!r}, completed={self.completed!r}, owner={self.owner!r})"


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    refresh_token: Mapped[str] = mapped_column(nullable=False)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=False, onupdate=func.now())

    def __repr__(self) -> str:
        return f"Task(uuid={self.uuid!r}, expires_at={self.expires_at!r}, created_at={self.created_at!r})"
