"""
Pydantic schemas for Lesson endpoints.
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class WeekOut(BaseModel):
    id: int
    number: int
    title: str
    description: Optional[str]

    class Config:
        from_attributes = True


class LessonOut(BaseModel):
    id: int
    week_id: int
    title: str
    slug: str
    description: Optional[str]
    topic: str
    order: int
    theory_content: Optional[str]
    code_examples: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class LessonWithProgress(LessonOut):
    completed: bool = False
    theory_read: bool = False
    tasks_completed: int = 0
    total_tasks: int = 0


class TheoryRequest(BaseModel):
    lesson_id: int
    regenerate: bool = False
