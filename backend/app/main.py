"""
Main FastAPI application entry point.
Configures middleware, routers, and startup events.
"""
import asyncio
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import auth, lessons, tasks, progress, submissions, achievements

logger = logging.getLogger(__name__)


async def ensure_database_exists(retries: int = 10, delay: float = 2.0) -> None:
    """
    Подключается к служебной БД 'postgres' и создаёт 'python_learning' если её нет.
    Повторяет попытки пока PostgreSQL не будет готов.
    """
    import asyncpg
    from urllib.parse import urlparse

    # Парсим DATABASE_URL: postgresql+asyncpg://user:pass@host:port/dbname
    raw = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    parsed = urlparse(raw)
    db_name = parsed.path.lstrip("/")
    host = parsed.hostname or "db"
    port = parsed.port or 5432
    user = parsed.username or "postgres"
    password = parsed.password or "postgres"

    for attempt in range(1, retries + 1):
        try:
            conn = await asyncpg.connect(
                host=host, port=port, user=user, password=password,
                database="postgres",   # всегда существует
            )
            try:
                exists = await conn.fetchval(
                    "SELECT 1 FROM pg_database WHERE datname = $1", db_name
                )
                if not exists:
                    await conn.execute(f'CREATE DATABASE "{db_name}"')
                    logger.info(f"База данных '{db_name}' создана.")
                else:
                    logger.info(f"База данных '{db_name}' уже существует.")
            finally:
                await conn.close()
            return  # успех
        except Exception as exc:
            logger.warning(f"Попытка {attempt}/{retries}: PostgreSQL не готов — {exc}")
            if attempt < retries:
                await asyncio.sleep(delay)

    raise RuntimeError("PostgreSQL недоступен после всех попыток подключения.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: ensure DB exists, then create tables."""
    await ensure_database_exists()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Python Learning Platform",
    description="Production-ready Python learning platform with AI-powered lessons",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(lessons.router, prefix="/api/v1/lessons", tags=["Lessons"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Tasks"])
app.include_router(progress.router, prefix="/api/v1/progress", tags=["Progress"])
app.include_router(submissions.router, prefix="/api/v1/submissions", tags=["Submissions"])
app.include_router(achievements.router, prefix="/api/v1/achievements", tags=["Achievements"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": "1.0.0"}
