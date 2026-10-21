"""Figures for the three-part 'System Design' theory guides in target/.
Every figure is computed from a formula or a simulation; toy assumptions are written on the figure.
Run:  py -3.12 figures/system_design_theory/make_figs.py
"""
import sys, os, hashlib, bisect, random
from math import comb, log, exp
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _style import *

OUT = out_dir(__file__)
random.seed(7)
rng = np.random.default_rng(7)


def note(ax, text, loc=(0.02, 0.97)):
    ax.text(*loc, text, transform=ax.transAxes, fontsize=8, color=GRAY, va="top",
            bbox=dict(fc="white", ec=LIGHT, pad=3))


# ---------------------------------------------------------------- Part 1
def fig01_latency_ladder():
    items = [("L1 cache reference", 1), ("L2 cache reference", 4), ("Mutex lock/unlock", 17),
             ("Main memory (RAM) reference", 100), ("Compress 1 KB (fast codec)", 2_000),
             ("NVMe SSD random 4 KB read", 20_000), ("Read 1 MB sequentially from SSD", 150_000),
             ("Round trip inside one datacenter", 500_000), ("HDD disk seek", 5_000_000),
             ("Round trip US East <-> Europe", 80_000_000), ("Round trip US <-> Australia", 200_000_000)]
    names = [i[0] for i in items][::-1]; vals = [i[1] for i in items][::-1]
    fig, ax = plt.subplots(figsize=(9, 5.2))
    cols = [BLUE if v < 1e3 else (PURPLE if v < 1e6 else (AMBER if v < 1e7 else RED)) for v in vals]
    ax.barh(names, vals, color=cols)
    ax.set_xscale("log"); ax.set_xlabel("Time (nanoseconds, log scale)")
    ax.grid(axis="x", alpha=0.3)
    for y, v in enumerate(vals):
        lab = f"{v:g} ns" if v < 1e3 else (f"{v/1e3:g} µs" if v < 1e6 else f"{v/1e6:g} ms")
        ax.text(v * 1.3, y, lab, va="center", fontsize=8)
    ax.set_xlim(0.5, 3e9)
    ax.set_title("Latency ladder: each colour band is ~1000× slower than the last")
    note(ax, "Approximate orders of magnitude for 2020s hardware\n(after Jeff Dean / Colin Scott tables). Not benchmarks.", (0.52, 0.97))
    save(fig, OUT, "fig01_latency_ladder.png")


def fig02_handshakes():
    names = ["TCP + TLS 1.2", "TCP + TLS 1.3", "QUIC (HTTP/3)\nfirst visit", "QUIC 0-RTT\nresumed"]
    rtts = [4, 3, 2, 1]
    fig, ax = plt.subplots(figsize=(7.5, 4))
    b = ax.bar(names, [r * 100 for r in rtts], color=[RED, AMBER, BLUE, GREEN])
    for bar, r in zip(b, rtts):
        ax.text(bar.get_x() + bar.get_width() / 2, r * 100 + 8, f"{r} RTT = {r*100} ms", ha="center", fontsize=9)
    ax.set_ylabel("Time until the response arrives (ms)"); ax.set_ylim(0, 470); ax.grid(axis="y", alpha=0.3)
    ax.set_title("Round trips before the first response byte (RTT = 100 ms)")
    note(ax, "Counts handshake round trips + 1 for the request itself.\nAssumes no packet loss.", (0.55, 0.97))
    save(fig, OUT, "fig02_handshake_rtts.png")


