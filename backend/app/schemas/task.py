"""
Pydantic schemas for Task endpoints.
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TaskOut(BaseModel):
    id: int
    lesson_id: Optional[int]
    title: str
    slug: str
    description: str
    difficulty: str
    category: str
    hints: Optional[str]
    test_cases: str
    solution_template: Optional[str]
    time_limit_ms: int
    memory_limit_mb: int

    class Config:
        from_attributes = True


class TaskFilter(BaseModel):
    difficulty: Optional[str] = None
    category: Optional[str] = None
    lesson_id: Optional[int] = None
    search: Optional[str] = None
