"""
Code submission model - stores user code submissions and results.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    code = Column(Text, nullable=False)

    # Execution results
    is_correct = Column(Boolean, default=False)
    execution_time_ms = Column(Float, nullable=True)
    memory_used_mb = Column(Float, nullable=True)
    output = Column(Text, nullable=True)
    error = Column(Text, nullable=True)

    # AI analysis
    ai_feedback = Column(Text, nullable=True)
    ai_score = Column(Float, nullable=True)  # 0-100

    # Status
    status = Column(String, default="pending")  # pending, running, completed, error

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="submissions")
    task = relationship("Task", back_populates="submissions")