def fig03_bloom():
    bpk = np.linspace(2, 20, 200)
    fig, ax = plt.subplots(figsize=(7.5, 4.3))
    for k, c in [(1, GRAY), (3, AMBER), (7, BLUE)]:
        ax.plot(bpk, (1 - np.exp(-k / bpk)) ** k, color=c, lw=1.6, label=f"k = {k} hash functions")
    kopt = np.maximum(1, np.round(bpk * log(2)))
    ax.plot(bpk, (1 - np.exp(-kopt / bpk)) ** kopt, color=GREEN, lw=2.4, label="best k = round(0.69 × bits/key)")
    # simulation points
    n = 5000
    xs, ys = [], []
    for b in [4, 6, 8, 10, 12, 14]:
        m = b * n; k = max(1, round(b * log(2))); bits = np.zeros(m, bool)
        def idx(s):
            h = hashlib.sha256(s.encode()).digest()
            a = int.from_bytes(h[:8], "big"); c = int.from_bytes(h[8:16], "big")
            return [(a + i * c) % m for i in range(k)]
        for i in range(n): bits[idx(str(i))] = True
        fp = np.mean([bits[idx("q" + str(i))].all() for i in range(40000)])
        xs.append(b); ys.append(max(fp, 1e-5))
    ax.scatter(xs, ys, color=RED, zorder=5, s=30, label="simulation (5,000 keys)")
    ax.set_yscale("log"); ax.set_xlabel("Bits of memory per stored key (m/n)"); ax.set_ylabel("False-positive rate")
    ax.axhline(0.01, color=GRAY, ls=":", lw=1); ax.text(19.8, 0.012, "1%", ha="right", fontsize=8, color=GRAY)
    ax.grid(alpha=0.3); ax.legend(fontsize=8, loc="lower left")
    ax.set_title("Bloom filter: ~10 bits per key buys a 1% false-positive rate")
    save(fig, OUT, "fig03_bloom_filter.png")


# ---------------------------------------------------------------- Part 2
def quorum(N, W, p):
    return sum(comb(N, i) * p ** i * (1 - p) ** (N - i) for i in range(W, N + 1))


def fig04_quorum():
    p = np.linspace(0.90, 0.999, 200)
    fig, ax = plt.subplots(figsize=(7.5, 4.3))
    for N, W, c, lab in [(1, 1, GRAY, "1 node"), (3, 3, RED, "N=3, need all 3"),
                         (3, 2, BLUE, "N=3, majority 2"), (5, 3, GREEN, "N=5, majority 3")]:
        ax.plot(p, [1 - quorum(N, W, x) for x in p], color=c, lw=2, label=lab)
    ax.set_yscale("log")
    ax.set_xlabel("Availability of each single node"); ax.set_ylabel("Probability the operation is UNavailable")
    ax.grid(alpha=0.3); ax.legend(fontsize=8, loc="center left")
    ax.set_title("Majority quorums turn unreliable nodes into a reliable system")
    note(ax, "Assumes nodes fail independently.\nAt p = 0.99: 1 node 1e-2, N=3 maj 3e-4, N=5 maj 1e-5", (0.02, 0.14))
    save(fig, OUT, "fig04_quorum_availability.png")


def fig05_rehash():
    K = 60000
    Ns = list(range(2, 21))
    mod = [sum(1 for k in range(K) if k % N != k % (N + 1)) / K for N in Ns]
    ideal = [1 / (N + 1) for N in Ns]
    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.plot(Ns, mod, "o-", color=RED, label="hash(key) mod N  (measured)")
    ax.plot(Ns, ideal, "o-", color=GREEN, label="consistent hashing ≈ 1/(N+1)")
    ax.set_xlabel("Servers before adding one (N → N+1)"); ax.set_ylabel("Fraction of keys that must move")
    ax.set_ylim(0, 1); ax.grid(alpha=0.3); ax.legend(fontsize=8)
    ax.set_title("Adding one server: modulo moves almost everything")
    save(fig, OUT, "fig05_rehash_moved.png")


