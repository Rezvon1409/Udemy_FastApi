from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.database import engine, Base
from app.routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Udemy")

app.add_middleware(SessionMiddleware, secret_key="supersecretkey")

app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Udemy API"}