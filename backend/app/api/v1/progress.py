"""
Progress API endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.progress_service import ProgressService
from app.repositories.user_repository import UserRepository

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get dashboard statistics for current user."""
    service = ProgressService(db)
    return await service.get_dashboard_stats(current_user.id)


@router.get("/leaderboard")
async def get_leaderboard(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get top users by XP."""
    repo = UserRepository(db)
    users = await repo.get_leaderboard(limit)
    return [
        {
            "rank": i + 1,
            "username": u.username,
            "xp_points": u.xp_points,
            "level": u.level,
            "streak_days": u.streak_days,
        }
        for i, u in enumerate(users)
    ]
