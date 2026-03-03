"""Database configuration and session management."""

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://team_tasks:team_tasks@db:5432/team_tasks",
)

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base = declarative_base()


def get_session() -> Generator:
    """FastAPI dependency that yields a SQLAlchemy session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
