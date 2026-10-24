"""Figures for the four-part 'System Design' guide (target/system-design/).
Every figure is computed from a formula or a simulation; toy assumptions are written on the figure.
Self-contained: needs only numpy and matplotlib. Writes the PNGs next to this script.
Run (from anywhere):  py -3.12 target/system-design/images/make_figs.py
"""
import os, hashlib, bisect, random
from collections import OrderedDict
from math import comb, log, exp
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, RED, GREEN, AMBER = "#2563eb", "#dc2626", "#16a34a", "#d97706"
PURPLE, GRAY, LIGHT = "#7c3aed", "#6b7280", "#e5e7eb"
plt.rcParams.update({
    "figure.dpi": 150, "savefig.bbox": "tight", "savefig.facecolor": "white",
    "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
    "axes.titleweight": "bold", "axes.titlesize": 11, "legend.frameon": False,
})
OUT = os.path.dirname(os.path.abspath(__file__))


def save(fig, out, name):
    fig.savefig(os.path.join(out, name))
    plt.close(fig)
    print("wrote", name)
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
    ax.set_title("Latency ladder: from nanoseconds (RAM) to hundreds of milliseconds (oceans)")
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


def fig13_zipf_cache():
    N = 100_000
    ranks = np.arange(1, N + 1, dtype=float)
    frac = np.logspace(-4, 0, 60)                     # cache size as a fraction of all items
    fig, ax = plt.subplots(figsize=(7.5, 4.3))
    for s, c in [(0.8, AMBER), (1.0, BLUE), (1.2, GREEN)]:
        w = ranks ** -s; cum = np.cumsum(w) / w.sum()
        ax.plot(frac * 100, [cum[max(0, int(f * N) - 1)] * 100 for f in frac], color=c, lw=2,
                label=f"ideal cache, Zipf s = {s}")
    ax.plot(frac * 100, frac * 100, color=GRAY, ls=":", label="uniform traffic (no skew)")
    # LRU simulation at s = 1.0 on the same 100k-item catalogue, to show the real-policy gap
    n2 = 100_000; r2 = np.arange(1, n2 + 1, dtype=float); p2 = r2 ** -1.0; p2 /= p2.sum()
    reqs = rng.choice(n2, size=400_000, p=p2)
    xs, ys = [], []
    for f in [0.001, 0.01, 0.05, 0.2]:
        cap = int(f * n2); lru = OrderedDict(); hits = 0
        for i, k in enumerate(reqs):
            if k in lru:
                lru.move_to_end(k)
                if i >= 100_000: hits += 1
            else:
                lru[k] = 1
                if len(lru) > cap: lru.popitem(last=False)
        xs.append(f * 100); ys.append(hits / 300_000 * 100)
    ax.scatter(xs, ys, color=RED, zorder=5, s=30, label="real LRU, s = 1.0 (simulated)")
    ax.set_xscale("log"); ax.set_xlabel("Cache size (% of all items, log scale)")
    ax.set_ylabel("Hit ratio (%)"); ax.set_ylim(0, 102); ax.grid(alpha=0.3)
    ax.legend(fontsize=8, loc="upper left")
    ax.set_title("Skewed traffic: a tiny cache serves most requests")
    note_txt = "Zipf: item of rank r is requested ∝ 1/rˢ.\nIdeal = always holds the top items (100k-item catalogue)."
    ax.text(0.98, 0.04, note_txt, transform=ax.transAxes, fontsize=8, color=GRAY, ha="right", va="bottom",
            bbox=dict(fc="white", ec=LIGHT, pad=3))
    save(fig, OUT, "fig13_zipf_cache.png")


# ---------------------------------------------------------------- added in the October 2026 audit
def _pos(name):
    """Position on a 360-degree ring from an MD5 hash (real hashing, not hand-placed)."""
    return int(hashlib.md5(name.encode()).hexdigest(), 16) % 3600 / 10.0


def _owner(angle, servers):
    pts = sorted((_pos(s), s) for s in servers)
    for a, s in pts:
        if angle <= a:
            return s
    return pts[0][1]                                   # wrap around past 360


