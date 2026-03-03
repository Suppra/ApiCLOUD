"""Application entrypoint: FastAPI app and router registration."""

from fastapi import FastAPI

from app import db_models
from app.db import Base, engine
from app.routes import auth, filters, tasks, users


app = FastAPI(title="Team Tasks App")

# Ensure tables exist (simple bootstrap; for prod use migrations)
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(filters.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
