"""Figures for 'Scaling to 1 Million Requests per Second'.
Computed: 02 bandwidth wall, 03 Little's law, 04 CPU budget, 06 measured O(n) vs index (SQLite),
08 birthday paradox, 09 RAM burn-down, 10 rare events. Reported-number charts are labelled as such.
Run:  python figures/million_rps/make_figs.py
"""
import sys, os, sqlite3, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _style import *

OUT = out_dir(__file__)
rng = np.random.default_rng(4)


def node(ax, x, y, text, fc="white", ec=DARK, w=1.8, h=0.8, fs=9, weight="normal"):
    box(ax, x - w / 2, y - h / 2, w, h, text, fc=fc, ec=ec, fs=fs, weight=weight)


# ------------------------------------------------------------------ 01 the journey
def fig_journey():
    steps = [("Express, 1 process\n(Mac Studio)", 20_000, GRAY), ("CP / Fastify, 1 process", 73_000, GRAY),
             ("12-core cluster, 1 KB route", 50_000, GRAY), ("128-core cloud, 'hi' route", 6_000_000, BLUE),
             ("128-core, 32 KB payload\n(NETWORK-bound)", 100_000, RED), ("same, payload cut to ~1 KB", 3_000_000, GREEN),
             ("Postgres writes (tuned)", 66_000, RED), ("Postgres reads (index)", 400_000, AMBER),
             ("single Redis (1 thread)", 100_000, AMBER), ("Redis Cluster, 15 masters", 1_000_000, GREEN),
             ("Node on 192 cores,\n30 KB payload", 700_000, RED), ("C++ / Drogon, 30 KB", 1_100_000, GREEN)]
    fig, ax = plt.subplots(figsize=(11, 5.4))
    y = np.arange(len(steps))
    ax.barh(y, [s[1] for s in steps], color=[s[2] for s in steps])
    for i, (lab, v, c) in enumerate(steps):
        ax.text(v * 1.15, i, f"{v:,} req/s", va="center", fontsize=8.5)
    ax.set_yticks(y); ax.set_yticklabels([s[0] for s in steps], fontsize=8.5)
    ax.invert_yaxis(); ax.set_xscale("log"); ax.set_xlim(1e4, 3e7)
    ax.axvline(1_000_000, color=DARK, ls="--"); ax.text(1.05e6, -0.75, "the 1M goal", fontsize=9, color=DARK)
    ax.set_xlabel("requests per second (log scale)")
    ax.set_title("The whole journey, as reported in the video\n(different routes and payloads: these are NOT apples-to-apples)")
    save(fig, OUT, "01_journey.png")


# ------------------------------------------------------------------ 02 the bandwidth wall
def fig_bandwidth():
    payload_kb = np.logspace(-2, 2, 200)
    fig, ax = plt.subplots(figsize=(9, 4.4))
    for gbps, col, name in [(10, GRAY, "10 Gbit/s (good server NIC)"), (50, AMBER, "50 Gbit/s (c8i.32xlarge)"),
                            (100, BLUE, "100 Gbit/s"), (600, GREEN, "600 Gbit/s (c8gn.48xlarge)")]:
        rps = gbps * 1e9 / 8 / (payload_kb * 1024)
        ax.loglog(payload_kb, rps, color=col, lw=2.3, label=name)
    ax.axhline(1e6, color=DARK, ls="--"); ax.text(0.011, 1.25e6, "1 million req/s", fontsize=9)
    for kb, lab in [(0.02, "'hi'\n20 B"), (1, "small JSON\n1 KB"), (30, "rich JSON\n30 KB")]:
        ax.axvline(kb, color=RED, ls=":", lw=1)
        ax.text(kb, 2e9, lab, fontsize=8, ha="center", color=RED)
    ax.set_xlabel("response payload size (KB)"); ax.set_ylabel("max requests/s the network allows")
    ax.set_ylim(1e3, 1e10)
    ax.set_title("The bandwidth wall (pure arithmetic): 1M req/s × 30 KB = 246 Gbit/s\n"
                 "No code optimization can beat this; only smaller payloads, compression, or more machines")
    ax.legend(fontsize=8.5); ax.grid(alpha=0.3, which="both")
    save(fig, OUT, "02_bandwidth_wall.png")


