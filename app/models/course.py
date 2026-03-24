from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(DECIMAL, nullable=False, default=0)
    is_published = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


    author = relationship("User", back_populates="courses")
    lessons = relationship("Lesson", back_populates="course")
    purchases = relationship("Purchase", back_populates="course")
    reviews = relationship("Review", back_populates="course")