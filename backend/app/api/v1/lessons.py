"""
Lessons API endpoints.
"""
import asyncio
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
    try:
        # Таймаут на всю операцию генерации теории
        result = await asyncio.wait_for(
            service.get_lesson_theory(lesson_id, current_user.id, regenerate),
            timeout=60  # 60 секунд на генерацию AI
        )
        return result
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="Превышено время ожидания генерации теории. Попробуйте позже или нажмите 'Сгенерировать снова'"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении теории: {str(e)}"
        )


@router.get("/{lesson_id}/task")
async def get_lesson_task(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get (or generate once) the task for a lesson. Always returns the same task."""
    service = LessonService(db)
    try:
        result = await asyncio.wait_for(
            service.get_or_create_lesson_task(lesson_id),
            timeout=60  # 60 секунд на генерацию задачи
        )
        return result
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="Превышено время ожидания генерации задачи. Попробуйте позже"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении задачи: {str(e)}"
        )


@router.post("/initialize")
async def initialize_course(db: AsyncSession = Depends(get_db)):
    """Initialize course structure in database (run once on setup)."""
    service = LessonService(db)
    await service.initialize_course()
    return {"message": "Course initialized successfully"}


@router.post("/sync")
async def sync_course(db: AsyncSession = Depends(get_db)):
    """Sync lesson metadata from course_structure. Clears theory/task cache for changed lessons."""
    service = LessonService(db)
    result = await service.sync_course()
    return {"message": "Course synced", **result}
