# PyNeon — Python Learning Platform

AI-powered platform for learning Python from scratch. Generates theory, tasks, and code feedback via **gpt4free** — no paid APIs required.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)

---

## Features

- 12-week Python course structured from basics to problem-solving level
- AI-generated theory and tasks per lesson topic (via gpt4free)
- Monaco Editor in the browser for writing and submitting code
- Sandboxed code execution inside Docker containers
- JWT authentication
- XP points, levels, streaks, and achievements system
- Leaderboard and personal progress dashboard

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, TypeScript, TailwindCSS, Framer Motion |
| Backend | FastAPI, Python 3.11 |
| Database | PostgreSQL 16, SQLAlchemy 2.0 (async), Alembic |
| Auth | JWT (python-jose), bcrypt |
| AI | gpt4free |
| Code Editor | Monaco Editor |
| Sandbox | Docker-in-Docker |
| Deploy | Docker Compose |

---

## Project Structure

```
python-learning-app/
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── auth.py          # Registration, login
│   │   │   ├── lessons.py       # Lessons, theory generation
│   │   │   ├── tasks.py         # Tasks, AI generation
│   │   │   ├── submissions.py   # Code submission & execution
│   │   │   ├── progress.py      # Progress, leaderboard
│   │   │   └── achievements.py  # Achievements
│   │   ├── core/
│   │   │   ├── config.py        # App configuration
│   │   │   ├── database.py      # Async SQLAlchemy setup
│   │   │   └── security.py      # JWT + password hashing
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── repositories/        # Data access layer
│   │   ├── services/
│   │   │   ├── ai_service.py        # gpt4free integration
│   │   │   ├── sandbox_service.py   # Docker code execution
│   │   │   ├── lesson_service.py
│   │   │   ├── task_service.py
│   │   │   ├── progress_service.py
│   │   │   └── achievement_service.py
│   │   ├── data/
│   │   │   └── course_structure.py  # 12-week curriculum
│   │   └── main.py
│   ├── alembic/                 # DB migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── auth/            # Login / Register
│   │   │   ├── dashboard/       # User dashboard
│   │   │   ├── lessons/[id]/    # Lesson view with theory and tasks
│   │   │   └── tasks/           # Task catalog
│   │   ├── components/
│   │   │   ├── editor/          # Monaco code editor
│   │   │   └── ui/              # Navbar, cards, progress bar
│   │   └── lib/
│   │       ├── api.ts           # Axios API client
│   │       └── store.ts         # Zustand auth state
│   └── Dockerfile
├── docker-compose.yml
└── docker-compose.dev.yml
```

---

## Getting Started

### Requirements

- Docker 24+
- Docker Compose 2.x

### 1. Clone

```bash
git clone https://github.com/maxim-vdonsk/python-learning-app.git
cd python-learning-app
```

### 2. Configure environment

```bash
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local
```

Edit `backend/.env` and set a strong `SECRET_KEY`.

### 3. Run

```bash
docker-compose up -d --build
```

Wait ~30 seconds, then open:

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

### 4. Initialize course data

```bash
curl -X POST http://localhost:8000/api/v1/lessons/initialize
curl -X POST http://localhost:8000/api/v1/achievements/seed
```

### 5. Development mode (hot-reload)

```bash
docker-compose -f docker-compose.dev.yml up
```

---

## Configuration

### backend/.env

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/python_learning
SECRET_KEY=your-secret-key-min-32-chars
DEBUG=false
ALLOWED_ORIGINS=["http://localhost:3000"]
SANDBOX_IMAGE=python:3.11-alpine
SANDBOX_TIMEOUT=10
SANDBOX_MEM_LIMIT=64m
GPT4FREE_MODEL=gpt-4o-mini
```

### frontend/.env.local

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### gpt4free model

By default the app uses `gpt-4o-mini`. If a provider is unavailable, change the model in `backend/.env`:

```env
GPT4FREE_MODEL=gpt-3.5-turbo
```

gpt4free selects an available provider automatically.

---

## API Reference

Full interactive docs at **http://localhost:8000/docs**

### Auth
```
POST /api/v1/auth/register
POST /api/v1/auth/login/json
```

### Lessons
```
GET  /api/v1/lessons/course         # Full course structure
GET  /api/v1/lessons/{id}/theory    # AI-generated theory
POST /api/v1/lessons/initialize     # Seed course data
```

### Tasks
```
GET  /api/v1/tasks/                 # List with filters
GET  /api/v1/tasks/{id}
POST /api/v1/tasks/generate         # AI-generate a task
```

### Submissions
```
POST /api/v1/submissions/           # Submit code
GET  /api/v1/submissions/my         # My submissions
```

### Progress
```
GET  /api/v1/progress/dashboard
GET  /api/v1/progress/leaderboard
```

### Achievements
```
GET  /api/v1/achievements/
GET  /api/v1/achievements/all
POST /api/v1/achievements/seed
```

---

## Gamification

| Difficulty | XP reward |
|------------|-----------|
| Easy | +50 XP |
| Medium | +100 XP |
| Hard | +200 XP |

Level increases every **500 XP**.

Achievements are awarded for completing lessons, maintaining streaks, and solving tasks.

---

## Docker

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Rebuild
docker-compose up -d --build

# Logs
docker-compose logs -f backend

# Reset database
docker-compose down -v && docker-compose up -d
```

---

## Troubleshooting

**gpt4free not responding** — switch to another model in `.env` (`gpt-3.5-turbo`).

**Sandbox not working** — make sure Docker socket is mounted:
```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

**Database connection error** — check `docker-compose logs db`, then restart the backend:
```bash
docker-compose restart backend
```

---

## License

MIT