def fig06_vnodes():
    nodes = list(range(10)); keys = 60000
    khash = [int(hashlib.md5(f"k{i}".encode()).hexdigest(), 16) for i in range(keys)]
    vs = [1, 2, 5, 10, 20, 50, 100, 200, 400]; mx = []
    for v in vs:
        pts = sorted((int(hashlib.md5(f"{n}-{i}".encode()).hexdigest(), 16), n) for n in nodes for i in range(v))
        hs = [p[0] for p in pts]; c = [0] * 10
        for h in khash: c[pts[bisect.bisect(hs, h) % len(pts)][1]] += 1
        mx.append(max(c) / (keys / 10))
    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.plot(vs, mx, "o-", color=BLUE)
    ax.axhline(1, color=GREEN, ls="--", lw=1); ax.text(400, 1.02, "perfect balance", ha="right", fontsize=8, color=GREEN)
    ax.set_xscale("log"); ax.set_xlabel("Virtual nodes per server (log scale)")
    ax.set_ylabel("Busiest server ÷ average load"); ax.grid(alpha=0.3)
    ax.set_title("Virtual nodes even out a consistent-hash ring (10 servers)")
    note(ax, "Simulation: 60,000 keys, MD5 positions.", (0.55, 0.97))
    save(fig, OUT, "fig06_vnode_balance.png")


def fig07_gossip():
    fig, ax = plt.subplots(figsize=(7.5, 4))
    for N, c in [(100, GREEN), (1000, BLUE), (10000, PURPLE)]:
        for t in range(15):
            inf = np.zeros(N, bool); inf[0] = True; hist = [1]
            while hist[-1] < N:
                senders = np.flatnonzero(inf)
                inf[rng.integers(0, N, len(senders))] = True
                hist.append(inf.sum())
            ax.plot(range(len(hist)), np.array(hist) / N, color=c, alpha=0.25, lw=1)
        ax.plot([], [], color=c, label=f"N = {N:,}  (log₂N + ln N ≈ {log(N,2)+log(N):.0f} rounds)")
    ax.set_xlabel("Gossip round (each informed node tells 1 random node)"); ax.set_ylabel("Fraction of nodes informed")
    ax.grid(alpha=0.3); ax.legend(fontsize=8, loc="lower right")
    ax.set_title("Gossip spreads in O(log N) rounds: 100× more nodes ≈ +11 rounds")
    note(ax, "15 simulated runs per size.", (0.02, 0.97))
    save(fig, OUT, "fig07_gossip_spread.png")


# ---------------------------------------------------------------- Part 3
def fig08_mm1():
    rho = np.linspace(0, 0.97, 300)
    fig, ax = plt.subplots(figsize=(7.5, 4.3))
    ax.plot(rho * 100, 10 / (1 - rho), color=BLUE, lw=2, label="mean time in system")
    ax.plot(rho * 100, 10 / (1 - rho) * log(100), color=RED, lw=2, ls="--", label="99th percentile (≈ 4.6× mean)")
    for r in [0.5, 0.8, 0.9]:
        ax.scatter([r * 100], [10 / (1 - r)], color=BLUE, zorder=5)
        ax.text(r * 100 - 2, 10 / (1 - r) + 25, f"{r:.0%}: {10/(1-r):.0f} ms", fontsize=8, ha="right")
    ax.set_ylim(0, 600); ax.set_xlabel("Server utilisation ρ (%)"); ax.set_ylabel("Latency (ms)")
    ax.grid(alpha=0.3); ax.legend(fontsize=8, loc="upper left")
    ax.set_title("Queueing: latency explodes as utilisation approaches 100%")
    note(ax, "M/M/1 model, service time 10 ms.\nW = S / (1 − ρ)", (0.02, 0.75))
    save(fig, OUT, "fig08_queue_latency.png")


def fig09_scaling():
    N = np.arange(1, 129)
    fig, ax = plt.subplots(figsize=(7.5, 4.3))
    ax.plot(N, N, color=GRAY, ls=":", label="linear (ideal)")
    ax.plot(N, 1 / (0.05 + 0.95 / N), color=BLUE, lw=2, label="Amdahl, 5% serial (cap 20×)")
    s, k = 0.05, 0.001
    usl = N / (1 + s * (N - 1) + k * N * (N - 1))
    ax.plot(N, usl, color=RED, lw=2, label="USL, σ=0.05, κ=0.001")
    pk = int(np.argmax(usl)); ax.scatter([N[pk]], [usl[pk]], color=RED, zorder=5)
    ax.text(N[pk] + 3, usl[pk] + 0.8, f"peak at N≈{N[pk]} ({usl[pk]:.1f}×)\nthen MORE nodes = LESS throughput", fontsize=8, color=RED)
    ax.set_ylim(0, 25); ax.set_xlabel("Number of workers / nodes N"); ax.set_ylabel("Speed-up vs one worker")
    ax.grid(alpha=0.3); ax.legend(fontsize=8, loc="upper left")
    ax.set_title("Why adding machines stops helping")
    save(fig, OUT, "fig09_scalability_laws.png")


