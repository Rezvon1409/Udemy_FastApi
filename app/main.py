from fastapi import FastAPI
from app.database import engine , Base
from app.routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title = 'Udemy')

app.include_router(auth.router)


@app.get('/')
def root():
    return {"message": "Udemy API"}