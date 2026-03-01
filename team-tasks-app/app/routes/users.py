from fastapi import APIRouter, HTTPException, status
from app.models import User, UserCreate
from typing import List
from datetime import datetime

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# In-memory storage (simple demo). Each item is a `User` dict-like object.
users_db: List[User] = []
_next_id = 1


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    global _next_id
    # check email uniqueness
    for existing in users_db:
        if existing.email == user.email:
            raise HTTPException(status_code=400, detail="El email ya existe")

    created = User(
        id=_next_id,
        name=user.name,
        email=user.email,
        is_active=user.is_active,
        created_at=datetime.utcnow()
    )
    users_db.append(created)
    _next_id += 1
    return created


@router.get("/", response_model=List[User])
def list_users():
    return users_db


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