def fig10_fanout():
    n = np.arange(1, 201)
    fig, ax = plt.subplots(figsize=(7.5, 4))
    for p, c in [(0.99, BLUE), (0.999, GREEN), (0.9999, PURPLE)]:
        ax.plot(n, 1 - p ** n, color=c, lw=2, label=f"each backend slow {1-p:.2%} of the time")
    ax.scatter([100], [1 - 0.99 ** 100], color=RED, zorder=5)
    ax.text(108, 0.47, "fan-out 100, p99 backends:\n63% of user requests hit a slow one", fontsize=8, color=RED)
    ax.set_xlabel("Backends one user request waits for (fan-out)"); ax.set_ylabel("P(user request is slow)")
    ax.set_ylim(0, 1); ax.grid(alpha=0.3); ax.legend(fontsize=8, loc="upper left")
    ax.set_title("Tail at scale: rare slowness becomes common under fan-out")
    save(fig, OUT, "fig10_tail_fanout.png")


def fig11_jitter():
    C = 1000; base = 100; attempts = 4
    bins = np.arange(0, 1700, 20)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
    for ax, mode, col in [(axes[0], "none", RED), (axes[1], "full", GREEN)]:
        times = []
        for _ in range(C):
            t = 0
            for a in range(attempts):
                d = base * 2 ** a
                t += d if mode == "none" else rng.uniform(0, d)
                times.append(t)
        ax.hist(times, bins=bins, color=col, alpha=0.85)
        ax.set_xlabel("Time after the outage (ms)"); ax.grid(alpha=0.3)
        ax.set_title("No jitter: synchronized retry waves" if mode == "none" else "Full jitter: retries spread out")
    axes[0].set_ylabel("Retries arriving per 20 ms")
    note(axes[1], "Toy: 1,000 clients fail at t=0, retry 4×,\nbackoff 100·2ᵃ ms. Every retry fails.", (0.40, 0.97))
    save(fig, OUT, "fig11_retry_jitter.png")


def fig12_kv():
    ctx = np.array([1, 4, 8, 16, 32, 64, 128]) * 1024
    per_gqa = 2 * 80 * 8 * 128 * 2; per_mha = 2 * 80 * 64 * 128 * 2
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.plot(ctx / 1024, ctx * per_mha / 2 ** 30, "o-", color=RED, label="64 KV heads (classic multi-head)")
    ax.plot(ctx / 1024, ctx * per_gqa / 2 ** 30, "o-", color=BLUE, label="8 KV heads (grouped-query)")
    ax.axhline(20, color=AMBER, ls="--"); ax.text(127, 8, "≈20 GB left for KV cache on 2×80 GB GPUs after FP16 weights", fontsize=8, color=AMBER, ha="right", va="top")
    ax.set_yscale("log"); ax.set_xlabel("Context length per request (thousand tokens)")
    ax.set_ylabel("KV cache for ONE request (GiB)"); ax.grid(alpha=0.3); ax.legend(fontsize=8, loc="lower right")
    ax.set_title("LLM serving: KV-cache memory, not compute, limits batch size")
    fig.text(0.5, -0.04, "Assumed 70B-class shape: 80 layers, head dim 128, FP16.  Bytes per token = 2 × layers × KV heads × head dim × 2.", ha="center", fontsize=8, color=GRAY)
    save(fig, OUT, "fig12_kv_cache.png")


if __name__ == "__main__":
    for f in [fig01_latency_ladder, fig02_handshakes, fig03_bloom, fig04_quorum, fig05_rehash, fig06_vnodes,
              fig07_gossip, fig08_mm1, fig09_scaling, fig10_fanout, fig11_jitter, fig12_kv]:
        f()
