"""
Тест ВСЕХ провайдеров gpt4free.
Сканирует папку g4f/Provider/ напрямую — находит все провайдеры независимо от версии.
Каждый провайдер тестируется 3 раза с реальным JSON-запросом.
"""
import asyncio
import importlib
import inspect
import json
import os
import re
import time

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

SKIP = {
    'BaseProvider', 'AsyncProvider', 'AbstractProvider',
    'AsyncGeneratorProvider', 'ProviderModelMixin', 'IterListProvider',
    'RaiseErrorProvider', 'NeedAuthProvider', 'CreateImagesProvider',
    'RetryProvider', 'Local', 'Reka', 'BaseRetryProvider',
}


def is_valid_json(text: str) -> bool:
    if not text or len(text) < 10:
        return False
    fence = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    candidate = fence.group(1) if fence else text
    s = candidate.find('{')
    e = candidate.rfind('}') + 1
    if s == -1 or e <= s:
        return False
    try:
        d = json.loads(candidate[s:e])
        return "theory" in d and len(d.get("theory", "")) > 20
    except Exception:
        return False


def is_junk(text: str):
    if not text:
        return "пустой ответ"
    tl = text.lower()
    if tl.startswith("<!") or tl.startswith("<html"):
        return "HTML"
    if "log in" in tl[:80] or "sign in" in tl[:80]:
        return "редирект на логин"
    if text.startswith("data:") or "[AI недоступен]" in text:
        return "ошибка провайдера"
    return None


def discover_providers():
    """Сканирует файловую систему g4f и возвращает все классы провайдеров."""
    import g4f
    g4f_path = os.path.dirname(g4f.__file__)
    provider_dir = os.path.join(g4f_path, 'Provider')

    if not os.path.isdir(provider_dir):
        print(f"Папка провайдеров не найдена: {provider_dir}")
        return []

    providers = []
    seen = set()

    for root, dirs, files in os.walk(provider_dir):
        dirs[:] = [d for d in dirs if d != '__pycache__']

        for fname in files:
            if not fname.endswith('.py') or fname.startswith('_'):
                continue

            rel = os.path.relpath(os.path.join(root, fname), g4f_path)
            module_path = 'g4f.' + rel.replace(os.sep, '.')[:-3]

            try:
                mod = importlib.import_module(module_path)
            except Exception:
                continue

            for name, obj in inspect.getmembers(mod, inspect.isclass):
                if name in SKIP or name in seen:
                    continue
                if not (hasattr(obj, 'supports_gpt_4') or
                        hasattr(obj, 'models') or
                        hasattr(obj, 'create_async') or
                        hasattr(obj, 'create_completion')):
                    continue
                seen.add(name)
                providers.append((name, obj))

    return sorted(providers, key=lambda x: x[0])


async def test_one(name: str, provider) -> dict:
    ok = 0
    errors = []

    for attempt in range(1, ATTEMPTS + 1):
        try:
            from g4f.client import AsyncClient
            client = AsyncClient()
            resp = await asyncio.wait_for(
                client.chat.completions.create(
                    model="gpt-4o-mini",
                    provider=provider,
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
            if not is_valid_json(text):
                snippet = text[:80].replace('\n', ' ')
                errors.append(f"#{attempt}: не JSON — {snippet}")
                continue

            ok += 1

        except asyncio.TimeoutError:
            errors.append(f"#{attempt}: таймаут {TIMEOUT}с")
        except Exception as ex:
            errors.append(f"#{attempt}: {str(ex)[:100]}")

        if attempt < ATTEMPTS:
            await asyncio.sleep(2)

    return {"name": name, "ok": ok, "errors": errors}


async def main():
    providers = discover_providers()
    print(f"Найдено провайдеров в g4f: {len(providers)}")
    print(f"Каждый тестируется {ATTEMPTS} раза с реальным JSON-запросом\n")
    print(f"{'Провайдер':<30} {'OK':>4} {'Fail':>5}  Статус")
    print("-" * 72)

    reliable = []
    unstable = []

    for name, provider in providers:
        print(f"  {name:<28} ...", end="", flush=True)
        t0 = time.time()
        result = await test_one(name, provider)
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

        print(f"\r  {name:<28} {ok:>4} {fail:>5}  {status}  ({elapsed:.0f}с)")

        if result["errors"] and ok < ATTEMPTS:
            for e in result["errors"][:2]:
                print(f"    └ {e}")

        await asyncio.sleep(1)

    print("\n" + "=" * 72)
    print(f"\n✓ НАДЁЖНЫЕ ({len(reliable)} шт):")
    for r in reliable:
        print(f"  {r}")

    print(f"\n~ НЕСТАБИЛЬНЫЕ ({len(unstable)} шт):")
    for n, ok in sorted(unstable, key=lambda x: -x[1]):
        print(f"  {n}  ({ok}/{ATTEMPTS})")

    print("\n--- Вставь в PROVIDER_CHAIN в ai_service.py ---")
    for b in reliable + [n for n, _ in unstable]:
        print(f'    ("{b}", "gpt-4o-mini"),')


if __name__ == "__main__":
    asyncio.run(main())
