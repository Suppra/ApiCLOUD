from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import db_models
from app.db import get_session
from app.models import User, UserCreate
from app.utils.security import hash_password
from app.db import get_session
from app import db_models


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    existing = session.scalar(select(db_models.User).where(db_models.User.email == user.email))
    if existing:
        raise HTTPException(status_code=400, detail="El email ya existe")
    password_hash = hash_password(user.password)

    db_user = db_models.User(
        name=user.name,
        email=user.email,
        is_active=user.is_active,
        created_at=datetime.utcnow(),
        password_hash=password_hash,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/", response_model=List[User])
def list_users(session: Session = Depends(get_session)):
    result = session.scalars(select(db_models.User).order_by(db_models.User.id)).all()
    return result


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(db_models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
