"""Pydantic data models for the users API."""
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


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
		orm_mode = True
