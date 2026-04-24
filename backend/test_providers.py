"""
Тест ВСЕХ провайдеров gpt4free.
Список берётся динамически из установленной библиотеки g4f.
Каждый провайдер проверяется 3 раза с реальным JSON-запросом.
"""
import asyncio
import json
import re
import time
import g4f
import g4f.Provider
from g4f.client import AsyncClient

SYSTEM = (
    "Ты преподаватель Python. "
    "НЕ представляйся. "
    "Отвечай ТОЛЬКО валидным JSON без какого-либо текста до или после."
)
PROMPT = (
    'Создай краткую теорию про print() в Python. '
    'Верни ТОЛЬКО JSON: {"theory": "текст", "examples": [{"title":"...","code":"...","explanation":"..."}]}'
)

ATTEMPTS = 3
TIMEOUT = 25


def is_valid_json_response(text: str) -> bool:
    if not text or len(text) < 10:
        return False
    fence = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    candidate = fence.group(1) if fence else text
    start = candidate.find('{')
    end = candidate.rfind('}') + 1
    if start == -1 or end <= start:
        return False
    try:
        data = json.loads(candidate[start:end])
        return "theory" in data and len(data.get("theory", "")) > 20
    except Exception:
        return False


def is_junk(text: str) -> str | None:
    """Возвращает причину если ответ — мусор, иначе None."""
    if not text:
        return "пустой ответ"
    tl = text.lower()
    if tl.startswith("<!doctype") or tl.startswith("<html"):
        return "HTML вместо ответа"
    if "log in" in tl[:80] or "sign in" in tl[:80]:
        return "редирект на логин"
    if text.startswith("data:") or text.startswith("[AI"):
        return "ошибка провайдера"
    if len(text) < 5:
        return f"слишком короткий: {text!r}"
    return None


async def test_provider(provider) -> dict:
    name = provider.__name__ if hasattr(provider, '__name__') else str(provider)
    ok = 0
    errors = []

    for attempt in range(1, ATTEMPTS + 1):
        try:
            client = AsyncClient(provider=provider)
            resp = await asyncio.wait_for(
                client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": SYSTEM},
                        {"role": "user",   "content": PROMPT},
                    ],
                ),
                timeout=TIMEOUT,
            )
            text = (resp.choices[0].message.content or "").strip()

            junk = is_junk(text)
            if junk:
                errors.append(f"#{attempt}: {junk}")
                continue

            if not is_valid_json_response(text):
                errors.append(f"#{attempt}: не JSON ({text[:70]}...)")
                continue

            ok += 1

        except asyncio.TimeoutError:
            errors.append(f"#{attempt}: таймаут {TIMEOUT}с")
        except Exception as e:
            errors.append(f"#{attempt}: {str(e)[:100]}")

        if attempt < ATTEMPTS:
            await asyncio.sleep(2)

    return {"name": name, "ok": ok, "errors": errors}


def get_all_providers():
    """Получить все провайдеры из g4f динамически."""
    providers = []
    for name in dir(g4f.Provider):
        if name.startswith("_"):
            continue
        obj = getattr(g4f.Provider, name)
        # Берём только классы-провайдеры
        try:
            if (isinstance(obj, type)
                    and hasattr(obj, 'create_completion')
                    and name not in ('BaseProvider', 'AsyncProvider', 'AbstractProvider',
                                     'AsyncGeneratorProvider', 'ProviderModelMixin',
                                     'RaiseErrorProvider', 'NeedAuthProvider')):
                providers.append(obj)
        except Exception:
            pass
    return providers


async def main():
    providers = get_all_providers()
    print(f"Найдено провайдеров в g4f: {len(providers)}")
    print(f"Тестируем каждый по {ATTEMPTS} попытки с реальным JSON-запросом\n")
    print(f"{'Провайдер':<30} {'OK':>4} {'Fail':>6}  Статус")
    print("-" * 70)

    reliable = []
    unstable = []

    for provider in providers:
        name = provider.__name__ if hasattr(provider, '__name__') else str(provider)
        print(f"  {name:<28} ...", end="", flush=True)
        t0 = time.time()

        result = await test_provider(provider)

        elapsed = time.time() - t0
        ok = result["ok"]
        fail = ATTEMPTS - ok

        if ok == ATTEMPTS:
            status = "✓ НАДЁЖНЫЙ"
            reliable.append(name)
        elif ok >= 1:
            status = f"~ нестабильный ({ok}/{ATTEMPTS})"
            unstable.append((name, ok))
        else:
            status = "✗ не работает"

        print(f"\r  {name:<28} {ok:>4} {fail:>6}  {status}  ({elapsed:.0f}с)")

        if result["errors"] and ok < ATTEMPTS:
            for e in result["errors"][:2]:
                print(f"    └ {e}")

        await asyncio.sleep(1)

    print("\n" + "=" * 70)
    print(f"\nНАДЁЖНЫЕ — прошли {ATTEMPTS}/{ATTEMPTS} ({len(reliable)} шт):")
    for r in reliable:
        print(f"  ✓ {r}")

    print(f"\nНЕСТАБИЛЬНЫЕ — прошли частично ({len(unstable)} шт):")
    for name, ok in sorted(unstable, key=lambda x: -x[1]):
        print(f"  ~ {name}  {ok}/{ATTEMPTS}")

    print("\nИТОГ для PROVIDER_CHAIN в ai_service.py:")
    best = reliable + [name for name, _ in unstable]
    if best:
        for b in best:
            print(f'    ("{b}", "gpt-4o-mini"),')
    else:
        print("  Ни один провайдер не прошёл тест — попробуй позже")


if __name__ == "__main__":
    asyncio.run(main())
