"""
AI Service Layer — все вызовы gpt4free изолированы здесь.
Совместимо с g4f >= 7.3.0

Рабочие провайдеры (проверено на сервере):
  - Yqcloud     / gpt-4o-mini  ✅
  - OperaAria   / gpt-4o-mini  ✅
  - Mintlify    / gpt-4o-mini  ✅
"""
import json
import asyncio
import logging
import hashlib
from typing import Optional

logger = logging.getLogger(__name__)

# Только проверенные рабочие провайдеры, строками (lazy resolve)
PROVIDER_CHAIN = [
    ("Yqcloud",    "gpt-4o-mini"),
    ("OperaAria",  "gpt-4o-mini"),
    ("Mintlify",   "gpt-4o-mini"),
]

# Статичные мотивационные фразы — fallback когда AI недоступен
_STATIC_PHRASES = [
    "Каждая строка кода — шаг к мастерству. Продолжай!",
    "Лучший момент начать учиться — сейчас. Ты уже здесь!",
    "Ты уже лучше того, кем был вчера. Не останавливайся!",
    "Код — это суперсила. Ты её осваиваешь прямо сейчас.",
    "Сложно сегодня — легко завтра. Практикуйся каждый день!",
    "Каждая ошибка — это урок. Ты учишься быстрее, чем думаешь!",
    "Python открывает двери. Ты уже стучишься в правильную дверь!",
]


def _get_provider(name: Optional[str]):
    """Безопасно получить провайдер по имени. None = авто-выбор."""
    if name is None:
        return None
    try:
        import g4f
        return getattr(g4f.Provider, name, None)
    except Exception:
        return None


