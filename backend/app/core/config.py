"""
Application configuration using Pydantic settings.
Loads from environment variables.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Python Learning Platform"
    DEBUG: bool = False
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/python_learning"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://frontend:3000"]

    # Docker sandbox
    SANDBOX_IMAGE: str = "python:3.11-alpine"
    SANDBOX_TIMEOUT: int = 10  # seconds
    SANDBOX_MEM_LIMIT: str = "64m"
    SANDBOX_CPU_QUOTA: int = 50000  # 50% CPU

    # gpt4free
    GPT4FREE_PROVIDER: str = "auto"  # auto-select best available provider
    GPT4FREE_MODEL: str = "gpt-4o-mini"

    # SMTP Email
    SMTP_HOST: str = ""
    SMTP_PORT: int = 465
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_NAME: str = "PyNeon Platform"
    SMTP_TLS: bool = True  # True = SMTP_SSL (465), False = STARTTLS (587)

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
