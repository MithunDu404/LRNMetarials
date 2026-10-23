"""Measure the Python performance claims that DSA advice is built on.

Run:  py -3.12 target/py/code/dsa/dsa_benchmarks.py      (about 1-2 minutes)
Each function returns data (used by images/make_dsa_figs.py) and main() prints a summary.
Timings are machine-specific; ratios and growth shapes are what carry over.
"""
from __future__ import annotations

import bisect
import heapq
import os
import random
import subprocess
import sys
import tempfile
import textwrap
import time
from collections import deque
from queue import PriorityQueue

PY = sys.executable


def best_of(fn, reps=3) -> float:
    best = float("inf")
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - t0)
    return best


# ---------------------------------------------------------------- 1. queues
def bench_queue(sizes=(1_000, 5_000, 10_000, 25_000, 50_000, 100_000, 200_000)):
    rows = []
    for n in sizes:
        def drain_list():
            q = list(range(n))
            while q:
                q.pop(0)

        def drain_deque():
            q = deque(range(n))
            while q:
                q.popleft()

        rows.append((n, best_of(drain_list, 1 if n > 50_000 else 3), best_of(drain_deque)))
    return rows


# ---------------------------------------------------------------- 2. strings
def bench_strings(sizes=(10_000, 50_000, 100_000, 200_000, 400_000)):
    rows = []
    for n in sizes:
        def plus_equals():
            s = ""
            for _ in range(n):
                s += "x"                  # CPython can resize in place: only ONE reference to s

        def plus_equals_shared():
            s = ""
            keep = []
            for i in range(n):
                s += "x"
                if i % 1000 == 0:
                    keep.append(s)        # a second reference forces a full copy next time
            return keep

        def plus_equals_aliased():
            s = ""
            for _ in range(n):
                t = s                     # alias: refcount 2, in-place resize impossible
                s = t + "x"

        def join():
            "".join(["x" for _ in range(n)])

        rows.append((n, best_of(plus_equals), best_of(plus_equals_shared),
                     best_of(plus_equals_aliased, 1), best_of(join)))
    return rows


# ---------------------------------------------------------------- 3. input reading
READERS = {
    "input() loop": "n = int(input())\ns = 0\nfor _ in range(n):\n    s += int(input())\nprint(s)",
    "sys.stdin.readline loop": "import sys\ninput = sys.stdin.readline\nn = int(input())\ns = 0\nfor _ in range(n):\n    s += int(input())\nprint(s)",
    "sys.stdin.read().split()": "import sys\ndata = sys.stdin.read().split()\nn = int(data[0])\nprint(sum(map(int, data[1:n + 1])))",
    "sys.stdin.buffer.read().split()": "import sys\ndata = sys.stdin.buffer.read().split()\nn = int(data[0])\nprint(sum(map(int, data[1:n + 1])))",
}


def bench_input(n=500_000):
    tmp = tempfile.mkdtemp()
    data_path = os.path.join(tmp, "in.txt")
    rng = random.Random(1)
    nums = [rng.randint(1, 10**9) for _ in range(n)]
    with open(data_path, "w") as f:
        f.write(f"{n}\n" + "\n".join(map(str, nums)) + "\n")
    expect = str(sum(nums))

    def run(code: str) -> float:
        script = os.path.join(tmp, "s.py")
        with open(script, "w") as f:
            f.write(code)
        best = float("inf")
        for _ in range(3):
            with open(data_path, "rb") as stdin:
                t0 = time.perf_counter()
                out = subprocess.run([PY, "-I", script], stdin=stdin, capture_output=True, text=True)
                best = min(best, time.perf_counter() - t0)
            assert out.stdout.strip() in (expect, ""), out.stderr
        return best

    startup = run("pass")
    return n, startup, {name: run(code) - startup for name, code in READERS.items()}


# ---------------------------------------------------------------- 4. priority structures
def bench_priority(n=100_000):
    rng = random.Random(3)
    vals = [rng.random() for _ in range(n)]
    results = {}

    def with_heapq():
        h = []
        for v in vals:
            heapq.heappush(h, v)
        while h:
            heapq.heappop(h)

    def with_heapify():
        h = vals[:]
        heapq.heapify(h)
        while h:
            heapq.heappop(h)

    def with_priorityqueue():
        q = PriorityQueue()
        for v in vals:
            q.put(v)
        while not q.empty():
            q.get()

    def with_insort():
        a = []
        for v in vals:
            bisect.insort(a, v)
        while a:
            a.pop()

    results["heapq push + pop"] = best_of(with_heapq)
    results["heapify + pop"] = best_of(with_heapify)
    results["queue.PriorityQueue"] = best_of(with_priorityqueue)
    results["bisect.insort list"] = best_of(with_insort)
    try:
        from sortedcontainers import SortedList

        def with_sortedlist():
            s = SortedList()
            for v in vals:
                s.add(v)
            while s:
                s.pop()

        results["SortedList"] = best_of(with_sortedlist)
    except ImportError:
        pass
    return n, results


