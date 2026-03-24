"""
Task (coding challenge) database model.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class DifficultyEnum(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)  # nullable for standalone tasks
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(Enum(DifficultyEnum), nullable=False, default=DifficultyEnum.easy)
    category = Column(String, nullable=False)  # e.g., "algorithms", "strings"
    hints = Column(Text)       # JSON array of hints
    test_cases = Column(Text, nullable=False)  # JSON array of {input, expected_output}
    solution_template = Column(Text)  # Starter code for user
    reference_solution = Column(Text) # Hidden reference solution
    time_limit_ms = Column(Integer, default=2000)
    memory_limit_mb = Column(Integer, default=64)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    lesson = relationship("Lesson", back_populates="tasks")
    submissions = relationship("Submission", back_populates="task")