def fig14_hash_ring():
    before = ["server-1", "server-2", "server-3", "server-4"]; after = before + ["server-5"]
    cols = dict(zip(after, [BLUE, GREEN, AMBER, PURPLE, RED]))
    keys = [f"key{i}" for i in range(120)]
    moved = [k for k in keys if _owner(_pos(k), before) != _owner(_pos(k), after)]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6))
    for ax, servers, title in [(axes[0], before, "Before: 4 servers"), (axes[1], after, "After adding server S5")]:
        t = np.linspace(0, 2 * np.pi, 400)
        ax.plot(np.cos(t), np.sin(t), color=LIGHT, lw=6, zorder=1)
        for k in keys:
            a = np.radians(90 - _pos(k)); o = _owner(_pos(k), servers)
            hl = servers is after and k in moved
            ax.scatter(np.cos(a), np.sin(a), s=55 if hl else 18, color=cols[o], zorder=3,
                       edgecolor="black" if hl else "none", lw=1.2)
        for s in servers:
            a = np.radians(90 - _pos(s))
            ax.scatter(np.cos(a), np.sin(a), marker="s", s=170, color=cols[s], zorder=4, edgecolor="white")
            ax.text(1.25 * np.cos(a), 1.25 * np.sin(a), "S" + s[-1], ha="center", va="center", fontsize=12,
                    fontweight="bold", color=cols[s])
        ax.set_xlim(-1.45, 1.45); ax.set_ylim(-1.45, 1.45); ax.set_aspect("equal"); ax.axis("off")
        ax.set_title(title)
    axes[0].text(0, 0, "Each key (dot) belongs to\nthe first server (square)\nclockwise from it",
                 ha="center", va="center", fontsize=9, color=GRAY)
    axes[1].text(0, 0, f"{len(moved)} of {len(keys)} keys moved,\nall of them to S5\n(outlined dots).\nEvery other key stayed put.",
                 ha="center", va="center", fontsize=9, color=GRAY)
    fig.text(0.5, 0.01, "Positions are real MD5 hashes of the names \"server-1\"…\"server-5\" and \"key0\"…\"key119\"; "
             "one point per server (no virtual nodes).\nhash mod N would move about 80% of the keys going from 4 to 5 servers.",
             ha="center", fontsize=8, color=GRAY)
    save(fig, OUT, "fig14_hash_ring.png")
    return len(moved), len(keys)