# ------------------------------------------------------------------ 03 Little's law
def fig_littles_law():
    lat = np.logspace(-1, 3, 200)   # ms
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    for rps, col in [(10_000, GRAY), (100_000, AMBER), (1_000_000, RED)]:
        ax.loglog(lat, rps * lat / 1000, color=col, lw=2.3, label=f"{rps:,} req/s")
    ax.scatter([5], [1e6 * 5 / 1000], color=DARK, zorder=5)
    ax.annotate("1M req/s at 5 ms per request\n= 5,000 requests in flight", (5, 5000), (0.15, 30000), fontsize=9,
                arrowprops=dict(arrowstyle="->", color=DARK))
    ax.axhline(120_000, color=GREEN, ls="--")
    ax.text(0.12, 145_000, "the video's final test: 60 machines × 400 conns × 5 pipelining = 120,000 in flight",
            fontsize=8.5, color=GREEN)
    ax.set_xlabel("average latency per request (ms)"); ax.set_ylabel("concurrent requests in flight")
    ax.set_title("Little's Law:  concurrency = throughput × latency\nSlow requests need proportionally more open connections")
    ax.legend(fontsize=9); ax.grid(alpha=0.3, which="both")
    save(fig, OUT, "03_littles_law.png")


# ------------------------------------------------------------------ 04 CPU budget per request
def fig_cpu_budget():
    fig, ax = plt.subplots(figsize=(9, 4.2))
    cores = np.array([8, 16, 32, 64, 128, 192, 384])
    for rps, col in [(100_000, GREEN), (1_000_000, RED)]:
        ax.plot(cores, cores * 1e6 / rps, "o-", color=col, lw=2.2, label=f"{rps:,} req/s")
    costs = [("dict/map lookup", 0.05), ("JSON parse 1 KB", 3), ("bcrypt hash", 100_000),
             ("JSON build 30 KB", 100), ("Redis round trip (network)", 200), ("Postgres query", 1000)]
    for name, us in costs:
        if us < 1e4:
            ax.axhline(us, color=GRAY, ls=":", lw=1)
            ax.text(400, us, f" {name} ≈ {us} µs", fontsize=8, va="center", color=GRAY)
    ax.set_yscale("log"); ax.set_xscale("log", base=2)
    ax.set_xlabel("CPU cores on the server"); ax.set_ylabel("CPU time available per request (µs, log)")
    ax.set_xlim(7, 1400)
    ax.set_title("Your CPU budget per request\n128 cores at 1M req/s = 128 µs of CPU per request — and JSON alone can eat most of it")
    ax.legend(fontsize=9); ax.grid(alpha=0.3, which="both")
    save(fig, OUT, "04_cpu_budget.png")


# ------------------------------------------------------------------ 05 threads and cores
def fig_threads():
    fig, axes = plt.subplots(1, 2, figsize=(12, 3.6))
    for ax, busy, title in [(axes[0], [True] + [False] * 11, "1 process, 1 thread:\n'100% CPU' means ONE core is busy"),
                            (axes[1], [True] * 12, "12 processes (PM2 cluster):\nevery core has work")]:
        ax.set_xlim(0, 12); ax.set_ylim(0, 3); ax.axis("off"); ax.set_title(title, weight="bold")
        for i, b in enumerate(busy):
            ax.add_patch(FancyBboxPatch((i + 0.1, 1.2), 0.8, 1.0, boxstyle="round,pad=0.02",
                                        fc="#fee2e2" if b else "#f3f4f6", ec=RED if b else GRAY, lw=1.4))
            ax.text(i + 0.5, 1.7, "busy" if b else "idle", ha="center", va="center", fontsize=7.5,
                    color=RED if b else GRAY)
            ax.text(i + 0.5, 1.0, f"core {i+1}", ha="center", va="top", fontsize=6.5, color=GRAY)
        used = sum(busy)
        ax.text(6, 0.4, f"Method 1 (sum of cores): {used*100}%     Method 2 (normalized): {used/12*100:.0f}%",
                ha="center", fontsize=9)
    save(fig, OUT, "05_threads_and_cores.png")


