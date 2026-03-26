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
        order_by: str = "id_asc",
    ) -> List[Task]:
        """Get tasks with optional filters."""
        from sqlalchemy import desc
        
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
        
        # Sorting
        if order_by == "id_desc":
            query = query.order_by(desc(Task.id))
        else:  # default "id_asc"
            query = query.order_by(Task.id)
        
        query = query.limit(limit).offset(offset)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update(self, task_id: int, **kwargs) -> Optional[Task]:
        """Update task fields."""
        task = await self.get_by_id(task_id)
        if not task:
            return None
        for key, value in kwargs.items():
            setattr(task, key, value)
        await self.db.flush()
        await self.db.refresh(task)
        return task

    async def delete_by_lesson_id(self, lesson_id: int) -> int:
        """Delete all tasks for a lesson. Returns count deleted."""
        from sqlalchemy import delete
        result = await self.db.execute(
            delete(Task).where(Task.lesson_id == lesson_id)
        )
        return result.rowcount

    async def create(self, **kwargs) -> Task:
        """Create a new task."""
        task = Task(**kwargs)
        self.db.add(task)
        await self.db.flush()
        await self.db.refresh(task)
        return task
