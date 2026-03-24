# 🚀 PyNeon — Python Learning Platform

> AI-powered Python learning platform with cyberpunk neon design.
> Powered entirely by **gpt4free** — no paid APIs needed.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)

## 📋 Содержание

- [Функциональность](#-функциональность)
- [Стек технологий](#-стек-технологий)
- [Структура проекта](#-структура-проекта)
- [Быстрый старт](#-быстрый-старт)
- [Настройка](#-настройка)
- [API документация](#-api-документация)
- [Примеры запросов](#-примеры-api-запросов)

---

## ✨ Функциональность

### Обучение
- 📚 **12-недельный курс** Python от нуля до уровня Yandex CodeRun
- 🤖 **AI-генерация теории** — подробные объяснения через gpt4free
- 💻 **Monaco Editor** — профессиональный редактор кода в браузере
- 🧪 **Sandbox выполнение** — безопасный запуск кода в Docker

### AI-возможности (gpt4free)
- Генерация уроков и объяснений "для новичка"
- Генерация задач по теме
- Анализ кода (стиль, производительность, корректность)
- Персональные мотивационные фразы

### Геймификация
- 🏆 Система достижений (8+ ачивок)
- 🔥 Streak дней подряд
- ⚡ XP очки и уровни
- 📊 Рейтинговая таблица

### Задачи
- Каталог задач (easy/medium/hard)
- Фильтрация по сложности и категории
- Тренировочный режим

---

## 🛠 Стек технологий

| Компонент | Технология |
|-----------|-----------|
| Frontend | Next.js 14 + TailwindCSS + Framer Motion |
| Backend | FastAPI + Python 3.11 |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0 (async) |
| Auth | JWT (python-jose) |
| AI | gpt4free |
| Code Editor | Monaco Editor |
| Sandbox | Docker-in-Docker |
| Deploy | Docker Compose |

---

## 📁 Структура проекта

```
python-learning-app/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # Эндпоинты API
│   │   │   ├── auth.py      # Регистрация, логин
│   │   │   ├── lessons.py   # Уроки, теория
│   │   │   ├── tasks.py     # Задачи, генерация
│   │   │   ├── submissions.py # Отправка кода
│   │   │   ├── progress.py  # Прогресс, рейтинг
│   │   │   └── achievements.py # Достижения
│   │   ├── core/
│   │   │   ├── config.py    # Конфигурация
│   │   │   ├── database.py  # Async SQLAlchemy
│   │   │   └── security.py  # JWT + bcrypt
│   │   ├── models/          # SQLAlchemy модели
│   │   ├── schemas/         # Pydantic схемы
│   │   ├── repositories/    # Слой данных
│   │   ├── services/
│   │   │   ├── ai_service.py      # ← Все вызовы gpt4free здесь
│   │   │   ├── sandbox_service.py # Docker sandbox
│   │   │   ├── auth_service.py
│   │   │   ├── lesson_service.py
│   │   │   ├── task_service.py
│   │   │   ├── progress_service.py
│   │   │   └── achievement_service.py
│   │   ├── data/
│   │   │   └── course_structure.py # 12-недельная программа
│   │   └── main.py
│   ├── alembic/             # Миграции БД
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── auth/        # Страница входа/регистрации
│   │   │   ├── dashboard/   # Главная панель
│   │   │   ├── lessons/[id] # Урок с теорией и практикой
│   │   │   └── tasks/       # Каталог задач
│   │   ├── components/
│   │   │   ├── editor/      # Monaco Code Editor
│   │   │   └── ui/          # Navbar, ProgressBar, Cards
│   │   └── lib/
│   │       ├── api.ts       # Axios клиент
│   │       └── store.ts     # Zustand (auth state)
│   ├── tailwind.config.ts   # Cyberpunk тема
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🚀 Быстрый старт

### Требования
- [Docker](https://docs.docker.com/get-docker/) 24+
- [Docker Compose](https://docs.docker.com/compose/) 2.x+
- Git

### 1. Клонирование

```bash
git clone <repository-url>
cd python-learning-app
```

### 2. Настройка окружения

```bash
# Бэкенд
cp backend/.env.example backend/.env
# Отредактируй SECRET_KEY в backend/.env!

# Фронтенд
cp frontend/.env.local.example frontend/.env.local
```

### 3. Запуск (Production)

```bash
docker-compose up -d --build
```

Подождите ~30 секунд. После успешного запуска:

| Сервис | URL |
|--------|-----|
| 🌐 Frontend | http://localhost:3000 |
| ⚙️ Backend API | http://localhost:8000 |
| 📖 API Docs | http://localhost:8000/docs |

### 4. Инициализация курса

После первого запуска выполни:

```bash
# Инициализация структуры курса
curl -X POST http://localhost:8000/api/v1/lessons/initialize

# Заполнение достижений
curl -X POST http://localhost:8000/api/v1/achievements/seed
```

### 5. Запуск для разработки (hot-reload)

```bash
docker-compose -f docker-compose.dev.yml up
```

---

## ⚙️ Настройка

### backend/.env

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/python_learning
SECRET_KEY=your-super-secret-key-min-32-chars
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

### Настройка gpt4free

По умолчанию используется модель `gpt-4o-mini`. Если она недоступна, измени в `backend/.env`:

```env
# Варианты:
GPT4FREE_MODEL=gpt-4o-mini
GPT4FREE_MODEL=gpt-4
GPT4FREE_MODEL=gpt-3.5-turbo
GPT4FREE_MODEL=claude-3-haiku
```

gpt4free автоматически выбирает доступного провайдера.

---

## 📚 API документация

После запуска доступна интерактивная Swagger UI:
**http://localhost:8000/docs**

### Основные эндпоинты

#### Аутентификация
```
POST /api/v1/auth/register   # Регистрация
POST /api/v1/auth/login/json # Вход
```

#### Уроки
```
GET  /api/v1/lessons/course           # Полная структура курса
GET  /api/v1/lessons/{id}/theory      # Теория урока (AI генерация)
POST /api/v1/lessons/initialize       # Инициализация курса
```

#### Задачи
```
GET  /api/v1/tasks/               # Список с фильтрами
GET  /api/v1/tasks/{id}           # Конкретная задача
POST /api/v1/tasks/generate       # AI-генерация задачи
```

#### Решения
```
POST /api/v1/submissions/         # Отправить код
GET  /api/v1/submissions/my       # Мои решения
```

#### Прогресс
```
GET  /api/v1/progress/dashboard   # Статистика дашборда
GET  /api/v1/progress/leaderboard # Рейтинг
```

#### Достижения
```
GET  /api/v1/achievements/        # Мои достижения
GET  /api/v1/achievements/all     # Все достижения
POST /api/v1/achievements/seed    # Заполнить достижения
```

---

## 💻 Примеры API запросов

### Регистрация

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "username": "hacker", "password": "secret123"}'
```

Ответ:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "hacker",
    "xp_points": 0,
    "level": 1,
    "streak_days": 0
  }
}
```

### Получение теории урока

```bash
TOKEN="your-jwt-token-here"

curl http://localhost:8000/api/v1/lessons/1/theory \
  -H "Authorization: Bearer $TOKEN"
```

Ответ:
```json
{
  "lesson_id": 1,
  "title": "Введение в Python",
  "theory": "# Введение в Python\n\n## Что такое Python?\n...",
  "examples": [
    {
      "title": "Первая программа",
      "code": "print('Hello, World!')",
      "explanation": "Функция print() выводит текст на экран"
    }
  ]
}
```

### Генерация AI задачи

```bash
curl -X POST "http://localhost:8000/api/v1/tasks/generate?topic=циклы&difficulty=easy&lesson_id=1" \
  -H "Authorization: Bearer $TOKEN"
```

### Отправка решения

```bash
curl -X POST http://localhost:8000/api/v1/submissions/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": 1,
    "code": "n = int(input())\nfor i in range(1, n+1):\n    print(i)"
  }'
```

Ответ:
```json
{
  "submission_id": 42,
  "is_correct": true,
  "execution_time_ms": 45.2,
  "passed_tests": 3,
  "total_tests": 3,
  "ai_feedback": "Отличное решение! Код читаемый и правильный...",
  "ai_score": 92.0,
  "recommendations": ["Попробуй использовать list comprehension для краткости"],
  "xp_earned": 50,
  "new_achievements": [
    {"title": "Первый шаг", "icon": "🎯", "xp_reward": 50}
  ]
}
```

### Статистика дашборда

```bash
curl http://localhost:8000/api/v1/progress/dashboard \
  -H "Authorization: Bearer $TOKEN"
```

Ответ:
```json
{
  "total_lessons": 48,
  "completed_lessons": 5,
  "completion_percentage": 10.4,
  "current_streak": 3,
  "total_xp": 750,
  "level": 2,
  "rating": 7.5,
  "motivation_phrase": "Ты уже прошёл 5 уроков — это только начало пути к мастерству!"
}
```

---

## 🎮 Система геймификации

### XP за задачи
| Сложность | XP |
|-----------|-----|
| Easy | +50 XP |
| Medium | +100 XP |
| Hard | +200 XP |

### Уровни
Уровень повышается каждые **500 XP**: Lv.1 → Lv.2 → ...

### Достижения
| Иконка | Название | Условие |
|--------|----------|---------|
| 🎯 | Первый шаг | 1 урок |
| 📅 | Неделя пройдена | 7 уроков |
| 🔥 | 3 дня подряд | Стрик 3 дня |
| ⚡ | Недельная серия | Стрик 7 дней |
| 💎 | Месяц упорства | Стрик 30 дней |
| 🧩 | Решатель | 10 задач |
| 🏆 | Мастер задач | 50 задач |
| 🎓 | Выпускник | Весь курс |

---

## 🐳 Docker команды

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Просмотр логов
docker-compose logs -f backend

# Пересборка
docker-compose up -d --build

# Сброс базы данных
docker-compose down -v && docker-compose up -d

# Войти в контейнер бэкенда
docker exec -it pyneon_backend bash
```

---

## 🔧 Возможные проблемы

### gpt4free не отвечает
Некоторые провайдеры могут быть недоступны. Попробуй изменить модель в `.env`:
```
GPT4FREE_MODEL=gpt-3.5-turbo
```

### Docker sandbox не работает
Убедись, что Docker socket монтируется:
```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

### База данных не подключается
```bash
docker-compose logs db
# Проверь что postgres запустился
docker-compose restart backend
```

---

## 📄 Лицензия

MIT License — используй свободно!

---

*Powered by [gpt4free](https://github.com/xtekky/gpt4free) • No paid APIs required*
