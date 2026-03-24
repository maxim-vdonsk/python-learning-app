"""
Lesson repository - database operations for Lesson and Week models.
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.lesson import Lesson, Week


class LessonRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_weeks(self) -> List[Week]:
        """Get all weeks with their lessons."""
        result = await self.db.execute(
            select(Week).options(selectinload(Week.lessons)).order_by(Week.number)
        )
        return result.scalars().all()

    async def get_lesson_by_id(self, lesson_id: int) -> Optional[Lesson]:
        """Get a lesson by ID."""
        result = await self.db.execute(
            select(Lesson).where(Lesson.id == lesson_id)
        )
        return result.scalar_one_or_none()

    async def get_lesson_by_slug(self, slug: str) -> Optional[Lesson]:
        """Get a lesson by slug."""
        result = await self.db.execute(
            select(Lesson).where(Lesson.slug == slug)
        )
        return result.scalar_one_or_none()

    async def get_lessons_by_week(self, week_id: int) -> List[Lesson]:
        """Get all lessons for a specific week."""
        result = await self.db.execute(
            select(Lesson).where(Lesson.week_id == week_id).order_by(Lesson.order)
        )
        return result.scalars().all()

    async def get_previous_topics(self, lesson_id: int) -> List[str]:
        """
        Возвращает список topic всех уроков, идущих ДО текущего
        (по week_id + order). Используется для составления задачи
        с учётом уже пройденного материала.
        """
        current = await self.get_lesson_by_id(lesson_id)
        if not current:
            return []

        result = await self.db.execute(
            select(Lesson.topic, Lesson.title).where(
                (Lesson.week_id < current.week_id) |
                (
                    (Lesson.week_id == current.week_id) &
                    (Lesson.order < current.order)
                )
            ).order_by(Lesson.week_id, Lesson.order)
        )
        rows = result.all()
        # Убираем дубли topic, сохраняем порядок
        seen = set()
        topics = []
        for topic, title in rows:
            if topic not in seen:
                seen.add(topic)
                topics.append(f"{topic} ({title})")
        return topics

    async def update_theory(self, lesson_id: int, theory: str, examples: str) -> None:
        """Update lesson theory content."""
        lesson = await self.get_lesson_by_id(lesson_id)
        if lesson:
            lesson.theory_content = theory
            lesson.code_examples = examples
            await self.db.flush()

    async def create_week(self, number: int, title: str, description: str) -> Week:
        """Create a new week."""
        week = Week(number=number, title=title, description=description)
        self.db.add(week)
        await self.db.flush()
        return week

    async def create_lesson(self, week_id: int, title: str, slug: str,
                             topic: str, order: int, description: str = "") -> Lesson:
        """Create a new lesson."""
        lesson = Lesson(
            week_id=week_id, title=title, slug=slug,
            topic=topic, order=order, description=description
        )
        self.db.add(lesson)
        await self.db.flush()
        return lesson
