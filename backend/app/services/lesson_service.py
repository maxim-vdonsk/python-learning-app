"""
Lesson service - business logic for lessons and theory generation.
"""
import json
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.lesson_repository import LessonRepository
from app.repositories.progress_repository import ProgressRepository
from app.services.ai_service import ai_service
from app.data.course_structure import COURSE_STRUCTURE


class LessonService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.lesson_repo = LessonRepository(db)
        self.progress_repo = ProgressRepository(db)

    async def get_course(self, user_id: int) -> list:
        """Get full course structure with user progress."""
        weeks = await self.lesson_repo.get_all_weeks()
        user_progress = await self.progress_repo.get_user_progress(user_id)

        # Map progress by lesson_id
        progress_map = {p.lesson_id: p for p in user_progress}

        result = []
        for week in weeks:
            lessons_data = []
            for lesson in week.lessons:
                prog = progress_map.get(lesson.id)
                lessons_data.append({
                    "id": lesson.id,
                    "title": lesson.title,
                    "slug": lesson.slug,
                    "description": lesson.description,
                    "topic": lesson.topic,
                    "order": lesson.order,
                    "completed": prog.completed if prog else False,
                    "theory_read": prog.theory_read if prog else False,
                    "tasks_completed": prog.tasks_completed if prog else 0,
                    "total_tasks": prog.total_tasks if prog else 0,
                })

            result.append({
                "id": week.id,
                "number": week.number,
                "title": week.title,
                "description": week.description,
                "lessons": lessons_data,
            })

        return result

    async def get_lesson_theory(self, lesson_id: int, user_id: int, regenerate: bool = False) -> dict:
        """Get theory for a lesson, generating via AI if needed."""
        lesson = await self.lesson_repo.get_lesson_by_id(lesson_id)
        if not lesson:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Урок не найден")

        # Generate theory if not cached or regenerate requested
        if not lesson.theory_content or regenerate:
            ai_data = await ai_service.generate_theory(lesson.topic, lesson.title)
            theory = ai_data.get("theory", "")
            examples = json.dumps(ai_data.get("examples", []), ensure_ascii=False)
            await self.lesson_repo.update_theory(lesson_id, theory, examples)
            lesson.theory_content = theory
            lesson.code_examples = examples

        # Mark theory as read
        await self.progress_repo.mark_theory_read(user_id, lesson_id)

        return {
            "lesson_id": lesson.id,
            "title": lesson.title,
            "theory": lesson.theory_content,
            "examples": json.loads(lesson.code_examples) if lesson.code_examples else [],
        }

    async def initialize_course(self) -> None:
        """Seed the database with the course structure if empty."""
        existing = await self.lesson_repo.get_all_weeks()
        if existing:
            return  # Already initialized

        for week_data in COURSE_STRUCTURE:
            week = await self.lesson_repo.create_week(
                number=week_data["number"],
                title=week_data["title"],
                description=week_data["description"],
            )
            for lesson_data in week_data["lessons"]:
                await self.lesson_repo.create_lesson(
                    week_id=week.id,
                    title=lesson_data["title"],
                    slug=lesson_data["slug"],
                    topic=lesson_data["topic"],
                    order=lesson_data["order"],
                    description=lesson_data.get("description", ""),
                )