# ------------------------------------------------------------------ 06 measured O(n) vs index
def fig_query_complexity():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE codes(id INTEGER PRIMARY KEY, code TEXT)")
    sizes = [10_000, 30_000, 100_000, 300_000, 1_000_000, 3_000_000]
    t_rand, t_cnt, t_idx, inserted = [], [], [], 0
    for rows in sizes:
        db.executemany("INSERT INTO codes(code) VALUES (?)", ((f"code{i}",) for i in range(inserted, rows)))
        db.commit(); inserted = rows
        t0 = time.perf_counter()
        for _ in range(3):
            db.execute("SELECT id, code FROM codes ORDER BY RANDOM() LIMIT 1").fetchone()
        t_rand.append((time.perf_counter() - t0) / 3 * 1000)
        t0 = time.perf_counter()
        for _ in range(3):
            db.execute("SELECT COUNT(*) FROM codes").fetchone()
        t_cnt.append((time.perf_counter() - t0) / 3 * 1000)
        t0 = time.perf_counter()
        for _ in range(20):
            mx = db.execute("SELECT MAX(id) FROM codes").fetchone()[0]
            db.execute("SELECT id, code FROM codes WHERE id = ?", (mx // 2,)).fetchone()
        t_idx.append((time.perf_counter() - t0) / 20 * 1000)
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4))
    ax = axes[0]
    ax.loglog(sizes, t_rand, "o-", color=RED, lw=2.2, label="v1: ORDER BY RANDOM()  — scans + sorts everything")
    ax.loglog(sizes, t_cnt, "o-", color=AMBER, lw=2.2, label="v2: SELECT COUNT(*)  — still a full scan")
    ax.loglog(sizes, t_idx, "o-", color=GREEN, lw=2.2, label="v3: MAX(id) + lookup by id — index, ~flat")
    ax.set_xlabel("rows in the table"); ax.set_ylabel("time for ONE query (ms, measured)")
    ax.set_title("Measured on SQLite: the same 'get a random row',\nwritten three ways")
    ax.legend(fontsize=8); ax.grid(alpha=0.3, which="both")
    ax = axes[1]
    per_core_rps = [1000 / t for t in t_idx], [1000 / t for t in t_rand]
    ax.loglog(sizes, [1000 / t for t in t_rand], "o-", color=RED, lw=2.2, label="ORDER BY RANDOM()")
    ax.loglog(sizes, [1000 / t for t in t_idx], "o-", color=GREEN, lw=2.2, label="index lookup")
    ax.axhline(1e6, color=DARK, ls="--"); ax.text(1.2e4, 1.3e6, "1M req/s target", fontsize=9)
    ax.set_xlabel("rows in the table"); ax.set_ylabel("requests/s one query thread could serve")
    ax.set_title("The same data as a throughput ceiling\n(one thread; real servers run many in parallel)")
    ax.legend(fontsize=8.5); ax.grid(alpha=0.3, which="both")
    save(fig, OUT, "06_query_complexity_measured.png")
    print("ORDER BY RANDOM ms:", [round(t, 2) for t in t_rand], "index ms:", [round(t, 4) for t in t_idx])


# ------------------------------------------------------------------ 07 storage hierarchy + buffer-and-flush
def fig_storage_and_buffer():
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 4.4), gridspec_kw=dict(width_ratios=[1, 1.3]))
    ax = axes[0]
    layers = [("CPU register", 0.3e-9, DARK), ("L1 cache", 1e-9, BLUE), ("RAM (Redis)", 100e-9, GREEN),
              ("NVMe SSD (Postgres)", 100e-6, AMBER), ("network round trip\n(same datacentre)", 500e-6, PURPLE),
              ("spinning disk seek", 10e-3, RED)]
    y = np.arange(len(layers))
    ax.barh(y, [l[1] for l in layers], color=[l[2] for l in layers])
    for i, (lab, v, c) in enumerate(layers):
        ax.text(v * 1.4, i, (f"{v*1e9:.1f} ns" if v < 1e-8 else f"{v*1e9:,.0f} ns") if v < 1e-6 else (f"{v*1e6:,.0f} µs" if v < 1e-3 else f"{v*1e3:,.0f} ms"),
                va="center", fontsize=8.5)
    ax.set_yticks(y); ax.set_yticklabels([l[0] for l in layers], fontsize=9); ax.invert_yaxis()
    ax.set_xscale("log"); ax.set_xlabel("typical latency (seconds, log)"); ax.set_xlim(1e-10, 1)
    ax.set_title("Why Redis beats Postgres on the hot path:\nRAM is ~1,000× lower latency than SSD")
    ax = axes[1]
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax.set_title("Buffer in memory, flush in batches", weight="bold")
    node(ax, 1.4, 8, "1M req/s", fc="#f9fafb", ec=GRAY, w=2.2, h=0.9)
    node(ax, 5, 8, "app server\n(writes to Redis)", fc="#eff6ff", ec=BLUE, w=3.0, h=1.0)
    node(ax, 5, 5.6, "Redis cluster (RAM)\nkey → value  +  sync-queue", fc="#fee2e2", ec=RED, w=5.2, h=1.2)
    node(ax, 5, 3.0, "sync worker: drain the queue,\nbatch INSERT every few seconds", fc="#fef3c7", ec=AMBER, w=5.6, h=1.2)
    node(ax, 5, 0.9, "Postgres (disk, durable, queryable)", fc="#f0fdf4", ec=GREEN, w=5.6, h=0.9)
    arrow(ax, 2.5, 8, 3.5, 8); arrow(ax, 5, 7.5, 5, 6.2, text="~100 µs", fs=8)
    arrow(ax, 5, 5.0, 5, 3.6, color=AMBER); arrow(ax, 5, 2.4, 5, 1.35, color=GREEN, text="thousands of rows per statement", fs=8)
    ax.text(5, 0.1, "The request path never waits for the disk. Durability is traded for a few seconds of lag.",
            ha="center", fontsize=8.5, color=GRAY)
    save(fig, OUT, "07_storage_and_buffering.png")


