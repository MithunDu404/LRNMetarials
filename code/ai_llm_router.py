"""Demos for 'AI Engineering 6 - Production LLM Engineering' (target/ai/).
1. Retries with backoff, then fallback to a second provider (mock providers, no API keys).
2. Cost per 1,000 requests with and without routing (assumed prices).
3. Semantic-cache threshold trade-off on toy question pairs.
Run:  py -3.12 code/ai_llm_router.py
"""
import random

# ---------------------------------------------------------------- 1. retry + fallback
class ProviderError(Exception):
    def __init__(self, status): self.status = status

def make_provider(name, failures):
    script = iter(failures)
    def call(prompt):
        status = next(script, 200)
        if status != 200:
            raise ProviderError(status)
        return f"[{name}] answer"
    return call

PROVIDERS = [("primary", make_provider("primary", [429, 503, 503])),
             ("fallback", make_provider("fallback", []))]

def complete(prompt, max_retries=2, base=0.5, rng=random.Random(4)):
    for name, call in PROVIDERS:
        for attempt in range(max_retries + 1):
            try:
                out = call(prompt)
                print(f"  {name} attempt {attempt + 1}: OK")
                return out
            except ProviderError as e:
                retryable = e.status in (429, 500, 502, 503, 529)
                wait = rng.uniform(0, base * 2 ** attempt)        # full jitter (not actually slept here)
                print(f"  {name} attempt {attempt + 1}: HTTP {e.status} -> "
                      + (f"retry after {wait:.2f}s" if retryable and attempt < max_retries else "give up on this provider"))
                if not retryable:
                    break
    raise RuntimeError("all providers failed")

# ---------------------------------------------------------------- 2. cost with routing
PRICES = {"large": (3.00, 15.00), "small": (0.25, 1.25)}   # assumed $ per million input / output tokens

def cost_per_1k(model, tin=2000, tout=500):
    pin, pout = PRICES[model]
    return 1000 * (tin * pin + tout * pout) / 1e6

def demo_cost():
    large, small = cost_per_1k("large"), cost_per_1k("small")
    routed = 0.7 * small + 0.3 * large
    print(f"  all large: ${large:.2f} per 1k requests | all small: ${small:.3f}")
    print(f"  route 70% small / 30% large: ${routed:.2f}  ({1 - routed / large:.0%} cheaper than all-large)")

# ---------------------------------------------------------------- 3. semantic cache threshold
PAIRS = [  # (similarity between a new question and a cached one, is the cached answer actually right?)
    (0.97, True),   # "how do I reset my password" vs "how to reset my password"
    (0.95, True),   # "cancel my plan" vs "how can I cancel my subscription"
    (0.93, False),  # "refund policy for EU" vs "refund policy for US"
    (0.91, True),   # "change billing email" vs "update the email on my invoices"
    (0.90, False),  # "reset password on mobile" vs "reset password on desktop"
    (0.86, False),  # "upgrade to Pro" vs "downgrade from Pro"
    (0.84, True),   # "where's my invoice" vs "find past invoices"
]

def demo_cache_threshold():
    for t in (0.96, 0.92, 0.88, 0.83):
        hits = [(s, ok) for s, ok in PAIRS if s >= t]
        wrong = sum(not ok for _, ok in hits)
        print(f"  threshold {t:.2f}: cache hits {len(hits)}/{len(PAIRS)}, wrong answers served {wrong}")

if __name__ == "__main__":
    print("--- retry + fallback"); print(" ", complete("hello"))
    print("--- cost"); demo_cost()
    print("--- semantic cache threshold"); demo_cache_threshold()
