"""
Task service - manages coding tasks and submissions.
"""
import json
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.task_repository import TaskRepository
from app.repositories.submission_repository import SubmissionRepository
from app.repositories.progress_repository import ProgressRepository
from app.repositories.user_repository import UserRepository
from app.services.ai_service import ai_service
from app.services.sandbox_service import sandbox_service
from app.services.achievement_service import AchievementService


class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.task_repo = TaskRepository(db)
        self.submission_repo = SubmissionRepository(db)
        self.progress_repo = ProgressRepository(db)
        self.user_repo = UserRepository(db)
        self.achievement_service = AchievementService(db)

    async def submit_solution(self, user_id: int, task_id: int, code: str) -> dict:
        """
        Process a code submission:
        1. Create submission record
        2. Run code in sandbox
        3. Check against test cases
        4. Analyze with AI
        5. Award XP and check achievements
        """
        # Create submission
        submission = await self.submission_repo.create(user_id, task_id, code)

        # Get task details
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            return {"error": "Задача не найдена"}

        test_cases = json.loads(task.test_cases) if task.test_cases else []

        # Run tests in sandbox
        test_results = await sandbox_service.run_tests(code, test_cases)

        is_correct = test_results["all_passed"]
        execution_time = test_results.get("execution_time_ms")

        # Get execution error if any
        error_msg = None
        if test_results["results"]:
            first_error = next(
                (r["error"] for r in test_results["results"] if r.get("error")),
                None
            )
            error_msg = first_error

        # AI analysis
        ai_result = await ai_service.analyze_code(
            code=code,
            task_description=task.description,
            is_correct=is_correct,
            execution_time_ms=execution_time,
            error=error_msg,
        )

        # Update submission
        await self.submission_repo.update_result(
            submission.id,
            is_correct=is_correct,
            execution_time_ms=execution_time,
            output=str(test_results["results"]),
            error=error_msg,
            ai_feedback=ai_result.get("feedback", ""),
            ai_score=float(ai_result.get("score", 0)),
        )

        # Award XP for correct solution
        xp_earned = 0
        if is_correct:
            xp_map = {"easy": 50, "medium": 100, "hard": 200}
            xp = xp_map.get(task.difficulty.value if hasattr(task.difficulty, 'value') else str(task.difficulty), 50)
            await self.user_repo.update_xp(user_id, xp)
            xp_earned = xp

        # Update progress if task belongs to lesson
        if task.lesson_id:
            lesson_tasks = await self.task_repo.get_filtered(lesson_id=task.lesson_id)

            # Count correct tasks for this lesson
            lesson_correct = 0
            for lt in lesson_tasks:
                subs = await self.submission_repo.get_user_submissions(user_id, lt.id)
                if any(s.is_correct for s in subs):
                    lesson_correct += 1

            await self.progress_repo.update_task_completion(
                user_id, task.lesson_id, lesson_correct, len(lesson_tasks)
            )

        # Check achievements
        new_achievements = await self.achievement_service.check_and_award(user_id)

        return {
            "submission_id": submission.id,
            "is_correct": is_correct,
            "execution_time_ms": execution_time,
            "passed_tests": test_results["passed"],
            "total_tests": test_results["total"],
            "test_results": test_results["results"],
            "ai_feedback": ai_result.get("feedback", ""),
            "ai_score": float(ai_result.get("score", 0)),
            "recommendations": ai_result.get("recommendations", []),
            "new_achievements": new_achievements,
            "xp_earned": xp_earned,
        }

    async def generate_ai_task(
        self,
        topic: str,
        difficulty: str,
        lesson_id: int = None,
        lesson_title: str = None,
        prev_topics: list = None,
    ) -> dict:
        """Generate a new task using AI and save to database."""
        task_data = await ai_service.generate_task(
            topic, difficulty, lesson_title or topic, prev_topics=prev_topics
        )

        import re
        slug = re.sub(r'[^a-z0-9-]', '-', task_data["title"].lower()[:50])
        slug = f"{slug}-{difficulty}"

        # Ensure unique slug
        existing = await self.task_repo.get_by_slug(slug)
        if existing:
            import time
            slug = f"{slug}-{int(time.time())}"

        task = await self.task_repo.create(
            lesson_id=lesson_id,
            title=task_data["title"],
            slug=slug,
            description=task_data["description"],
            difficulty=difficulty,
            category=task_data.get("category", topic),
            hints=json.dumps(task_data.get("hints", []), ensure_ascii=False),
            test_cases=json.dumps(task_data.get("test_cases", []), ensure_ascii=False),
            solution_template=task_data.get("solution_template", "# Напишите решение здесь\n"),
        )

        return {
            "id": task.id,
            "title": task.title,
            "slug": task.slug,
            "description": task.description,
            "difficulty": task.difficulty,
            "category": task.category,
            "hints": json.loads(task.hints) if task.hints else [],
            "test_cases": json.loads(task.test_cases) if task.test_cases else [],
            "solution_template": task.solution_template,
        }
