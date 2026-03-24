"""
Achievements API endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.achievement_service import AchievementService

router = APIRouter()


@router.get("/")
async def get_my_achievements(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all achievements for current user."""
    service = AchievementService(db)
    return await service.get_user_achievements(current_user.id)


@router.get("/all")
async def get_all_achievements(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all available achievements."""
    from sqlalchemy import select
    from app.models.achievement import Achievement
    result = await db.execute(select(Achievement))
    achievements = result.scalars().all()
    return [
        {
            "id": a.id,
            "name": a.name,
            "title": a.title,
            "description": a.description,
            "icon": a.icon,
            "xp_reward": a.xp_reward,
            "condition_type": a.condition_type,
            "condition_value": a.condition_value,
        }
        for a in achievements
    ]


@router.post("/seed")
async def seed_achievements(db: AsyncSession = Depends(get_db)):
    """Seed default achievements (run once on setup)."""
    service = AchievementService(db)
    await service.seed_achievements()
    return {"message": "Achievements seeded"}
