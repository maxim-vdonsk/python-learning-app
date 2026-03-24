"""
Pydantic schemas for Submission endpoints.
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class SubmissionCreate(BaseModel):
    task_id: int
    code: str


class SubmissionOut(BaseModel):
    id: int
    user_id: int
    task_id: int
    code: str
    is_correct: bool
    execution_time_ms: Optional[float]
    memory_used_mb: Optional[float]
    output: Optional[str]
    error: Optional[str]
    ai_feedback: Optional[str]
    ai_score: Optional[float]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class SubmissionResult(BaseModel):
    submission_id: int
    is_correct: bool
    execution_time_ms: Optional[float]
    memory_used_mb: Optional[float]
    output: Optional[str]
    error: Optional[str]
    ai_feedback: str
    ai_score: float
    recommendations: List[str] = []
    passed_tests: int = 0
    total_tests: int = 0
