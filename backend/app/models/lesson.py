"""
Lesson and Week database models.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Week(Base):
    __tablename__ = "weeks"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)

    lessons = relationship("Lesson", back_populates="week", order_by="Lesson.order")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    week_id = Column(Integer, ForeignKey("weeks.id"), nullable=False)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    topic = Column(String, nullable=False)  # e.g., "variables", "loops"
    order = Column(Integer, nullable=False)
    theory_content = Column(Text)  # Pre-generated theory
    code_examples = Column(Text)   # JSON array of code examples

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    week = relationship("Week", back_populates="lessons")
    tasks = relationship("Task", back_populates="lesson", cascade="all, delete-orphan")
    progress_entries = relationship("Progress", back_populates="lesson")
