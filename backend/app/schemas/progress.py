"""
Pydantic schemas for Progress endpoints.
"""
from pydantic import BaseModel
from typing import List
from datetime import datetime


class ProgressOut(BaseModel):
    lesson_id: int
    completed: bool
    theory_read: bool
    tasks_completed: int
    total_tasks: int
    started_at: datetime
    completed_at: datetime | None

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    total_lessons: int
    completed_lessons: int
    completion_percentage: float
    current_streak: int
    total_xp: int
    level: int
    rating: float
    motivation_phrase: str