def fig15_watermark():
    r = np.random.default_rng(15)
    n = 160
    event = np.sort(r.uniform(0, 60, n))
    delay = r.exponential(1.5, n)                      # most events arrive within a few seconds
    strag = r.random(n) < 0.06                         # a few phones were offline for a while
    delay[strag] = r.uniform(8, 25, strag.sum())
    proc = event + delay
    lag = 5.0                                          # watermark = newest event time seen - 5 s
    order = np.argsort(proc)
    # an event is late if, when it arrives, the watermark has already passed its event time
    late = np.zeros(n, bool); mx = -1e9
    for i in order:
        if event[i] < mx - lag:
            late[i] = True
        mx = max(mx, event[i])
    tt = proc[order]; wm = np.maximum.accumulate(event[order]) - lag
    fig, ax = plt.subplots(figsize=(8.5, 5))
    for w0 in range(0, 60, 15):
        ax.axhspan(w0, w0 + 15, color=[BLUE, GREEN][(w0 // 15) % 2], alpha=0.06)
        ax.text(1, w0 + 7.5, f"window\n{w0}–{w0 + 15} s", fontsize=7.5, color=GRAY, va="center")
    ax.scatter(proc[~late], event[~late], s=14, color=BLUE, label="on-time event", zorder=3)
    ax.scatter(proc[late], event[late], s=45, color=RED, marker="x", zorder=4,
               label="late event (watermark had already passed it)")
    ax.step(tt, wm, where="post", color=AMBER, lw=2, label="watermark = newest event time seen − 5 s")
    ax.plot([0, 85], [0, 85], color=GRAY, ls=":", lw=1, label="zero delay (event time = arrival time)")
    emitted = {}
    for w_end in [15, 30, 45]:
        idx = int(np.argmax(wm >= w_end)); emitted[w_end] = round(float(tt[idx]), 1)
        ax.scatter([tt[idx]], [w_end], color=AMBER, s=60, zorder=5, edgecolor="black")
        ax.annotate(f"window ending {w_end} s\nclosed at {tt[idx]:.0f} s", (tt[idx], w_end),
                    xytext=(tt[idx] + 5, w_end - 7), fontsize=7.5, arrowprops=dict(arrowstyle="-", color=GRAY))
    ax.set_xlim(0, 85); ax.set_ylim(0, 62)
    ax.set_xlabel("Processing time: when the event reached the stream processor (s)")
    ax.set_ylabel("Event time: when it actually happened (s)")
    ax.grid(alpha=0.3); ax.legend(fontsize=7.5, loc="lower right")
    ax.set_title("Watermarks: deciding when a time window is complete")
    note(ax, f"Toy simulation: {n} events, delays mostly ~1.5 s,\n6% stragglers delayed 8–25 s. {late.sum()} arrived late.",
         (0.02, 0.97))
    save(fig, OUT, "fig15_watermark.png")
    return int(late.sum()), n, emitted


def fig16_token_bucket():
    C, rate = 10, 5.0
    reqs = [0.0] * 12 + [0.6] * 4 + list(np.arange(1.5, 4.5, 0.125)) + [7.0] * 10
    tokens, last = float(C), 0.0
    T, L, ok_t, bad_t = [0.0], [float(C)], [], []
    for t in reqs:
        refilled = min(C, tokens + (t - last) * rate)
        if t > last:                                   # linear refill between requests
            T.append(t); L.append(refilled)
        tokens, last = refilled, t
        if tokens >= 1:
            tokens -= 1; ok_t.append(t)
        else:
            bad_t.append(t)
        T.append(t); L.append(tokens)
    for t in np.linspace(last, 8.5, 40):
        T.append(t); L.append(min(C, tokens + (t - last) * rate))
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(11, 4.3), gridspec_kw={"width_ratios": [2.2, 1]})
    ax.plot(T, L, color=BLUE, lw=1.8, label="tokens in the bucket")
    ax.scatter(ok_t, [-0.6] * len(ok_t), marker="|", s=120, color=GREEN, label=f"allowed ({len(ok_t)})")
    ax.scatter(bad_t, [-1.4] * len(bad_t), marker="|", s=120, color=RED, label=f"rejected with 429 ({len(bad_t)})")
    ax.axhline(C, color=GRAY, ls=":", lw=1); ax.text(8.45, C + 0.3, "capacity C = 10", ha="right", fontsize=8, color=GRAY)
    ax.text(0.05, 11.3, "burst of 12", fontsize=8)
    ax.text(1.55, 5.3, "steady 8 req/s for 3 s\n(faster than the 5/s refill)", fontsize=8)
    ax.text(5.6, 11.3, "burst of 10 after a rest", fontsize=8)
    ax.set_ylim(-2, 12.5); ax.set_xlim(-0.1, 8.5)
    ax.set_xlabel("Time (s)"); ax.set_ylabel("Tokens"); ax.grid(alpha=0.3)
    ax.legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.42, 0.95)); ax.set_title("Token bucket (C = 10, refill 5 tokens/s)")
    # Right: the fixed-window edge burst. Client sends 10 at t = 0.95 s and 10 at t = 1.00 s.
    # Limit: 10 per 1-second window (token bucket: C = 10, refill 10/s).
    fixed = 10 + 10                                    # new window at t = 1.00 starts from zero
    prev_weight = 1 - 0.0 / 1.0                        # sliding counter: 0 s into the new window
    sliding = 10 + max(0, int(10 - prev_weight * 10))
    bucket = 10 + int(min(10, 0 + 0.05 * 10))          # only 0.5 token refilled in 0.05 s
    b = ax2.bar(["Fixed\nwindow", "Sliding\nwindow\ncounter", "Token\nbucket"], [fixed, sliding, bucket],
                color=[RED, GREEN, BLUE])
    for bar, v in zip(b, [fixed, sliding, bucket]):
        ax2.text(bar.get_x() + bar.get_width() / 2, v + 0.4, str(v), ha="center", fontsize=9)
    ax2.axhline(10, color=GRAY, ls=":"); ax2.set_ylim(0, 23); ax2.set_ylabel("Requests allowed")
    ax2.set_title("10 requests at 0.95 s + 10 at 1.00 s\n(limit: 10 per second)", fontsize=10)
    ax2.tick_params(axis="x", labelsize=8)
    save(fig, OUT, "fig16_token_bucket.png")
    return len(ok_t), len(bad_t)


if __name__ == "__main__":
    for f in [fig01_latency_ladder, fig02_handshakes, fig03_bloom, fig04_quorum, fig05_rehash, fig06_vnodes,
              fig07_gossip, fig08_mm1, fig09_scaling, fig10_fanout, fig11_jitter, fig12_kv, fig13_zipf_cache,
              fig14_hash_ring, fig15_watermark, fig16_token_bucket]:
        out = f()
        if out is not None:
            print("   ->", out)
