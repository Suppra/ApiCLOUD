"""Application entrypoint: FastAPI app and router registration."""
from fastapi import FastAPI
from app.routes import users

app = FastAPI(title="Team Tasks - Users")

app.include_router(users.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
