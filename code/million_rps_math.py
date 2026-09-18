"""The arithmetic behind '1 million requests per second' — all of it runnable.

1. Bandwidth: what payload size can you serve at 1M req/s on a given network card?
2. Little's Law: how much concurrency does 1M req/s need?
3. CPU budget: how many microseconds of CPU may one request use?
4. Measured: ORDER BY RANDOM() vs index lookup as a table grows (the O(n) lesson)
5. UUID collisions via the birthday paradox
6. Rare events: at 1M req/s, how often does a "one in a million" event happen?
"""
import math, sqlite3, time

# ------------------------------------------------------------------ 1. bandwidth
def bandwidth():
    print("1. BANDWIDTH ---------------------------------------------------------")
    for payload_kb in (0.02, 1, 30):
        gbps = 1_000_000 * payload_kb * 1024 * 8 / 1e9
        print(f"   1M req/s x {payload_kb:>5} KB = {gbps:8.1f} Gbit/s "
              f"({gbps/8:6.1f} GB/s)  -> needs a {'10' if gbps<10 else '100' if gbps<100 else '400+'} Gbit-class NIC")
    for nic_gbps in (10, 50, 100, 600):
        max_kb = nic_gbps * 1e9 / 8 / 1_000_000 / 1024
        print(f"   a {nic_gbps:>3} Gbit/s card at 1M req/s allows a payload of at most {max_kb:6.1f} KB")

# ------------------------------------------------------------------ 2. Little's Law
def littles_law():
    print("\n2. LITTLE'S LAW  (concurrency = throughput x latency) ------------------")
    for ms in (0.5, 1, 5, 50, 200):
        print(f"   at 1,000,000 req/s and {ms:>5} ms per request -> {1_000_000 * ms / 1000:>10,.0f} requests in flight")
    print("   the video's final test: 60 machines x 400 connections x 5 pipelining = "
          f"{60*400*5:,} in flight")

# ------------------------------------------------------------------ 3. CPU budget
def cpu_budget():
    print("\n3. CPU BUDGET --------------------------------------------------------")
    for cores in (12, 128, 192):
        us = cores * 1e6 / 1_000_000
        print(f"   {cores:>4} cores at 1M req/s -> {us:6.1f} us of CPU per request "
              f"(a Python dict lookup is ~0.05 us; parsing 30 KB of JSON is ~100 us)")

# ------------------------------------------------------------------ 4. measured: O(n) vs index
def query_complexity():
    print("\n4. MEASURED: ORDER BY RANDOM() vs INDEX LOOKUP ------------------------")
    print("   rows        ORDER BY RANDOM()    MAX(id)+lookup     slowdown")
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE codes(id INTEGER PRIMARY KEY, code TEXT)")
    inserted = 0
    for rows in (10_000, 100_000, 1_000_000):
        db.executemany("INSERT INTO codes(code) VALUES (?)",
                       ((f"code{i}",) for i in range(inserted, rows)))
        db.commit(); inserted = rows
        t0 = time.perf_counter()
        for _ in range(3):
            db.execute("SELECT id, code FROM codes ORDER BY RANDOM() LIMIT 1").fetchone()
        t_rand = (time.perf_counter() - t0) / 3 * 1000
        t0 = time.perf_counter()
        for _ in range(3):
            mx = db.execute("SELECT MAX(id) FROM codes").fetchone()[0]
            db.execute("SELECT id, code FROM codes WHERE id = ?", (mx // 2,)).fetchone()
        t_idx = (time.perf_counter() - t0) / 3 * 1000
        print(f"   {rows:>9,}   {t_rand:>12.2f} ms   {t_idx:>12.4f} ms   {t_rand/t_idx:>10,.0f}x")
    print("   ORDER BY RANDOM() scans and sorts the WHOLE table for every request: O(n log n).")
    print("   Caveat for MAX(id)+random: gaps from deleted rows mean a miss, so retry or keep a dense id map.")

# ------------------------------------------------------------------ 5. birthday paradox
def uuid_collisions():
    print("\n5. UUID COLLISIONS (birthday paradox) ---------------------------------")
    N = 2 ** 122                                   # random bits in a UUIDv4
    n_50 = math.sqrt(2 * N * math.log(2))          # count for a 50% chance of one collision
    rate = 1_000_000
    years = n_50 / rate / (365.25 * 24 * 3600)
    print(f"   UUIDv4 has 122 random bits -> {N:.3e} possible values")
    print(f"   50% chance of ONE collision after {n_50:.3e} UUIDs")
    print(f"   generating 1,000,000 per second, that takes {years:,.0f} years")
    for n in (1e12, 1e15, 1e18):
        p = 1 - math.exp(-n * n / (2 * N))
        print(f"   after {n:.0e} UUIDs, collision probability ~= {p:.2e}")

# ------------------------------------------------------------------ 6. rare events
def rare_events():
    print("\n6. RARE EVENTS AT SCALE ----------------------------------------------")
    rps = 1_000_000
    for odds in (1e6, 1e9, 1e12):
        per_day = rps * 86400 / odds
        every = odds / rps
        print(f"   a 1-in-{odds:.0e} event happens {per_day:>12,.2f} times per day "
              f"(once every {every:>10,.1f} s)")
    print("   This is why 'it only fails one time in a million' is not a defence at this scale.")

if __name__ == "__main__":
    bandwidth(); littles_law(); cpu_budget(); query_complexity(); uuid_collisions(); rare_events()
