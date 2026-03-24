"""
Test script to check which g4f providers are working.
"""
import asyncio
import sys
from g4f.client import AsyncClient

# Providers to test
PROVIDERS_TO_TEST = [
    ("Blackbox", "gpt-4o-mini"),
    ("ChatGpt", "openai-fast"),
    ("PollinationsAI", None),  # Uses default model
    ("Mintlify", "gpt-4o-mini"),
    ("Yqcloud", "gpt-4o-mini"),
    ("OperaAria", "gpt-4o-mini"),
]

TEST_PROMPT = "Explain quantum computing in one sentence"
TIMEOUT = 15


async def test_provider(provider_name: str, model: str = None):
    """Test a single provider and return result."""
    try:
        import g4f
        provider = getattr(g4f.Provider, provider_name, None)
        
        if provider is None:
            return (provider_name, "❌", "Provider not found in g4f")
        
        client = AsyncClient(provider=provider)
        
        response = await asyncio.wait_for(
            client.chat.completions.create(
                model=model or "gpt-4o-mini",
                messages=[{"role": "user", "content": TEST_PROMPT}],
            ),
            timeout=TIMEOUT,
        )
        
        content = (response.choices[0].message.content or "").strip()
        
        if not content:
            return (provider_name, "❌", "Empty response")
        
        if content.lower().startswith("<!doctype") or content.lower().startswith("<html"):
            return (provider_name, "❌", "Returned HTML instead of text")
        
        if "authentication error" in content.lower() or "no api key" in content.lower():
            return (provider_name, "❌", "Authentication error")
        
        if content.startswith("data:"):
            return (provider_name, "❌", f"Streaming error: {content[:80]}")
        
        return (provider_name, "✅", f"OK ({len(content)} chars)")
        
    except asyncio.TimeoutError:
        return (provider_name, "❌", f"Timeout ({TIMEOUT}s)")
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            return (provider_name, "❌", f"404 Not Found")
        return (provider_name, "❌", f"{type(e).__name__}: {error_msg[:50]}")


async def main():
    print("=" * 70)
    print("G4F PROVIDER TEST")
    print("=" * 70)
    print(f"Testing {len(PROVIDERS_TO_TEST)} providers with timeout {TIMEOUT}s each")
    print(f"Test prompt: '{TEST_PROMPT}'")
    print("=" * 70)
    print()
    
    results = []
    
    for i, (provider_name, model) in enumerate(PROVIDERS_TO_TEST, 1):
        print(f"[{i}/{len(PROVIDERS_TO_TEST)}] Testing {provider_name}...", end=" ")
        sys.stdout.flush()
        
        result = await test_provider(provider_name, model)
        results.append(result)
        
        print(f"{result[1]} {result[2]}")
    
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    working = [r for r in results if r[1] == "✅"]
    failed = [r for r in results if r[1] == "❌"]
    
    if working:
        print(f"\n✅ WORKING ({len(working)}):")
        for name, _, msg in working:
            print(f"   {name}: {msg}")
    
    if failed:
        print(f"\n❌ FAILED ({len(failed)}):")
        for name, _, msg in failed:
            print(f"   {name}: {msg}")
    
    print()
    print("=" * 70)
    
    if working:
        print("\nRecommended PROVIDER_CHAIN for ai_service.py:")
        print("PROVIDER_CHAIN = [")
        for name, _, _ in working:
            model = next((m for n, m in PROVIDERS_TO_TEST if n == name), "gpt-4o-mini")
            print(f'    ("{name}", "{model}"),')
        print("]")
    else:
        print("\n⚠️  No providers working! Try updating g4f: pip install -U g4f")
    
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
