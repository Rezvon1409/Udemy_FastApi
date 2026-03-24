from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.database import engine, Base
from app.routers import auth, courses, lessons, tasks, purchases, reviews , progress

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Udemy")

app.add_middleware(SessionMiddleware, secret_key="supersecretkey")

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(lessons.router)
app.include_router(tasks.router)
app.include_router(purchases.router)
app.include_router(reviews.router)
app.include_router(progress.router)

@app.get("/")
def root():
    return {"message": "Udemy API"}