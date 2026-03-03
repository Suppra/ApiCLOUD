from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import db_models
from app.db import get_session
from app.models import Task


# routes under a dedicated subpath to avoid conflicting with /tasks/{task_id}
router = APIRouter(prefix="/tasks/filters", tags=["Filters"])


@router.get("/search", response_model=List[Task])
def search_tasks(q: str, session: Session = Depends(get_session)):
    """Search tasks by title or description."""
    query = select(db_models.Task).where(
        (db_models.Task.title.ilike(f"%{q}%")) | (db_models.Task.description.ilike(f"%{q}%"))
    )
    result = session.scalars(query).all()
    return result


@router.get("/filter", response_model=List[Task])
def filter_tasks(
    user_id: Optional[int] = None,
    status: Optional[str] = None,
    session: Session = Depends(get_session)
):
    """Filter tasks by user_id or status."""
    query = select(db_models.Task)
    if user_id:
        query = query.where(db_models.Task.user_id == user_id)
    if status:
        query = query.where(db_models.Task.status == status)
    
    result = session.scalars(query.order_by(db_models.Task.id)).all()
    return result
