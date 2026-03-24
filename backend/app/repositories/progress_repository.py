"""
Progress repository - database operations for Progress model.
"""
from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.progress import Progress


class ProgressRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create(self, user_id: int, lesson_id: int) -> Progress:
        """Get or create a progress entry for user+lesson."""
        result = await self.db.execute(
            select(Progress).where(
                Progress.user_id == user_id,
                Progress.lesson_id == lesson_id
            )
        )
        progress = result.scalar_one_or_none()
        if not progress:
            progress = Progress(user_id=user_id, lesson_id=lesson_id)
            self.db.add(progress)
            await self.db.flush()
        return progress

    async def get_user_progress(self, user_id: int) -> List[Progress]:
        """Get all progress entries for a user."""
        result = await self.db.execute(
            select(Progress).where(Progress.user_id == user_id)
        )
        return result.scalars().all()

    async def mark_theory_read(self, user_id: int, lesson_id: int) -> Progress:
        """Mark theory as read for a lesson."""
        progress = await self.get_or_create(user_id, lesson_id)
        progress.theory_read = True
        await self.db.flush()
        return progress

    async def update_task_completion(self, user_id: int, lesson_id: int, tasks_done: int, total: int) -> None:
        """Update task completion counts."""
        progress = await self.get_or_create(user_id, lesson_id)
        progress.tasks_completed = tasks_done
        progress.total_tasks = total
        if tasks_done >= total and total > 0:
            progress.completed = True
            progress.completed_at = datetime.utcnow()
        await self.db.flush()
