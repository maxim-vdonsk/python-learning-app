"""
Lesson service - business logic for lessons and theory generation.
"""
import json
import re
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.lesson_repository import LessonRepository
from app.repositories.progress_repository import ProgressRepository
from app.repositories.task_repository import TaskRepository
from app.services.ai_service import ai_service
from app.services.achievement_service import AchievementService
from app.services.progress_service import ProgressService
from app.data.course_structure import COURSE_STRUCTURE


def _is_ai_error(text: str) -> bool:
    """Возвращает True если текст — сообщение об ошибке AI, а не реальный контент."""
    return not text or text.startswith("[AI недоступен]")


class LessonService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.lesson_repo = LessonRepository(db)
        self.progress_repo = ProgressRepository(db)
        self.achievement_service = AchievementService(db)
        self.progress_service = ProgressService(db)

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

        # Generate theory if not cached (or forced regenerate)
        # Не перезаписываем кеш если уже есть валидный контент
        needs_generate = (
            regenerate
            or not lesson.theory_content
            or _is_ai_error(lesson.theory_content)
        )
        if needs_generate:
            ai_data = await ai_service.generate_theory(lesson.topic, lesson.title)
            theory = ai_data.get("theory", "")
            examples = json.dumps(ai_data.get("examples", []), ensure_ascii=False)
            # Сохраняем только если AI вернул реальный контент
            if not _is_ai_error(theory):
                await self.lesson_repo.update_theory(lesson_id, theory, examples)
                lesson.theory_content = theory
                lesson.code_examples = examples

        # Mark theory as read
        await self.progress_repo.mark_theory_read(user_id, lesson_id)

        # Update streak and check achievements on theory read
        await self.progress_service.update_streak(user_id)
        await self.achievement_service.check_and_award(user_id)

        return {
            "lesson_id": lesson.id,
            "title": lesson.title,
            "theory": lesson.theory_content,
            "examples": json.loads(lesson.code_examples) if lesson.code_examples else [],
        }

    async def get_or_create_lesson_task(self, lesson_id: int) -> dict:
        """
        Возвращает существующее задание для урока или генерирует новое (один раз).
        Повторные вызовы всегда вернут то же самое задание.
        """
        from fastapi import HTTPException

        lesson = await self.lesson_repo.get_lesson_by_id(lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Урок не найден")

        task_repo = TaskRepository(self.db)

        # Ищем существующее задание для этого урока (последнее созданное)
        existing = await task_repo.get_filtered(lesson_id=lesson_id, limit=1, order_by="id_desc")
        if existing:
            t = existing[0]
            return {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "difficulty": t.difficulty,
                "category": t.category,
                "hints": json.loads(t.hints) if t.hints else [],
                "test_cases": json.loads(t.test_cases) if t.test_cases else [],
                "solution_template": t.solution_template,
            }

        # Получаем список уже пройденных тем для контекста
        prev_topics = await self.lesson_repo.get_previous_topics(lesson_id)

        # Генерируем задание с учётом пройденного материала
        task_data = await ai_service.generate_task(
            lesson.topic, "easy", lesson.title, prev_topics=prev_topics
        )

        # Если AI вернул ошибку — возвращаем заглушку без сохранения в БД
        if _is_ai_error(task_data.get("description", "")):
            return {
                "id": None,
                "title": f"Задача по теме: {lesson.title}",
                "description": (
                    f"Напишите программу на Python по теме «{lesson.title}».\n\n"
                    "Задача временно недоступна. Попробуйте позже или напишите "
                    "любой код связанный с темой урока."
                ),
                "difficulty": "easy",
                "category": lesson.topic,
                "hints": ["Используй знания из теоретической части"],
                "test_cases": [],
                "solution_template": "# Напишите решение здесь\n",
            }

        # Сохраняем в БД с привязкой к уроку
        slug = re.sub(r'[^a-z0-9-]', '-', task_data["title"].lower()[:50])
        slug = f"{slug}-lesson-{lesson_id}"
        existing_slug = await task_repo.get_by_slug(slug)
        if existing_slug:
            import time
            slug = f"{slug}-{int(time.time())}"

        task = await task_repo.create(
            lesson_id=lesson_id,
            title=task_data["title"],
            slug=slug,
            description=task_data["description"],
            difficulty="easy",
            category=task_data.get("category", lesson.topic),
            hints=json.dumps(task_data.get("hints", []), ensure_ascii=False),
            test_cases=json.dumps(task_data.get("test_cases", []), ensure_ascii=False),
            solution_template=task_data.get("solution_template", "# Напишите решение здесь\n"),
        )

        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "difficulty": task.difficulty,
            "category": task.category,
            "hints": json.loads(task.hints) if task.hints else [],
            "test_cases": json.loads(task.test_cases) if task.test_cases else [],
            "solution_template": task.solution_template,
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