# ---------------------------------------------------------------- 5. big integers
def bench_bignum(sizes=(1_000, 5_000, 10_000, 20_000, 40_000)):
    MOD = 10**9 + 7
    rng = random.Random(5)
    rows = []
    for n in sizes:
        arr = [rng.randint(1, 10**9) for _ in range(n)]

        def mod_each_step():
            p = 1
            for x in arr:
                p = p * x % MOD
            return p

        def mod_at_end():
            p = 1
            for x in arr:
                p *= x
            return p % MOD

        assert mod_each_step() == mod_at_end()
        rows.append((n, best_of(mod_each_step), best_of(mod_at_end, 1)))
    return rows


# ---------------------------------------------------------------- 6. recursion depth
RECURSION_SCRIPT = textwrap.dedent("""
    import sys, threading
    from functools import cache
    sys.setrecursionlimit(10**6 + 1000)
    kind, where, cap = sys.argv[1], sys.argv[2], int(sys.argv[3])

    def make():
        if kind == "plain":
            def f(n):
                return 0 if n == 0 else 1 + f(n - 1)
        elif kind == "cache":
            @cache
            def f(n):
                return 0 if n == 0 else 1 + f(n - 1)
        else:
            memo = {}
            def f(n):
                if n in memo:
                    return memo[n]
                memo[n] = r = 0 if n == 0 else 1 + f(n - 1)
                return r
        return f

    def deepest():
        lo, hi = 1, cap                    # binary search the deepest call that works
        while lo < hi:
            mid = (lo + hi + 1) // 2
            try:
                make()(mid)
                lo = mid
            except RecursionError:
                hi = mid - 1
        return lo

    if where == "thread":
        threading.stack_size(64 * 1024 * 1024)   # Windows rejected 256 MiB and 512 MiB here
        out = []
        t = threading.Thread(target=lambda: out.append(deepest()))
        t.start(); t.join()
        print(out[0])
    else:
        print(deepest())
""")


def bench_recursion(cap=1_000_000):
    """Deepest recursion that works, with sys.setrecursionlimit set far higher (10**6)."""
    tmp = tempfile.mkdtemp()
    script = os.path.join(tmp, "rec.py")
    with open(script, "w") as f:
        f.write(RECURSION_SCRIPT)
    rows = []
    for kind in ("plain", "cache", "dict"):
        for where in ("main", "thread"):
            r = subprocess.run([PY, "-I", script, kind, where, str(cap)], capture_output=True, text=True, timeout=600)
            depth = int(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip().isdigit() else 0
            rows.append((kind, where, depth))
    return cap, rows


# ---------------------------------------------------------------- 7. loop micro-costs
def bench_loops(n=1_000_000):
    data = list(range(n))
    out = {}

    def append_loop():
        r = []
        for x in data:
            r.append(x * 2)

    def append_loop_local():
        r = []
        app = r.append
        for x in data:
            app(x * 2)

    def comprehension():
        [x * 2 for x in data]

    def map_lambda():
        list(map(lambda x: x * 2, data))

    def builtin_sum():
        sum(data)

    def manual_sum():
        s = 0
        for x in data:
            s += x

    for fn in (append_loop, append_loop_local, comprehension, map_lambda, manual_sum, builtin_sum):
        out[fn.__name__] = best_of(fn)
    return n, out


def main():
    print(f"Python {sys.version.split()[0]} on {sys.platform}\n")

    print("1. Draining a queue of n items (seconds)")
    for n, lst, dq in bench_queue():
        print(f"   n={n:>7}: list.pop(0) {lst:8.4f} | deque.popleft {dq:8.4f} | ratio {lst / dq:7.1f}x")

    print("\n2. Building a string of n chars one at a time (seconds)")
    for n, pe, shared, alias, jn in bench_strings():
        print(f"   n={n:>7}: s += 'x' {pe:.4f} | with extra refs {shared:.4f} | aliased {alias:.4f} | ''.join {jn:.4f}")

    n, startup, res = bench_input()
    print(f"\n3. Reading {n:,} integers from stdin (seconds, interpreter startup {startup:.3f}s subtracted)")
    for name, t in res.items():
        print(f"   {name:<32} {t:.3f}")

    n, res = bench_priority()
    print(f"\n4. Push {n:,} random floats then pop them all (seconds)")
    for name, t in res.items():
        print(f"   {name:<22} {t:.3f}")

    print("\n5. Product of n numbers <= 1e9, mod 1e9+7 (seconds)")
    for n, step, end in bench_bignum():
        print(f"   n={n:>6}: mod every step {step:.4f} | mod at the end {end:.4f} | ratio {end / step:6.1f}x")

    cap, rows = bench_recursion()
    print(f"\n6. Deepest recursion that works (searched up to {cap:,}; recursion limit set to 10**6)")
    names = {"plain": "plain recursive function", "cache": "@functools.cache recursion", "dict": "hand-written dict memo"}
    for kind, where, depth in rows:
        print(f"   {names[kind]:<28} {where:<6} {depth:>9,}{'  (= search cap)' if depth == cap else ''}")

    n, res = bench_loops()
    print(f"\n7. Loop styles over {n:,} items (seconds)")
    for name, t in res.items():
        print(f"   {name:<18} {t:.4f}")


if __name__ == "__main__":
    main()
