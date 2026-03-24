"""
Progress service - tracks and calculates user learning progress.
"""
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.progress_repository import ProgressRepository
from app.repositories.user_repository import UserRepository
from app.repositories.lesson_repository import LessonRepository
from app.services.ai_service import ai_service


class ProgressService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.progress_repo = ProgressRepository(db)
        self.user_repo = UserRepository(db)
        self.lesson_repo = LessonRepository(db)

    async def get_dashboard_stats(self, user_id: int) -> dict:
        """Get comprehensive dashboard statistics for a user."""
        user = await self.user_repo.get_by_id(user_id)
        user_progress = await self.progress_repo.get_user_progress(user_id)
        all_weeks = await self.lesson_repo.get_all_weeks()

        # Count total lessons
        total_lessons = sum(len(week.lessons) for week in all_weeks)
        completed_lessons = sum(1 for p in user_progress if p.completed)

        completion_pct = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0

        # Update streak
        today = date.today()
        last_activity = user.last_activity_date.date() if user.last_activity_date else None

        stats = {
            "total_lessons": total_lessons,
            "completed_lessons": completed_lessons,
            "completion_percentage": round(completion_pct, 1),
            "current_streak": user.streak_days,
            "total_xp": user.xp_points,
            "level": user.level,
            "rating": user.rating,
            "streak": user.streak_days,
        }

        # Generate motivation phrase
        motivation = await ai_service.generate_motivation(user.username, stats)
        stats["motivation_phrase"] = motivation

        return stats

    async def update_streak(self, user_id: int) -> None:
        """Update user's daily streak."""
        user = await self.user_repo.get_by_id(user_id)
        today = date.today()

        if user.last_activity_date:
            last = user.last_activity_date.date()
            delta = (today - last).days

            if delta == 1:
                # Consecutive day - increase streak
                user.streak_days += 1
            elif delta > 1:
                # Streak broken
                user.streak_days = 1
            # delta == 0: same day, no change
        else:
            user.streak_days = 1

        user.last_activity_date = datetime.utcnow()
        await self.db.flush()
