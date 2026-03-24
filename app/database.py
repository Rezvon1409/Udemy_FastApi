from sqlalchemy import create_engine
from sqlalchemy.orm import  declarative_base , sessionmaker

DATABASE_URL = 'sqlite:///./udemy.db'

engine = create_engine(DATABASE_URL , echo=True)

SessionLocal = sessionmaker(autoflush=False , autocommit=False , bind=engine)

Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()