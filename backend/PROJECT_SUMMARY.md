# Python Learning Platform - Backend

A production-ready FastAPI backend for an AI-powered Python learning application with code sandbox execution and achievement system.

## Project Structure

### Core Directories
- **app/** - Main application package
  - **main.py** - FastAPI application entry point with lifespan management and CORS middleware
  - **core/** - Configuration and infrastructure
    - config.py - Pydantic settings with environment variables
    - database.py - Async SQLAlchemy setup with AsyncSession
    - security.py - JWT authentication, password hashing, OAuth2 dependencies
  - **api/v1/** - REST API endpoints
    - auth.py - Registration and login endpoints
    - lessons.py - Course and theory endpoints
    - tasks.py - Task management and filtering
    - submissions.py - Code submission handling
    - progress.py - Dashboard and leaderboard
    - achievements.py - Achievement tracking
  - **models/** - SQLAlchemy ORM models
    - user.py - User with gamification fields (XP, level, streak)
    - lesson.py - Lesson and Week models with course structure
    - task.py - Coding tasks with difficulty and test cases
    - progress.py - User progress tracking per lesson
    - submission.py - Code submissions with execution results
    - achievement.py - Achievements and user achievements
  - **schemas/** - Pydantic validation schemas
    - user.py, lesson.py, task.py, submission.py, progress.py, achievement.py
  - **repositories/** - Data access layer
    - user_repository.py - User queries and updates
    - lesson_repository.py - Lesson and week management
    - task_repository.py - Task filtering and creation
    - progress_repository.py - Progress tracking
    - submission_repository.py - Submission storage
  - **services/** - Business logic
    - ai_service.py - gpt4free integration for content generation and code analysis
    - sandbox_service.py - Docker-based code execution with resource limits
    - auth_service.py - User registration and authentication
    - lesson_service.py - Course initialization and theory generation
    - task_service.py - Task submission and evaluation pipeline
    - progress_service.py - Dashboard stats and streak tracking
    - achievement_service.py - Achievement checking and awarding
  - **data/** - Static course content
    - course_structure.py - 12-week curriculum with 48 lessons

### Configuration Files
- **requirements.txt** - Python dependencies (FastAPI, SQLAlchemy, Docker, gpt4free, etc.)
- **Dockerfile** - Container image based on Python 3.11-slim
- **alembic/** - Database migration setup
  - env.py - Async migration configuration
  - alembic.ini - Migration settings
- **.env.example** - Environment variable template

## Key Features

### Authentication
- JWT token-based authentication
- Password hashing with bcrypt
- OAuth2 with Bearer tokens
- User registration with email validation

### Course Management
- 12-week structured curriculum
- 48 lessons organized in weeks
- AI-powered theory generation with caching
- Progress tracking per lesson
- Task completion monitoring

### Code Execution
- Sandboxed Python execution in Docker containers
- CPU and memory limits enforcement
- Configurable timeout handling
- Fallback execution without Docker
- Test case validation with flexible output matching

### AI Integration (gpt4free)
- Lesson theory generation with examples
- Task generation with test cases
- Code submission analysis and feedback
- Personalized motivation phrases
- Retry logic with exponential backoff

### Gamification
- XP points system (50-200 per task)
- Level progression (1 level per 500 XP)
- Daily streak tracking
- Leaderboard by XP
- 8 achievement types with conditions

### API Endpoints
- /api/v1/auth - Registration, login
- /api/v1/lessons - Course structure, theory generation
- /api/v1/tasks - Task browsing, filtering, generation
- /api/v1/submissions - Code submission and evaluation
- /api/v1/progress - Dashboard stats, leaderboard
- /api/v1/achievements - User achievements, all achievements

## Setup Instructions

### Prerequisites
- Python 3.11+
- PostgreSQL with asyncpg
- Docker (for code sandbox)
- gpt4free providers available

### Installation
```bash
pip install -r requirements.txt
cp .env.example .env
```

### Environment Setup
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/python_learning
SECRET_KEY=your-secret-key-here
DEBUG=false
SANDBOX_IMAGE=python:3.11-alpine
SANDBOX_TIMEOUT=10
GPT4FREE_MODEL=gpt-4o-mini
```

### Database Initialization
```bash
# Using SQLAlchemy lifespan (automatic on startup)
# Or with Alembic:
alembic upgrade head
```

### Running the Application
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Initialize Course
```bash
# POST /api/v1/lessons/initialize
# POST /api/v1/achievements/seed
```

## Technology Stack
- **Framework**: FastAPI 0.115.0
- **Database**: PostgreSQL with SQLAlchemy 2.0.36 (async)
- **Auth**: python-jose + passlib
- **Code Execution**: Docker + asyncio subprocess fallback
- **AI**: gpt4free with AsyncClient
- **Validation**: Pydantic 2.9.2
- **Server**: Uvicorn

## Architecture Notes

### Layered Architecture
1. **API Layer** (api/v1/*) - HTTP request handling
2. **Service Layer** (services/*) - Business logic
3. **Repository Layer** (repositories/*) - Data access
4. **Model Layer** (models/*) - Database schema
5. **Core Layer** (core/*) - Infrastructure (DB, auth, config)

### Async-First Design
- All database operations use async/await
- Code execution runs in asyncio
- AI service uses AsyncClient for gpt4free

### Error Handling
- HTTPException for API errors
- Fallback execution without Docker
- AI service retry logic with exponential backoff
- Comprehensive error messages

## File Statistics
- Total files: 48
- Python files: 40
- Configuration files: 5
- Documentation: 3

## Next Steps
1. Configure PostgreSQL connection
2. Set up gpt4free provider
3. Initialize course structure and achievements
4. Deploy with Docker Compose or Kubernetes
5. Connect with frontend application
