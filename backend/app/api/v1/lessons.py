"""
Lessons API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.lesson_service import LessonService

router = APIRouter()


@router.get("/course")
async def get_course(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get full course structure with user progress."""
    service = LessonService(db)
    return await service.get_course(current_user.id)


@router.get("/{lesson_id}/theory")
async def get_theory(
    lesson_id: int,
    regenerate: bool = False,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get theory content for a lesson, generating via AI if needed."""
    service = LessonService(db)
    return await service.get_lesson_theory(lesson_id, current_user.id, regenerate)


@router.post("/initialize")
async def initialize_course(db: AsyncSession = Depends(get_db)):
    """Initialize course structure in database (run once on setup)."""
    service = LessonService(db)
    await service.initialize_course()
    return {"message": "Course initialized successfully"}
