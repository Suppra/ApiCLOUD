"""Pydantic data models for the users API."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
