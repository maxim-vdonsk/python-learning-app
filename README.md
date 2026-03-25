# PyNeon — Платформа для изучения Python

Платформа для изучения Python с нуля на основе AI. Генерирует теорию, задачи и обратную связь по коду через **gpt4free** — без платных API.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)

---

## Возможности

- 12-недельный курс Python от основ до уверенного решения задач
- AI-генерация теории и задач по теме урока (через gpt4free)
- Monaco Editor в браузере для написания и отправки кода
- Выполнение кода в изолированном Docker-контейнере
- Аутентификация через JWT
- Email-уведомления: приветственное письмо при регистрации, восстановление пароля на почту
- Система XP, уровней, стриков и достижений
- Таблица лидеров и личный дашборд прогресса

---

## Стек технологий

| Уровень | Технология |
|---------|-----------|
| Frontend | Next.js 14, TypeScript, TailwindCSS, Framer Motion |
| Backend | FastAPI, Python 3.11 |
| База данных | PostgreSQL 16, SQLAlchemy 2.0 (async), Alembic |
| Авторизация | JWT (python-jose), bcrypt |
| AI | gpt4free |
| Редактор кода | Monaco Editor |
| Песочница | Docker-in-Docker |
| Деплой | Docker Compose, Caddy |

---

## Структура проекта

```
python-learning-app/
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── auth.py          # Регистрация, вход
│   │   │   ├── lessons.py       # Уроки, генерация теории
│   │   │   ├── tasks.py         # Задачи, AI-генерация
│   │   │   ├── submissions.py   # Отправка и выполнение кода
│   │   │   ├── progress.py      # Прогресс, рейтинг
│   │   │   └── achievements.py  # Достижения
│   │   ├── core/
│   │   │   ├── config.py        # Конфигурация приложения
│   │   │   ├── database.py      # Асинхронный SQLAlchemy
│   │   │   └── security.py      # JWT + хэширование паролей
│   │   ├── models/              # SQLAlchemy модели
│   │   ├── schemas/             # Pydantic схемы
│   │   ├── repositories/        # Слой доступа к данным
│   │   ├── services/
│   │   │   ├── ai_service.py        # Интеграция с gpt4free
│   │   │   ├── sandbox_service.py   # Выполнение кода в Docker
│   │   │   ├── email_service.py     # SMTP email (welcome, восстановление пароля)
│   │   │   ├── lesson_service.py
│   │   │   ├── task_service.py
│   │   │   ├── progress_service.py
│   │   │   └── achievement_service.py
│   │   ├── data/
│   │   │   └── course_structure.py  # Программа курса на 12 недель
│   │   └── main.py
│   ├── alembic/                 # Миграции БД
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── auth/            # Вход / Регистрация
│   │   │   ├── dashboard/       # Дашборд пользователя
│   │   │   ├── lessons/[id]/    # Страница урока с теорией и задачами
│   │   │   └── tasks/           # Каталог задач
│   │   ├── components/
│   │   │   ├── editor/          # Monaco редактор кода
│   │   │   └── ui/              # Navbar, карточки, прогресс-бар
│   │   └── lib/
│   │       ├── api.ts           # Axios клиент
│   │       └── store.ts         # Zustand (состояние авторизации)
│   └── Dockerfile
├── Caddyfile              # Конфигурация reverse proxy
├── docker-compose.yml
└── docker-compose.dev.yml
```

---

## Быстрый старт

### Требования

- Docker 24+
- Docker Compose 2.x

### 1. Клонирование

```bash
git clone https://github.com/maxim-vdonsk/python-learning-app.git
cd python-learning-app
```

### 2. Настройка окружения

```bash
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local
```

Отредактируй `backend/.env` — обязательно задай свой `SECRET_KEY`.

### 3. Локальный запуск (без домена)

```bash
docker-compose up -d --build
```

Подождите ~30 секунд, затем откройте:

| Сервис | URL |
|--------|-----|
| Frontend | http://localhost |
| Backend API | http://localhost/api/v1 |
| API документация (Swagger) | http://localhost/api/v1/../docs |

### 3а. Деплой с доменом (HTTPS автоматически)

Сгенерируй секретный ключ:

```bash
openssl rand -hex 32
```

Создай `.env` файл в корне проекта:

