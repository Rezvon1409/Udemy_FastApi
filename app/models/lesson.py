from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    video_url = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    order = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


    course = relationship("Course", back_populates="lessons")
    tasks = relationship("Task", back_populates="lesson")
    progress = relationship("LessonProgress", back_populates="lesson")