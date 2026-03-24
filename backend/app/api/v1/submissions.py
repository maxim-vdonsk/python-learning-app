"""
Submissions API endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.submission import SubmissionCreate
from app.services.task_service import TaskService
from app.repositories.submission_repository import SubmissionRepository

router = APIRouter()


@router.post("/")
async def submit_code(
    submission: SubmissionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit code for a task and get results."""
    service = TaskService(db)
    return await service.submit_solution(current_user.id, submission.task_id, submission.code)


@router.get("/my")
async def get_my_submissions(
    task_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's submissions."""
    repo = SubmissionRepository(db)
    submissions = await repo.get_user_submissions(current_user.id, task_id)
    return [
        {
            "id": s.id,
            "task_id": s.task_id,
            "is_correct": s.is_correct,
            "execution_time_ms": s.execution_time_ms,
            "ai_score": s.ai_score,
            "status": s.status,
            "created_at": s.created_at.isoformat(),
        }
        for s in submissions
    ]
