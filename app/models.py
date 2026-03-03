"""Pydantic data models for the users API."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr
    is_active: bool = True


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "pendiente"


class TaskCreate(TaskBase):
    user_id: int


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class Task(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
