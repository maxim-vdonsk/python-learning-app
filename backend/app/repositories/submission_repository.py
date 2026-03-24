"""
Submission repository - database operations for Submission model.
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.submission import Submission


class SubmissionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int, task_id: int, code: str) -> Submission:
        """Create a new submission."""
        submission = Submission(user_id=user_id, task_id=task_id, code=code, status="pending")
        self.db.add(submission)
        await self.db.flush()
        await self.db.refresh(submission)
        return submission

    async def update_result(self, submission_id: int, **kwargs) -> Optional[Submission]:
        """Update submission with execution results."""
        result = await self.db.execute(
            select(Submission).where(Submission.id == submission_id)
        )
        submission = result.scalar_one_or_none()
        if submission:
            for key, value in kwargs.items():
                setattr(submission, key, value)
            submission.status = "completed"
            await self.db.flush()
        return submission

    async def get_user_submissions(self, user_id: int, task_id: Optional[int] = None) -> List[Submission]:
        """Get all submissions for a user, optionally filtered by task."""
        query = select(Submission).where(Submission.user_id == user_id)
        if task_id:
            query = query.where(Submission.task_id == task_id)
        query = query.order_by(Submission.created_at.desc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def count_correct_by_user(self, user_id: int) -> int:
        """Count correct submissions for a user."""
        from sqlalchemy import func
        result = await self.db.execute(
            select(func.count(Submission.id)).where(
                Submission.user_id == user_id,
                Submission.is_correct == True
            )
        )
        return result.scalar() or 0
