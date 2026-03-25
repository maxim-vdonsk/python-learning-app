"""
Tasks API endpoints.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService

router = APIRouter()


@router.get("/")
async def get_tasks(
    difficulty: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    lesson_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(20, le=100),
    offset: int = Query(0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get tasks with optional filtering."""
    repo = TaskRepository(db)
    tasks = await repo.get_filtered(difficulty, category, lesson_id, search, limit, offset)
    return [
        {
            "id": t.id,
            "title": t.title,
            "slug": t.slug,
            "description": t.description,
            "difficulty": t.difficulty,
            "category": t.category,
            "solution_template": t.solution_template,
            "hints": t.hints,
        }
        for t in tasks
    ]


@router.get("/{task_id}")
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific task by ID."""
    repo = TaskRepository(db)
    task = await repo.get_by_id(task_id)
    if not task:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return {
        "id": task.id,
        "title": task.title,
        "slug": task.slug,
        "description": task.description,
        "difficulty": task.difficulty,
        "category": task.category,
        "hints": task.hints,
        "solution_template": task.solution_template,
        "time_limit_ms": task.time_limit_ms,
    }


@router.post("/generate")
async def generate_task(
    topic: str,
    difficulty: str = "easy",
    lesson_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate a new AI task for a topic."""
    service = TaskService(db)
    return await service.generate_ai_task(topic, difficulty, lesson_id)


@router.post("/{task_id}/regenerate-tests")
async def regenerate_task_tests(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Regenerate test cases for an existing task using AI."""
    from fastapi import HTTPException
    repo = TaskRepository(db)
    task = await repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    from app.services.ai_service import ai_service
    task_data = await ai_service.generate_task(
        topic=task.category or "general",
        difficulty=task.difficulty.value if hasattr(task.difficulty, "value") else str(task.difficulty),
        lesson_title=task.title,
    )
    new_test_cases = task_data.get("test_cases", [])
    if not new_test_cases:
        raise HTTPException(status_code=500, detail="AI не смог сгенерировать тест-кейсы")

    import json
    await repo.update(task_id, test_cases=json.dumps(new_test_cases, ensure_ascii=False))
    await db.commit()
    return {"task_id": task_id, "test_cases": new_test_cases}


@router.post("/lessons/{lesson_id}/regenerate")
async def regenerate_lesson_task(
    lesson_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate a new task for a specific lesson (replaces existing one)."""
    from app.services.lesson_service import LessonService
    from fastapi import HTTPException
    
    lesson_service = LessonService(db)
    
    # Get lesson to get topic and difficulty
    lesson = await lesson_service.lesson_repo.get_lesson_by_id(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Урок не найден")
    
    # Get previous topics for curriculum context
    prev_topics = await lesson_service.lesson_repo.get_previous_topics(lesson_id)

    # Generate new task
    task_service = TaskService(db)
    new_task = await task_service.generate_ai_task(
        topic=lesson.topic,
        difficulty="easy",
        lesson_id=lesson_id,
        lesson_title=lesson.title,
        prev_topics=prev_topics,
    )
    
    return new_task
