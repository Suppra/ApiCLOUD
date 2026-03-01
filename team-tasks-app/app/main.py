"""Application entrypoint with FastAPI wired."""

from fastapi import FastAPI

from app.routes import auth


app = FastAPI(title="Team Tasks App")

app.include_router(auth.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