```env
DOMAIN=yourdomain.com
NEXT_PUBLIC_API_URL=https://yourdomain.com
ALLOWED_ORIGINS=["https://yourdomain.com"]
SECRET_KEY=<вывод openssl rand -hex 32>
```

Запусти:

```bash
docker-compose up -d --build
```

Caddy автоматически получит SSL-сертификат через Let's Encrypt. Сайт будет доступен по `https://yourdomain.com`.

> **Требования для HTTPS:** домен должен указывать на IP сервера (A-запись), порты 80 и 443 должны быть открыты.

### 4. Инициализация данных курса

```bash
curl -X POST http://localhost:8000/api/v1/lessons/initialize
curl -X POST http://localhost:8000/api/v1/achievements/seed
```

### 5. Режим разработки (hot-reload)

```bash
docker-compose -f docker-compose.dev.yml up
```

---

## Конфигурация

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

# SMTP Email (опционально — для welcome-писем и восстановления пароля)
# Gmail: SMTP_HOST=smtp.gmail.com, SMTP_PORT=465, SMTP_TLS=true
# Yandex: SMTP_HOST=smtp.yandex.ru, SMTP_PORT=465, SMTP_TLS=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_TLS=true
```

### frontend/.env.local

```env
# Локально (Caddy проксирует /api/* на бэкенд)
NEXT_PUBLIC_API_URL=http://localhost

# С доменом
# NEXT_PUBLIC_API_URL=https://yourdomain.com
```

### Caddy (Caddyfile)

Caddy используется как reverse proxy:
- `yourdomain.com/api/*` → FastAPI backend (порт 8000)
- `yourdomain.com/*` → Next.js frontend (порт 3000)

При указании реального домена Caddy автоматически получает и обновляет SSL-сертификат через Let's Encrypt.

### Настройка gpt4free

По умолчанию используется модель `gpt-4o-mini`. Если провайдер недоступен, замени модель в `backend/.env`:

```env
GPT4FREE_MODEL=gpt-3.5-turbo
```

gpt4free автоматически выбирает доступного провайдера.

---

## API

Полная интерактивная документация: **http://localhost:8000/docs**

### Авторизация
```
POST /api/v1/auth/register          # Регистрация (welcome email отправляется автоматически)
POST /api/v1/auth/login/json        # Вход
POST /api/v1/auth/forgot-password   # Сброс пароля — новый пароль отправляется на email
```

### Уроки
```
GET  /api/v1/lessons/course         # Полная структура курса
GET  /api/v1/lessons/{id}/theory    # AI-генерация теории урока
POST /api/v1/lessons/initialize     # Инициализация данных курса
```

### Задачи
```
GET  /api/v1/tasks/                 # Список с фильтрами
GET  /api/v1/tasks/{id}
POST /api/v1/tasks/generate         # AI-генерация задачи
```

### Решения
```
POST /api/v1/submissions/           # Отправить код на проверку
GET  /api/v1/submissions/my         # Мои решения
```

### Прогресс
```
GET  /api/v1/progress/dashboard
GET  /api/v1/progress/leaderboard
```

### Достижения
```
GET  /api/v1/achievements/
GET  /api/v1/achievements/all
POST /api/v1/achievements/seed
```

---

## Геймификация

| Сложность задачи | Награда |
|-----------------|---------|
| Easy | +50 XP |
| Medium | +100 XP |
| Hard | +200 XP |

Уровень повышается каждые **500 XP**.

Достижения выдаются за прохождение уроков, поддержание стриков и решение задач.

---

## Docker

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Пересборка
docker-compose up -d --build

# Логи
docker-compose logs -f backend

# Сброс базы данных
docker-compose down -v && docker-compose up -d
```

---

## Возможные проблемы

**gpt4free не отвечает** — смените модель в `.env` (например, `gpt-3.5-turbo`).

**Песочница не работает** — убедитесь, что Docker socket монтируется:
```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

**Ошибка подключения к базе данных** — проверьте `docker-compose logs db`, затем перезапустите бэкенд:
```bash
docker-compose restart backend
```

**HTTPS не работает** — убедитесь, что:
1. A-запись домена указывает на IP сервера
2. Порты 80 и 443 открыты в файрволе
3. Переменная `DOMAIN` задана в `.env`

Логи Caddy:
```bash
docker-compose logs caddy
```

---

## Лицензия

MIT