# ------------------------------------------------------------------ 08 birthday paradox
def fig_birthday():
    N = 2.0 ** 122
    n = np.logspace(9, 20, 300)
    p = 1 - np.exp(-n * n / (2 * N))
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.loglog(n, np.clip(p, 1e-30, 1), color=PURPLE, lw=2.5)
    n50 = np.sqrt(2 * N * np.log(2))
    ax.axhline(0.5, color=GRAY, ls=":"); ax.axvline(n50, color=RED, ls="--")
    ax.text(n50 * 1.15, 1e-10, f"50% chance after\n{n50:.1e} UUIDs\n= {n50/1e6/3.156e7:,.0f} years at 1M/s",
            fontsize=9, color=RED)
    for years, lab in [(1, "1 year"), (100, "100 years")]:
        x = 1e6 * years * 3.156e7
        ax.axvline(x, color=GREEN, ls=":", lw=1)
        ax.text(x, 1e-26, f"{lab} at\n1M UUIDs/s", fontsize=8, color=GREEN, ha="center")
    ax.set_xlabel("UUIDv4 values generated"); ax.set_ylabel("probability of at least one collision")
    ax.set_ylim(1e-30, 2)
    ax.set_title("Birthday paradox: P ≈ 1 − exp(−n² / 2N),  N = 2¹²²\n"
                 "Random IDs remove the coordination bottleneck of a shared counter, at negligible risk")
    ax.grid(alpha=0.3, which="both")
    save(fig, OUT, "08_uuid_birthday.png")


# ------------------------------------------------------------------ 09 RAM burn-down
def fig_ram():
    hours = np.linspace(0, 12, 300)
    fig, ax = plt.subplots(figsize=(9, 4))
    for bytes_per_rec, col, lab in [(100, GREEN, "100 B per record"), (500, AMBER, "500 B per record"),
                                    (1700, RED, "~1.7 KB per record (the video: 100 GB / 60M rows)")]:
        gb = 1_000_000 * bytes_per_rec * hours * 3600 / 1e9
        ax.plot(hours, gb, color=col, lw=2.3, label=lab)
    ax.axhline(384, color=DARK, ls="--"); ax.text(0.1, 420, "384 GB of RAM (c8gn.48xlarge)", fontsize=9)
    ax.set_yscale("log"); ax.set_ylim(10, 1e6)
    ax.set_xlabel("hours of sustained 1M writes/s"); ax.set_ylabel("RAM consumed (GB, log)")
    ax.set_title("Memory is a bucket with a hole you must open:\nat 1M writes/s you fill 384 GB in minutes unless you flush to disk")
    ax.legend(fontsize=8.5); ax.grid(alpha=0.3, which="both")
    for b, col, dy in [(100, GREEN, 120), (500, AMBER, 60), (1700, RED, 30)]:
        t = 384e9 / (1_000_000 * b) / 3600
        ax.scatter([t], [384], color=col, zorder=5)
        ax.annotate(f"384 GB full in {t*60:.0f} min", (t, 384), (t + 0.9, dy), fontsize=8.5, color=col,
                    arrowprops=dict(arrowstyle="->", color=col, lw=1))
    save(fig, OUT, "09_ram_burndown.png")


