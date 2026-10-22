"""Small runnable demos quoted in the three 'System Design' theory guides (target/).
No dependencies beyond the standard library.  Run:  py -3.12 code/system_design_theory.py
"""
import hashlib, math, random


# ---------------------------------------------------------------- Part 1: Bloom filter
class BloomFilter:
    def __init__(self, n_items, fp_rate):
        self.m = math.ceil(-n_items * math.log(fp_rate) / math.log(2) ** 2)  # bits
        self.k = max(1, round(self.m / n_items * math.log(2)))                # hash functions
        self.bits = bytearray(self.m)

    def _positions(self, item):
        d = hashlib.sha256(item.encode()).digest()
        a, b = int.from_bytes(d[:8], "big"), int.from_bytes(d[8:16], "big")
        return [(a + i * b) % self.m for i in range(self.k)]   # double hashing

    def add(self, item):
        for p in self._positions(item):
            self.bits[p] = 1

    def might_contain(self, item):
        return all(self.bits[p] for p in self._positions(item))


def demo_bloom():
    bf = BloomFilter(n_items=100_000, fp_rate=0.01)
    for i in range(100_000):
        bf.add(f"user:{i}")
    misses = sum(not bf.might_contain(f"user:{i}") for i in range(100_000))
    fps = sum(bf.might_contain(f"other:{i}") for i in range(100_000))
    print(f"bits={bf.m:,} ({bf.m/8/1024:.0f} KiB), k={bf.k}")
    print(f"false negatives: {misses}   false positives: {fps/100_000:.2%}")


# ---------------------------------------------------------------- Part 2: vector clocks
def vc_merge(a, b):
    return {n: max(a.get(n, 0), b.get(n, 0)) for n in a.keys() | b.keys()}


def vc_compare(a, b):
    nodes = a.keys() | b.keys()
    le = all(a.get(n, 0) <= b.get(n, 0) for n in nodes)
    ge = all(a.get(n, 0) >= b.get(n, 0) for n in nodes)
    if le and ge: return "equal"
    if le: return "a happened before b"
    if ge: return "b happened before a"
    return "CONCURRENT (conflict)"


def demo_vector_clocks():
    base = {"A": 1}                       # A writes v1
    b_write = vc_merge(base, {"B": 1})    # B read v1, then wrote v2
    c_write = vc_merge(base, {"C": 1})    # C read v1, then wrote v3 (never saw v2)
    print("v1 vs v2:", vc_compare(base, b_write))
    print("v2 vs v3:", vc_compare(b_write, c_write))
    merged = vc_merge(b_write, c_write); merged["B"] += 1   # B resolves the conflict
    print("resolved clock:", dict(sorted(merged.items())), "| v3 vs resolved:", vc_compare(c_write, merged))


# ---------------------------------------------------------------- Part 2: idempotency keys
class PaymentService:
    def __init__(self):
        self.results = {}    # idempotency_key -> stored response (in real life: a DB table, same transaction)
        self.balance = 100

    def charge(self, idem_key, amount):
        if idem_key in self.results:          # retry of a request we already did
            return self.results[idem_key]
        self.balance -= amount
        resp = {"status": "charged", "amount": amount, "balance": self.balance}
        self.results[idem_key] = resp
        return resp


def demo_idempotency():
    svc = PaymentService()
    for attempt in range(3):                  # client times out and retries the SAME key
        print("attempt", attempt + 1, svc.charge("order-42", 30))


# ---------------------------------------------------------------- Part 3: retry with full jitter
def backoff_full_jitter(attempt, base=0.1, cap=10.0, rng=random):
    """Seconds to sleep before retry number `attempt` (0-based)."""
    return rng.uniform(0, min(cap, base * 2 ** attempt))


def demo_jitter():
    rng = random.Random(3)
    print("sleeps (s):", [round(backoff_full_jitter(a, rng=rng), 3) for a in range(6)])


# ---------------------------------------------------------------- Part 4: token bucket rate limiter
class TokenBucket:
    """In production this state lives in Redis and the update runs atomically (a Lua script)."""
    def __init__(self, capacity, refill_per_s):
        self.capacity, self.rate = capacity, refill_per_s
        self.tokens, self.last = capacity, 0.0

    def allow(self, now):
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)  # lazy refill
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


def demo_token_bucket():
    tb = TokenBucket(capacity=10, refill_per_s=5)
    burst = [tb.allow(0.0) for _ in range(12)]
    print("burst of 12 at t=0.0s: allowed", sum(burst), "rejected", 12 - sum(burst))
    later = [tb.allow(0.6) for _ in range(4)]
    print("4 more at t=0.6s:      allowed", sum(later), "rejected", 4 - sum(later))


if __name__ == "__main__":
    for d in (demo_bloom, demo_vector_clocks, demo_idempotency, demo_jitter, demo_token_bucket):
        print(f"--- {d.__name__}"); d()
