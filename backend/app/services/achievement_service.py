"""
Achievement service - checks and awards achievements.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.achievement import Achievement, UserAchievement
from app.repositories.user_repository import UserRepository
from app.repositories.progress_repository import ProgressRepository
from app.repositories.submission_repository import SubmissionRepository


# Default achievements to seed
DEFAULT_ACHIEVEMENTS = [
    {"name": "first_lesson", "title": "Первый шаг", "description": "Завершил первый урок",
     "icon": "🎯", "xp_reward": 50, "condition_type": "lessons_completed", "condition_value": 1},
    {"name": "week_one", "title": "Неделя пройдена", "description": "Завершил 7 уроков",
     "icon": "📅", "xp_reward": 100, "condition_type": "lessons_completed", "condition_value": 7},
    {"name": "streak_3", "title": "3 дня подряд", "description": "Занимался 3 дня подряд",
     "icon": "🔥", "xp_reward": 75, "condition_type": "streak", "condition_value": 3},
    {"name": "streak_7", "title": "Недельная серия", "description": "Занимался 7 дней подряд",
     "icon": "⚡", "xp_reward": 200, "condition_type": "streak", "condition_value": 7},
    {"name": "streak_30", "title": "Месяц упорства", "description": "Занимался 30 дней подряд",
     "icon": "💎", "xp_reward": 500, "condition_type": "streak", "condition_value": 30},
    {"name": "solver_10", "title": "Решатель", "description": "Решил 10 задач",
     "icon": "🧩", "xp_reward": 150, "condition_type": "submissions_correct", "condition_value": 10},
    {"name": "solver_50", "title": "Мастер задач", "description": "Решил 50 задач",
     "icon": "🏆", "xp_reward": 400, "condition_type": "submissions_correct", "condition_value": 50},
    {"name": "graduate", "title": "Выпускник", "description": "Завершил весь курс",
     "icon": "🎓", "xp_reward": 1000, "condition_type": "lessons_completed", "condition_value": 48},
]


class AchievementService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.progress_repo = ProgressRepository(db)
        self.submission_repo = SubmissionRepository(db)

    async def seed_achievements(self) -> None:
        """Seed default achievements into the database."""
        for ach_data in DEFAULT_ACHIEVEMENTS:
            result = await self.db.execute(
                select(Achievement).where(Achievement.name == ach_data["name"])
            )
            if not result.scalar_one_or_none():
                achievement = Achievement(**ach_data)
                self.db.add(achievement)
        await self.db.flush()

    async def check_and_award(self, user_id: int) -> list:
        """Check all achievements and award newly earned ones."""
        user = await self.user_repo.get_by_id(user_id)
        user_progress = await self.progress_repo.get_user_progress(user_id)
        correct_submissions = await self.submission_repo.count_correct_by_user(user_id)
        completed_lessons = sum(1 for p in user_progress if p.completed)

        # Get all achievements
        all_achievements = (await self.db.execute(select(Achievement))).scalars().all()

        # Get already earned achievement IDs
        earned = (await self.db.execute(
            select(UserAchievement).where(UserAchievement.user_id == user_id)
        )).scalars().all()
        earned_ids = {ua.achievement_id for ua in earned}

        new_achievements = []

        for achievement in all_achievements:
            if achievement.id in earned_ids:
                continue

            earned_it = False
            ctype = achievement.condition_type
            cval = achievement.condition_value

            if ctype == "lessons_completed" and completed_lessons >= cval:
                earned_it = True
            elif ctype == "streak" and user.streak_days >= cval:
                earned_it = True
            elif ctype == "submissions_correct" and correct_submissions >= cval:
                earned_it = True

            if earned_it:
                ua = UserAchievement(user_id=user_id, achievement_id=achievement.id)
                self.db.add(ua)
                await self.user_repo.update_xp(user_id, achievement.xp_reward)
                new_achievements.append({
                    "name": achievement.name,
                    "title": achievement.title,
                    "icon": achievement.icon,
                    "xp_reward": achievement.xp_reward,
                })

        await self.db.flush()
        return new_achievements

    async def get_user_achievements(self, user_id: int) -> list:
        """Get all achievements for a user."""
        result = await self.db.execute(
            select(UserAchievement)
            .where(UserAchievement.user_id == user_id)
        )
        user_achievements = result.scalars().all()

        output = []
        for ua in user_achievements:
            ach_result = await self.db.execute(
                select(Achievement).where(Achievement.id == ua.achievement_id)
            )
            ach = ach_result.scalar_one_or_none()
            if ach:
                output.append({
                    "id": ach.id,
                    "name": ach.name,
                    "title": ach.title,
                    "description": ach.description,
                    "icon": ach.icon,
                    "xp_reward": ach.xp_reward,
                    "earned_at": ua.earned_at.isoformat(),
                })
        return output
