"""Basic authentication endpoints with simple bearer tokens (no JWT)."""

import secrets
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app import db_models
from app.utils.security import verify_password


router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
	email: EmailStr
	password: str


class TokenResponse(BaseModel):
	access_token: str
	token_type: str = "bearer"


# Token store: token -> email

# In-memory token store: token -> email
TOKEN_STORE: dict[str, str] = {}


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, session: Session = Depends(get_session)) -> TokenResponse:
	user = session.scalar(select(db_models.User).where(db_models.User.email == payload.email))
	if not user or not verify_password(payload.password, user.password_hash):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

	token = secrets.token_hex(16)
	TOKEN_STORE[token] = payload.email
	return TokenResponse(access_token=token)


def get_current_user(authorization: Optional[str] = Header(default=None)) -> str:
	"""Basic bearer-token validation against in-memory store."""
	if not authorization or not authorization.lower().startswith("bearer "):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

	token = authorization.split(" ", 1)[1]
	email = TOKEN_STORE.get(token)
	if not email:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

	return email


def require_user(email: str = Depends(get_current_user)) -> str:
	"""Dependency to inject current user email into protected endpoints."""
	return email
