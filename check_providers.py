import asyncio, g4f, inspect
from g4f.client import AsyncClient

TEST_MESSAGE = [{"role": "user", "content": "Say OK"}]

async def test_provider(name, provider):
    for model in ["gpt-4o-mini", "gpt-4o", "openai", "openai-large", "openai-fast", "blackboxai"]:
        try:
            client = AsyncClient(provider=provider)
            resp = await asyncio.wait_for(
                client.chat.completions.create(model=model, messages=TEST_MESSAGE),
                timeout=12
            )
            text = (resp.choices[0].message.content or "").strip()
            if text and "log in" not in text[:30].lower() and "[" not in text[:5]:
                return (name, model, "✅ OK", text[:40])
        except asyncio.TimeoutError:
            return (name, model, "⏱ timeout", "")
        except Exception as e:
            err = str(e)[:50]
            if "not supported" in err or "not found" in err or "No model" in err:
                continue
            return (name, model, f"❌ {err}", "")
    return (name, "-", "⚠️ нет моделей", "")

async def main():
    providers = [(n, getattr(g4f.Provider, n)) for n in dir(g4f.Provider)
                 if not n.startswith("_") and inspect.isclass(getattr(g4f.Provider, n))]
    print(f"{'Провайдер':<28} {'Модель':<22} Статус")
    print("-"*80)
    working = []
    for i in range(0, len(providers), 8):
        batch = providers[i:i+8]
        results = await asyncio.gather(*[test_provider(n, p) for n, p in batch])
        for name, model, status, resp in results:
            if "✅" in status:
                print(f"{name:<28} {model:<22} {status}  {resp}")
                working.append((name, model))
    print(f"\n✅ РАБОЧИЕ ({len(working)}):")
    for n, m in working:
        print(f'    ("{n}", "{m}"),')

asyncio.run(main())
