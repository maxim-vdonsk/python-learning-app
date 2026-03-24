"""
Task repository - database operations for Task model.
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.models.task import Task, DifficultyEnum


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        result = await self.db.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Optional[Task]:
        """Get task by slug."""
        result = await self.db.execute(select(Task).where(Task.slug == slug))
        return result.scalar_one_or_none()

    async def get_filtered(
        self,
        difficulty: Optional[str] = None,
        category: Optional[str] = None,
        lesson_id: Optional[int] = None,
        search: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Task]:
        """Get tasks with optional filters."""
        query = select(Task)
        if difficulty:
            query = query.where(Task.difficulty == difficulty)
        if category:
            query = query.where(Task.category == category)
        if lesson_id:
            query = query.where(Task.lesson_id == lesson_id)
        if search:
            query = query.where(
                or_(Task.title.ilike(f"%{search}%"), Task.description.ilike(f"%{search}%"))
            )
        query = query.limit(limit).offset(offset)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, **kwargs) -> Task:
        """Create a new task."""
        task = Task(**kwargs)
        self.db.add(task)
        await self.db.flush()
        await self.db.refresh(task)
        return task
