"""
Pydantic schemas for Achievement endpoints.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AchievementOut(BaseModel):
    id: int
    name: str
    title: str
    description: str
    icon: str
    xp_reward: int
    condition_type: str
    condition_value: int

    class Config:
        from_attributes = True


class UserAchievementOut(BaseModel):
    achievement: AchievementOut
    earned_at: datetime

    class Config:
        from_attributes = True