class AIService:
    """
    Сервис AI-функций на базе gpt4free.
    Все вызовы LLM проходят через этот класс.
    """

    async def _chat(self, system_prompt: str, user_prompt: str,
                    timeout: int = 30) -> str:
        """
        Пробует провайдеры из PROVIDER_CHAIN по очереди.
        Возвращает первый успешный ответ.
        """
        from g4f.client import AsyncClient

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ]

        last_error = "нет провайдеров"
        for provider_name, model in PROVIDER_CHAIN:
            provider = _get_provider(provider_name)
            label = provider_name or "auto"

            if provider_name is not None and provider is None:
                logger.debug(f"AI: провайдер {provider_name} не найден, пропускаем")
                continue

            try:
                logger.info(f"AI: пробую {label}/{model}")
                client = AsyncClient(provider=provider)
                resp = await asyncio.wait_for(
                    client.chat.completions.create(
                        model=model,
                        messages=messages,
                    ),
                    timeout=timeout,
                )
                text = (resp.choices[0].message.content or "").strip()
                # Проверяем что ответ не пустой и не страница логина
                if (text
                        and len(text) > 5
                        and "log in" not in text[:50].lower()
                        and "sign in" not in text[:50].lower()
                        and "[AI недоступен]" not in text):
                    logger.info(f"AI: успех через {label}/{model} ({len(text)} символов)")
                    return text
                last_error = f"{label}: подозрительный ответ: {text[:60]}"
                logger.warning(f"AI: {last_error}")
            except asyncio.TimeoutError:
                last_error = f"{label}: таймаут {timeout}с"
                logger.warning(f"AI таймаут: {last_error}")
            except Exception as exc:
                last_error = f"{label}: {exc}"
                logger.warning(f"AI ошибка: {last_error}")

        logger.error(f"AI: все провайдеры исчерпаны. {last_error}")
        return f"[AI недоступен] {last_error}"

    # ------------------------------------------------------------------ #

    async def generate_theory(self, topic: str, lesson_title: str) -> dict:
        """Генерирует подробную теорию урока через AI."""
        system = (
            "Ты — опытный преподаватель Python. "
            "Объясняй подробно, с аналогиями, для полного новичка. "
            "Отвечай на русском языке, используй markdown и блоки ```python."
        )
        prompt = f"""Создай подробное объяснение темы "{lesson_title}" (тема: {topic}).

Структура:
1. Что это такое (аналогия из жизни)
2. Зачем нужно
3. Синтаксис с объяснением
4. 3 примера от простого к сложному
5. Частые ошибки
6. Советы

Верни JSON:
{{"theory": "текст в markdown", "examples": [{{"title":"..","code":"..","explanation":".."}}]}}"""

        resp = await self._chat(system, prompt)
        return self._parse_json(resp, {"theory": resp, "examples": []})

    async def generate_task(self, topic: str, difficulty: str,
                            lesson_title: str) -> dict:
        """Генерирует задачу по теме и сложности."""
        hints_map = {
            "easy":   "1-5 строк кода, базовый синтаксис",
            "medium": "10-20 строк, несколько концепций",
            "hard":   "сложный алгоритм, оптимальное решение",
        }
        system = (
            "Ты создаёшь чёткие задачи по Python. "
            "Отвечай ТОЛЬКО валидным JSON на русском языке."
        )
        prompt = f"""Задача по Python: тема "{lesson_title}", сложность {difficulty} ({hints_map.get(difficulty,'')}).

Верни ТОЛЬКО JSON без лишнего текста:
{{
  "title": "Название",
  "description": "Описание с примерами ввода/вывода",
  "hints": ["подсказка 1", "подсказка 2"],
  "test_cases": [
    {{"input": "ввод", "expected_output": "вывод"}},
    {{"input": "ввод2", "expected_output": "вывод2"}}
  ],
  "solution_template": "# Напишите решение здесь\\n",
  "category": "strings"
}}"""

        resp = await self._chat(system, prompt)
        return self._parse_json(resp, {
            "title": f"Задача по {topic}",
            "description": resp,
            "hints": [],
            "test_cases": [],
            "solution_template": "# Напишите решение здесь\n",
            "category": topic,
        })

    async def analyze_code(
        self,
        code: str,
        task_description: str,
        is_correct: bool,
        execution_time_ms: Optional[float] = None,
        error: Optional[str] = None,
    ) -> dict:
        """Анализирует код студента, возвращает отзыв и оценку."""
        system = (
            "Ты — доброжелательный ментор Python. "
            "Анализируй код: правильность, стиль, производительность. "
            "Отвечай на русском языке, только валидным JSON."
        )
        status  = "ПРАВИЛЬНО" if is_correct else "НЕПРАВИЛЬНО"
        t_str   = f"{execution_time_ms:.1f}мс" if execution_time_ms else "?"
        err_str = f"\nОшибка: {error}" if error else ""

        prompt = f"""Проанализируй код:

ЗАДАЧА: {task_description[:400]}
КОД:
```python
{code[:1200]}
```
Статус: {status} | Время: {t_str}{err_str}

Верни JSON:
{{
  "feedback": "анализ 2-3 абзаца",
  "score": 80,
  "recommendations": ["совет 1", "совет 2"],
  "style_issues": [],
  "performance_note": ""
}}"""

        resp = await self._chat(system, prompt)
        base = 80 if is_correct else 30
        return self._parse_json(resp, {
            "feedback": resp or "Код проверен.",
            "score": base,
            "recommendations": ["Продолжай практиковаться!"],
            "style_issues": [],
            "performance_note": "",
        })

    async def generate_motivation(self, username: str, stats: dict) -> str:
        """
        Генерирует персональную мотивационную фразу.
        Таймаут 10 сек — дашборд не должен долго ждать.
        При неудаче возвращает статичную фразу.
        """
        system = "Ты вдохновляющий ментор. Пиши короткие фразы на русском."
        prompt = (
            f"Мотивация для {username}: "
            f"{stats.get('completed_lessons', 0)} уроков, "
            f"стрик {stats.get('streak', 0)} дней, уровень {stats.get('level', 1)}. "
            "1-2 предложения без кавычек."
        )
        try:
            result = await asyncio.wait_for(
                self._chat(system, prompt, timeout=10),
                timeout=12,
            )
            if not result.startswith("[AI недоступен"):
                return result
        except (asyncio.TimeoutError, Exception):
            pass

        # Статичная фраза на основе имени
        idx = int(hashlib.md5(username.encode()).hexdigest(), 16) % len(_STATIC_PHRASES)
        return _STATIC_PHRASES[idx]

    async def check_code_correctness(self, code: str, test_cases: list) -> dict:
        """AI-проверка логики кода когда sandbox недоступен."""
        system = "Ты Python интерпретатор. Выполняй код мысленно."
        prompt = f"""Код:
```python
{code[:800]}
```
Тесты: {json.dumps(test_cases[:3], ensure_ascii=False)}
Верни JSON: {{"is_correct": true, "explanation": "...", "passed": 1, "total": 2}}"""

        resp = await self._chat(system, prompt, timeout=20)
        return self._parse_json(resp, {
            "is_correct": False,
            "explanation": "Не удалось проверить",
            "passed": 0,
            "total": len(test_cases),
        })

    # ------------------------------------------------------------------ #

    def _parse_json(self, text: str, fallback: dict) -> dict:
        """Извлекает первый валидный JSON-объект из текста."""
        start = text.find('{')
        end   = text.rfind('}') + 1
        if start != -1 and end > start:
            try:
                return json.loads(text[start:end])
            except json.JSONDecodeError:
                pass
        return fallback


# Singleton
ai_service = AIService()