# ------------------------------------------------------------------ 10 rare events
def fig_rare_events():
    rps = np.logspace(1, 6, 200)
    fig, ax = plt.subplots(figsize=(9, 4))
    for odds, col, lab in [(1e6, RED, "1-in-a-million event"), (1e9, AMBER, "1-in-a-billion event"),
                           (1e12, GREEN, "1-in-a-trillion event")]:
        ax.loglog(rps, rps * 86400 / odds, color=col, lw=2.3, label=lab)
    ax.axhline(1, color=DARK, ls="--"); ax.text(12, 1.3, "once per day", fontsize=9)
    ax.axvline(1e6, color=GRAY, ls=":"); ax.text(1.1e6, 1e-6, "1M req/s", fontsize=9, color=GRAY)
    ax.scatter([1e6], [86400], color=RED, zorder=5)
    ax.annotate("at 1M req/s a 'one in a million'\nevent happens EVERY SECOND", (1e6, 86400), (2e3, 5e4),
                fontsize=9, color=RED, arrowprops=dict(arrowstyle="->", color=RED))
    ax.set_xlabel("requests per second"); ax.set_ylabel("occurrences per day")
    ax.set_ylim(1e-8, 1e7)
    ax.set_title("Why rare bugs stop being rare\n(and why 2 billion requests with 40 timeouts = 0.000002% is genuinely good)")
    ax.legend(fontsize=8.5); ax.grid(alpha=0.3, which="both")
    save(fig, OUT, "10_rare_events.png")


# ------------------------------------------------------------------ 11 one big box vs many
def fig_distributed():
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.4))
    for ax in axes:
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax = axes[0]; ax.set_title("What the video built: one enormous machine", weight="bold")
    node(ax, 5, 8.5, "every user on Earth", fc="#f9fafb", ec=GRAY, w=5, h=0.9)
    node(ax, 5, 5.5, "1 × c8gn.48xlarge\n192 cores · 384 GB · 600 Gbit/s\n≈ $8,000 / month", fc="#fee2e2", ec=RED, w=6, h=1.8)
    arrow(ax, 5, 8.0, 5, 6.5, color=RED)
    ax.text(5, 3.2, "✗ one region: users far away pay 200 ms\n✗ one failure domain\n"
                    "✗ the network card is a hard ceiling\n✓ great for learning where limits are", ha="center", fontsize=9)
    ax = axes[1]; ax.set_title("What Uber/Amazon actually do: many, spread out", weight="bold")
    node(ax, 5, 9.0, "users, routed by geography (DNS / anycast)", fc="#f9fafb", ec=GRAY, w=8, h=0.8)
    regions = [("US-East", 1.5), ("US-West", 3.6), ("Europe", 5.7), ("Asia", 7.8)]
    for name, x in regions:
        node(ax, x, 6.3, name, fc="#eff6ff", ec=BLUE, w=1.8, h=0.7, fs=8.5)
        arrow(ax, 5, 8.55, x, 6.7, color=BLUE, lw=1)
        for j in range(3):
            ax.add_patch(FancyBboxPatch((x - 0.7 + j * 0.5, 4.3), 0.42, 0.9, boxstyle="round,pad=0.02",
                                        fc="#dcfce7", ec=GREEN, lw=1))
        ax.text(x, 3.9, "servers", ha="center", fontsize=7.5, color=GREEN)
    ax.text(5, 2.6, "✓ low latency everywhere   ✓ a region can fail   ✓ add capacity where demand is\n"
                    "100 servers × 10,000 req/s each = 1,000,000 req/s, on ordinary hardware", ha="center", fontsize=9)
    save(fig, OUT, "11_one_box_vs_distributed.png")


if __name__ == "__main__":
    fig_journey(); fig_bandwidth(); fig_littles_law(); fig_cpu_budget(); fig_threads(); fig_query_complexity()
    fig_storage_and_buffer(); fig_birthday(); fig_ram(); fig_rare_events(); fig_distributed()
