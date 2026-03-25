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
# Обновленный список - Free2GPT больше не работает (возвращает HTML)
PROVIDER_CHAIN = [
    ("Yqcloud", "gpt-4o-mini"),
    ("OperaAria", "gpt-4o-mini"),
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
        Общий дедлайн на все провайдеры = timeout * 1.5
        """
        from g4f.client import AsyncClient

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ]

        last_error = "нет провайдеров"
        successful_response = None

        # Общий дедлайн на все попытки
        overall_deadline = asyncio.get_event_loop().time() + (timeout * 1.5)
        
        logger.info(f"AI: начинаю перебор провайдеров, дедлайн через {timeout * 1.5}с")

        for provider_name, model in PROVIDER_CHAIN:
            # Проверяем общий дедлайн перед каждой попыткой
            if asyncio.get_event_loop().time() >= overall_deadline:
                logger.warning(f"AI: превышен общий дедлайн ({timeout * 1.5}с)")
                last_error = "превышен общий дедлайн"
                break

            provider = _get_provider(provider_name)
            label = provider_name or "auto"

            if provider_name is not None and provider is None:
                logger.debug(f"AI: провайдер {provider_name} не найден, пропускаем")
                continue
            
            logger.info(f"AI: === Попытка {PROVIDER_CHAIN.index((provider_name, model)) + 1}/{len(PROVIDER_CHAIN)}: {label}/{model} ===")

            try:
                logger.info(f"AI: пробую {label}/{model}")
                client = AsyncClient(provider=provider)
                
                # Вычисляем остаток времени для текущей попытки
                remaining_time = overall_deadline - asyncio.get_event_loop().time()
                attempt_timeout = min(timeout, max(5, remaining_time))
                
                resp = await asyncio.wait_for(
                    client.chat.completions.create(
                        model=model,
                        messages=messages,
                    ),
                    timeout=attempt_timeout,
                )
                text = (resp.choices[0].message.content or "").strip()
                successful_response = text
                
            except asyncio.TimeoutError:
                last_error = f"{label}: таймаут {attempt_timeout}с"
                logger.warning(f"AI таймаут: {last_error}")
                continue
            except Exception as exc:
                last_error = f"{label}: {exc}"
                logger.warning(f"AI ошибка: {last_error}")
                continue
            
            # Проверяем что ответ не пустой
            if not successful_response:
                last_error = f"{label}: пустой ответ"
                logger.warning(f"AI: {last_error}")
                successful_response = None
                continue
            
            # Проверяем на ошибки аутентификации и другие API-ошибки
            text_lower = successful_response.lower()
            if "authentication error" in text_lower or "no api key" in text_lower:
                last_error = f"{label}: ошибка аутентификации"
                logger.warning(f"AI: {last_error}")
                successful_response = None
                continue
            
            # Проверяем на HTML-ответы (когда провайдер вернул страницу вместо JSON)
            if text_lower.startswith("<!doctype") or text_lower.startswith("<html"):
                last_error = f"{label}: вернул HTML вместо ответа"
                logger.warning(f"AI: провайдер {label} вернул HTML-страницу вместо ответа")
                successful_response = None
                continue
            
            # Проверяем на стриминг-ответы с ошибками (data: {...})
            if successful_response.startswith("data:"):
                # Пытаемся распарсить как JSON ошибку
                try:
                    import json as json_lib
                    # Извлекаем первую data: строку
                    first_line = successful_response.split("\n")[0]
                    if first_line.startswith("data:"):
                        json_str = first_line[5:].strip()
                        if json_str != "[DONE]":
                            error_data = json_lib.loads(json_str)
                            if error_data.get("type") == "error":
                                error_text = error_data.get("errorText", "Неизвестная ошибка")
                                last_error = f"{label}: {error_text}"
                                logger.warning(f"AI: ошибка от провайдера: {last_error}")
                                successful_response = None
                                continue
                except Exception:
                    # Если не распарсили, продолжаем проверки ниже
                    pass
            
            # Проверяем на подозрительные ответы
            if (len(successful_response) <= 5
                    or "log in" in successful_response[:50].lower()
                    or "sign in" in successful_response[:50].lower()
                    or "[AI недоступен]" in successful_response
                    or successful_response.startswith("data:")):
                last_error = f"{label}: подозрительный ответ: {successful_response[:60]}"
                logger.warning(f"AI: {last_error}")
                successful_response = None
                continue
            
            # Успех!
            logger.info(f"AI: успех через {label}/{model} ({len(successful_response)} символов)")
            return successful_response

        # Все провайдеры исчерпаны
        logger.error(f"AI: все провайдеры исчерпаны после {len(PROVIDER_CHAIN)} попыток. Последняя ошибка: {last_error}")
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
                            lesson_title: str,
                            prev_topics: list[str] | None = None) -> dict:
        """
        Генерирует задачу по теме и сложности.

        prev_topics — список тем, пройденных ДО этого урока.
        AI органично включает их в задачу (не сложнее текущей темы).
        """
        hints_map = {
            "easy":   "1-5 строк кода, базовый синтаксис",
            "medium": "10-20 строк, несколько концепций",
            "hard":   "сложный алгоритм, оптимальное решение",
        }
        system = (
            "Ты создаёшь чёткие практические задачи по Python для начинающих. "
            "Отвечай ТОЛЬКО валидным JSON на русском языке."
        )

        # Блок с ранее изученными темами
        if prev_topics:
            prev_block = (
                "\nУченик уже изучил ТОЛЬКО эти темы (и ничего больше):\n"
                + "\n".join(f"  - {t}" for t in prev_topics[-10:])
                + "\n"
            )
            forbidden_block = (
                "\nСТРОГО ЗАПРЕЩЕНО использовать в задаче:\n"
                "  - классы, ООП (class, self, __init__)\n"
                "  - исключения (try/except), если они не в пройденных темах\n"
                "  - импорт модулей (import), если он не в пройденных темах\n"
                "  - декораторы, генераторы, async/await\n"
                "  - любые концепции, которых НЕТ в списке пройденных тем выше\n"
            )
        else:
            prev_block = "\nУченик только начинает — это самый первый урок.\n"
            forbidden_block = (
                "\nСТРОГО ЗАПРЕЩЕНО использовать в задаче:\n"
                "  - всё, кроме базового вывода и простейших операций текущей темы\n"
            )

        prompt = f"""Создай задачу по Python для новичка.

ТЕКУЩАЯ ТЕМА УРОКА: «{lesson_title}» (topic: {topic})
СЛОЖНОСТЬ: {difficulty} ({hints_map.get(difficulty, '')})
{prev_block}{forbidden_block}
ТРЕБОВАНИЯ:
- Задача проверяет ТОЛЬКО тему «{lesson_title}» — ничего сложнее
- Решение должно умещаться в знания из пройденных тем + текущей темы
- Конкретные входные/выходные данные для тест-кейсов

ПРАВИЛА ДЛЯ TEST_CASES (строго соблюдать):
- "input" — это то, что передаётся в stdin (то, что студент вводит через клавиатуру).
  Несколько значений разделяются символом \\n (например "5\\n10").
  Если ввод не нужен — пустая строка "".
- "expected_output" — ТОЛЬКО то, что программа выводит через print().
  НЕ включай текст из input("подсказка") — это не часть вывода.
  Например: input("Введите имя: ") + print(f"Привет, {{name}}!") →
  input="Аня", expected_output="Привет, Аня!" (без "Введите имя:")
- Добавляй 2-3 разных тест-кейса с разными входными данными.

Верни ТОЛЬКО JSON без лишнего текста:
{{
  "title": "Короткое название задачи",
  "description": "Условие задачи с примерами ввода и вывода",
  "hints": ["подсказка 1", "подсказка 2"],
  "test_cases": [
    {{"input": "ввод", "expected_output": "вывод"}},
    {{"input": "ввод2", "expected_output": "вывод2"}}
  ],
  "solution_template": "# Напишите решение здесь\\n",
  "category": "{topic}"
}}"""

        resp = await self._chat(system, prompt)
        return self._parse_json(resp, {
            "title": f"Задача по теме: {lesson_title}",
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
            "Оценивай код по критериям: правильность логики, читаемость, эффективность. "
            "ВАЖНО: Не придирайся к формату ввода (input/split/отдельные строки) — это не ошибка. "
            "Если код проходит тесты — он правильный, даже если стиль ввода отличается от примера. "
            "Фокусируйся на логике, алгоритмах, именовании переменных. "
            "Отвечай на русском языке, только валидным JSON."
        )
        status  = "ПРАВИЛЬНО" if is_correct else "НЕПРАВИЛЬНО"
        t_str   = f"{execution_time_ms:.1f}мс" if execution_time_ms else "?"
        err_str = f"\nОшибка: {error}" if error else ""

        prompt = f"""Проанализируй код студента:

ЗАДАЧА: {task_description[:400]}
КОД:
```python
{code[:1200]}
```
Статус тестов: {status} | Время выполнения: {t_str}{err_str}

КРИТЕРИИ ОЦЕНКИ:
- Если тесты пройдены (статус ПРАВИЛЬНО) — код рабочий, ставь 80-100 баллов
- Если тесты не пройдены — ставь 20-50 баллов в зависимости от логики
- Формат ввода (input().split() vs два input()) НЕ является ошибкой
- Смотри на логику, алгоритм, читаемость, а не на стиль ввода

Верни JSON:
{{
  "feedback": "подробный разбор 2-3 абзаца: что правильно, что можно улучшить",
  "score": 85,
  "recommendations": ["конкретный совет 1", "конкретный совет 2"],
  "style_issues": ["если есть проблемы с именованием/стилем"],
  "performance_note": "заметка по производительности если есть"
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
