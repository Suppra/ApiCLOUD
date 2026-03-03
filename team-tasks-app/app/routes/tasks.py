from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import db_models
from app.db import get_session
from app.models import Task, TaskCreate, TaskUpdate


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    # Verify user exists
    user = session.get(db_models.User, task.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db_task = db_models.Task(
        title=task.title,
        description=task.description,
        status=task.status,
        user_id=task.user_id,
        created_at=datetime.utcnow(),
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get("/", response_model=List[Task])
def list_tasks(session: Session = Depends(get_session)):
    """List all tasks (Basic CRUD)."""
    result = session.scalars(select(db_models.Task).order_by(db_models.Task.id)).all()
    return result


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(db_models.Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task


@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)):
    db_task = session.get(db_models.Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    update_data = task_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)

    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    db_task = session.get(db_models.Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    session.delete(db_task)
    session.commit()
    return None
