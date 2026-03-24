"""
User repository - database operations for User model.
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, email: str, username: str, hashed_password: str) -> User:
        """Create a new user."""
        user = User(email=email, username=username, hashed_password=hashed_password)
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def update_xp(self, user_id: int, xp_delta: int) -> None:
        """Add XP points to user and recalculate level."""
        user = await self.get_by_id(user_id)
        if user:
            user.xp_points += xp_delta
            # Level up every 500 XP
            user.level = (user.xp_points // 500) + 1
            await self.db.flush()

    async def update_streak(self, user_id: int, streak: int) -> None:
        """Update user streak days."""
        await self.db.execute(
            update(User).where(User.id == user_id).values(streak_days=streak)
        )

    async def get_leaderboard(self, limit: int = 10) -> List[User]:
        """Get top users by XP."""
        result = await self.db.execute(
            select(User).order_by(User.xp_points.desc()).limit(limit)
        )
        return result.scalars().all()
