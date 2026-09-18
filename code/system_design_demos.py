"""Runnable demos for the System Design study guide (standard library only).

1. SQL injection vs parameterized queries (SQLite)
2. JWT (HS256) — build, decode, verify, tamper
3. Consistent hashing vs modulo hashing — how many keys move when a server is added
4. LRU cache hit ratio under skewed (Zipf-like) traffic
"""
import base64, hashlib, hmac, json, random, sqlite3, time
from bisect import bisect
from collections import OrderedDict

# ------------------------------------------------------------------ 1. SQL injection
def demo_sql_injection():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE users(name TEXT, password TEXT, is_admin INT)")
    db.executemany("INSERT INTO users VALUES (?,?,?)", [("alice", "s3cret", 0), ("admin", "hunter2", 1)])
    name, password = "admin' --", "anything"              # attacker-controlled input
    unsafe = f"SELECT name FROM users WHERE name = '{name}' AND password = '{password}'"
    print("[injection] unsafe query:", unsafe)
    print("[injection] unsafe result  ->", db.execute(unsafe).fetchall(), "(logged in as admin without the password!)")
    safe = db.execute("SELECT name FROM users WHERE name = ? AND password = ?", (name, password)).fetchall()
    print("[injection] parameterized ->", safe, "(input treated as data, not SQL)")

# ------------------------------------------------------------------ 2. JWT
def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def b64url_decode(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))

def jwt_encode(claims, secret):
    header = b64url(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
    payload = b64url(json.dumps(claims, separators=(",", ":")).encode())
    sig = hmac.new(secret, f"{header}.{payload}".encode(), hashlib.sha256).digest()
    return f"{header}.{payload}.{b64url(sig)}"

def jwt_verify(token, secret):
    header, payload, sig = token.split(".")
    expected = b64url(hmac.new(secret, f"{header}.{payload}".encode(), hashlib.sha256).digest())
    if not hmac.compare_digest(sig, expected):
        return None, "invalid signature"
    claims = json.loads(b64url_decode(payload))
    if claims["exp"] < time.time():
        return None, "expired"
    return claims, "ok"

def demo_jwt():
    secret = b"server-side-secret-never-sent-to-clients"
    token = jwt_encode({"sub": "user_123", "role": "editor", "scope": "posts:write",
                        "iss": "auth.example.com", "exp": int(time.time()) + 900}, secret)
    print("\n[jwt] token:", token[:60] + "...")
    print("[jwt] anyone can READ the payload (it is only base64):", json.loads(b64url_decode(token.split(".")[1])))
    print("[jwt] verify original ->", jwt_verify(token, secret)[1])
    h, p, s = token.split(".")
    forged = json.loads(b64url_decode(p)); forged["role"] = "admin"
    tampered = f"{h}.{b64url(json.dumps(forged, separators=(',', ':')).encode())}.{s}"
    print("[jwt] verify after changing role to admin ->", jwt_verify(tampered, secret)[1])

# ------------------------------------------------------------------ 3. consistent hashing
def h(key):
    return int(hashlib.md5(key.encode()).hexdigest(), 16)

class HashRing:
    def __init__(self, nodes, vnodes=100):
        self.ring = sorted((h(f"{n}#{i}"), n) for n in nodes for i in range(vnodes))
        self.points = [p for p, _ in self.ring]

    def node_for(self, key):
        return self.ring[bisect(self.points, h(key)) % len(self.ring)][1]

def demo_consistent_hashing():
    keys = [f"user:{i}" for i in range(100_000)]
    before = [f"s{i}" for i in range(4)]; after = before + ["s4"]
    moved_mod = sum(h(k) % 4 != h(k) % 5 for k in keys) / len(keys)
    r1, r2 = HashRing(before), HashRing(after)
    moved_ring = sum(r1.node_for(k) != r2.node_for(k) for k in keys) / len(keys)
    print(f"\n[hashing] add a 5th server: modulo moves {moved_mod:.0%} of keys, consistent hashing moves {moved_ring:.0%} "
          f"(ideal = 1/5 = 20%)")

# ------------------------------------------------------------------ 4. LRU cache
class LRUCache:
    def __init__(self, capacity):
        self.capacity, self.data = capacity, OrderedDict()
    def get(self, key):
        if key in self.data:
            self.data.move_to_end(key); return self.data[key]
        return None
    def put(self, key, value):
        self.data[key] = value; self.data.move_to_end(key)
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)                   # evict least recently used

def demo_cache():
    random.seed(1)
    n_items = 100_000
    weights = [1 / (i + 1) for i in range(n_items)]          # a few items are very popular (Zipf)
    requests = random.choices(range(n_items), weights=weights, k=200_000)
    for cap in (100, 1_000, 10_000):
        cache, hits = LRUCache(cap), 0
        for key in requests:
            if cache.get(key) is not None:
                hits += 1
            else:
                cache.put(key, f"row {key}")                 # cache-aside: miss -> read DB -> store
        avg_ms = (hits * 1 + (len(requests) - hits) * (1 + 50)) / len(requests)
        print(f"[cache] LRU size {cap:>6} ({cap / n_items:.1%} of items): hit ratio {hits / len(requests):.0%}, "
              f"avg latency {avg_ms:.1f} ms (cache 1 ms, DB 50 ms)")

if __name__ == "__main__":
    demo_sql_injection(); demo_jwt(); demo_consistent_hashing(); demo_cache()
