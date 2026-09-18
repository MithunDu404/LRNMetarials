"""Figures for 'System Design - APIs Databases Caching CDNs and Scaling'.
Computed figures: 04 availability math, 05 load-balancer simulation, 06 consistent hashing, 08 polling vs WebSocket,
10 cache hit-ratio (LRU simulation), 11 CDN latency physics, 15 rate-limiter window burst simulation.
Run:  python figures/system_design/make_figs.py
"""
import sys, os, hashlib, heapq, random
from bisect import bisect
from collections import OrderedDict
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _style import *

OUT = out_dir(__file__)
rng = np.random.default_rng(8)
random.seed(8)


def node(ax, x, y, text, fc="white", ec=DARK, w=1.8, h=0.8, fs=9, weight="normal"):
    box(ax, x - w / 2, y - h / 2, w, h, text, fc=fc, ec=ec, fs=fs, weight=weight)


# ------------------------------------------------------------------ 01 architecture evolution
def fig_evolution():
    fig, axes = plt.subplots(1, 4, figsize=(16, 5.4))
    titles = ["① single server", "② split web & data tiers", "③ load balancer + many servers", "④ + cache, CDN, DB replicas"]
    for ax, t in zip(axes, titles):
        ax.set_xlim(0, 10); ax.set_ylim(0, 12); ax.axis("off"); ax.set_title(t, weight="bold")
    # 1
    ax = axes[0]
    node(ax, 5, 11, "users", fc="#f9fafb", ec=GRAY, w=3); node(ax, 1.6, 8.6, "DNS", fc="#fffbeb", ec=AMBER, w=2.2)
    node(ax, 5, 5.5, "ONE server\nweb app + DB\n+ cache + files", fc="#eff6ff", ec=BLUE, w=6, h=3)
    arrow(ax, 4.2, 10.5, 2.0, 9.0, color=AMBER, text="IP?", fs=8); arrow(ax, 5, 10.5, 5, 7.1)
    ax.text(5, 2.5, "simple, cheap\nbut one crash = total outage", ha="center", fontsize=8.5, color=RED)
    # 2
    ax = axes[1]
    node(ax, 5, 11, "users", fc="#f9fafb", ec=GRAY, w=3)
    node(ax, 5, 7.5, "web tier\n(app server)", fc="#eff6ff", ec=BLUE, w=5, h=1.6)
    node(ax, 5, 3.8, "data tier\n(database server)", fc="#f0fdf4", ec=GREEN, w=5, h=1.6)
    arrow(ax, 5, 10.5, 5, 8.35); arrow(ax, 5, 6.65, 5, 4.65, style="<|-|>")
    ax.text(5, 1.5, "scale each tier on its own", ha="center", fontsize=8.5, color=GRAY)
    # 3
    ax = axes[2]
    node(ax, 5, 11, "users", fc="#f9fafb", ec=GRAY, w=3); node(ax, 5, 9, "load balancer(s)", fc="#fef3c7", ec=AMBER, w=5)
    for i, x in enumerate([2, 5, 8]):
        node(ax, x, 6.5, f"app {i+1}", fc="#eff6ff", ec=BLUE, w=2.2); arrow(ax, 5, 8.6, x, 6.9)
        arrow(ax, x, 6.1, 5, 4.2)
    node(ax, 5, 3.6, "database", fc="#f0fdf4", ec=GREEN, w=4)
    ax.text(5, 1.8, "stateless app servers:\nadd more when busy\n(DB is now the SPOF)", ha="center", fontsize=8.5, color=GRAY)
    arrow(ax, 5, 10.6, 5, 9.4)
    # 4
    ax = axes[3]
    node(ax, 5, 11.2, "users", fc="#f9fafb", ec=GRAY, w=3); node(ax, 1.7, 9.6, "CDN edge\n(static files)", fc="#fdf2f8", ec=PINK, w=3, h=1.1, fs=8)
    node(ax, 6.3, 9.4, "load balancers", fc="#fef3c7", ec=AMBER, w=4.2, h=0.7)
    arrow(ax, 4.3, 10.8, 2.3, 10.2, color=PINK); arrow(ax, 5.6, 10.8, 6.1, 9.8)
    for x in [3.7, 6.3, 8.9]:
        node(ax, x, 7.6, "app", fc="#eff6ff", ec=BLUE, w=1.9, h=0.7); arrow(ax, 6.3, 9.05, x, 7.95, lw=1)
    node(ax, 2.0, 5.6, "cache\n(Redis)", fc="#fee2e2", ec=RED, w=2.6, h=1.1)
    node(ax, 6.3, 5.4, "primary DB\n(writes)", fc="#f0fdf4", ec=GREEN, w=3.2, h=1.1)
    arrow(ax, 3.7, 7.25, 2.4, 6.15, lw=1, color=RED); arrow(ax, 6.3, 7.25, 6.3, 5.95, lw=1)
    for x in [4.4, 8.2]:
        node(ax, x, 3.2, "read\nreplica", fc="#dcfce7", ec=GREEN, w=2.4, h=1.1, fs=8); arrow(ax, 6.3, 4.85, x, 3.75, color=GREEN, lw=1, text="replicate" if x > 5 else None, fs=7)
    ax.text(5, 1.2, "fast reads, global static delivery,\nno single DB machine for reads", ha="center", fontsize=8.5, color=GRAY)
    save(fig, OUT, "01_architecture_evolution.png")


# ------------------------------------------------------------------ 02 request flow
def fig_request_flow():
    fig, ax = canvas(12.5, 5.2, (0, 12.5), (0, 5.2))
    ax.text(6.25, 4.95, "What happens when you open app.demo.com", ha="center", fontsize=12, weight="bold")
    cols = [(1.2, "browser /\nmobile app", GRAY), (4.4, "DNS resolver", AMBER), (7.6, "server\n(203.0.113.7)", BLUE), (10.8, "database", GREEN)]
    for x, t, c in cols:
        node(ax, x, 4.2, t, fc="white", ec=c, w=2.2, h=0.8)
        ax.plot([x, x], [3.75, 0.2], color=LIGHT, lw=2, zorder=1)
    msgs = [(1.2, 4.4, 3.4, "① where is app.demo.com?", AMBER), (4.4, 1.2, 3.0, "② it's 203.0.113.7 (cached for TTL)", AMBER),
            (1.2, 7.6, 2.5, "③ TCP + TLS handshake, then GET /product/123", BLUE), (7.6, 10.8, 2.0, "④ SELECT … WHERE id=123", GREEN),
            (10.8, 7.6, 1.55, "⑤ row", GREEN), (7.6, 1.2, 1.05, "⑥ 200 OK  HTML (browser) or JSON (mobile)", BLUE)]
    for x1, x2, y, t, c in msgs:
        arrow(ax, x1, y, x2, y, color=c, lw=1.6)
        ax.text((x1 + x2) / 2, y + 0.08, t, ha="center", va="bottom", fontsize=8.5, color=c,
                bbox=dict(fc="white", ec="none", pad=0.3))
    save(fig, OUT, "02_request_flow.png")


# ------------------------------------------------------------------ 03 SQL vs document model
def fig_data_models():
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.6))
    for ax in axes:
        ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax = axes[0]; ax.set_title("Relational: separate tables, linked by IDs, JOIN to combine", weight="bold")
    tables = [(0.2, 6.2, "customers", ["id | name | email", "123 | John | j@x.com", "124 | Mia  | m@x.com"]),
              (5.3, 6.2, "products", ["id | name   | price", "p1 | Lamp   | 19.99", "p2 | Chair  | 89.00"]),
              (2.6, 1.0, "orders", ["id | customer_id | product_id", "o1 | 123         | p1", "o2 | 123         | p2"])]
    for x, y, name, rows in tables:
        box(ax, x, y, 4.4, 2.9, "", fc="#f0fdf4", ec=GREEN)
        ax.text(x + 0.15, y + 2.55, name, fontsize=10, weight="bold", color=GREEN)
        for i, r in enumerate(rows):
            ax.text(x + 0.15, y + 1.85 - i * 0.62, r, fontsize=8.5, family="monospace", weight="bold" if i == 0 else "normal")
    arrow(ax, 3.5, 3.9, 2.0, 6.2, color=GRAY, lw=1); arrow(ax, 6.0, 3.9, 7.0, 6.2, color=GRAY, lw=1)
    ax = axes[1]; ax.set_title("Document (MongoDB): related data nested in one record", weight="bold")
    doc = ('{\n  "_id": 123,\n  "name": "John",\n  "email": "j@x.com",\n  "orders": [\n'
           '    {"id": "o1", "product": {"name": "Lamp",  "price": 19.99}},\n'
           '    {"id": "o2", "product": {"name": "Chair", "price": 89.00}}\n  ]\n}')
    ax.text(0.3, 9.2, doc, family="monospace", fontsize=9.5, va="top", bbox=dict(fc="#eff6ff", ec=BLUE, boxstyle="round,pad=0.6"))
    ax.text(0.3, 1.0, "one read gets the whole page ✓   but product data is duplicated in every order ✗\n"
                      "(changing a product name means updating many documents)", fontsize=8.5, color=GRAY)
    save(fig, OUT, "03_sql_vs_document.png")


# ------------------------------------------------------------------ 04 availability math
def fig_availability():
    a = np.linspace(0.9, 0.9999, 300)
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4))
    ax = axes[0]
    for n, c in [(1, RED), (2, AMBER), (3, GREEN)]:
        ax.plot(a * 100, (1 - (1 - a) ** n) * 100, color=c, lw=2.3, label="1 copy (no redundancy)" if n == 1 else f"{n} redundant copies in parallel")
    ax.set_xlabel("availability of ONE server (%)"); ax.set_ylabel("system availability (%)")
    ax.set_title("Redundancy: the system is down only if ALL copies are down\nA = 1 − (1 − a)ⁿ   (assumes independent failures)")
    ax.legend(fontsize=8.5); ax.grid(alpha=0.3); ax.set_ylim(90, 100.2)
    ax = axes[1]
    comps = ["DNS\n99.99%", "load bal.\n99.95%", "app tier\n99.9%", "database\n99.9%", "cache\n99.9%"]
    avail = [0.9999, 0.9995, 0.999, 0.999, 0.999]
    chain = np.cumprod(avail)
    minutes = (1 - chain) * 525600
    ax.bar(range(len(comps)), minutes, color=[BLUE, AMBER, BLUE, GREEN, RED])
    for i, (m, c) in enumerate(zip(minutes, chain)):
        ax.text(i, m + 20, f"{c*100:.2f}%\n≈{m/60:.1f} h/yr", ha="center", fontsize=8.5)
    ax.set_xticks(range(len(comps))); ax.set_xticklabels(comps, fontsize=8.5)
    ax.set_ylabel("expected downtime per year (minutes)"); ax.set_xlabel("system after adding each component in the request path")
    ax.set_title("Components in SERIES multiply: every single point\nof failure adds downtime  (A = a₁·a₂·a₃…)")
    ax.set_ylim(0, minutes.max() * 1.3)
    save(fig, OUT, "04_availability_math.png")


# ------------------------------------------------------------------ 05 load balancing simulation
def fig_lb_sim():
    from collections import deque
    speed = np.array([1.0, 1.0, 1.0, 0.5])                     # server 4 is half as fast (older machine)
    n_req, rate = 80000, 4.5                                    # ~85% of total capacity is used
    arrivals = np.cumsum(rng.exponential(1 / rate, n_req))
    work = rng.lognormal(np.log(0.8), 1.0, n_req) * 0.5         # heavy-tailed job sizes (mean ≈ 0.66 s of work)
    choices = rng.integers(0, 4, size=(n_req, 2))

    def simulate(policy):
        k = len(speed)
        deps = [deque() for _ in range(k)]                      # departure times of jobs in each FIFO single-worker queue
        last = np.zeros(k); rr = 0; lat = np.empty(n_req)
        for i, (t, w) in enumerate(zip(arrivals, work)):
            for q in deps:
                while q and q[0] <= t:
                    q.popleft()
            active = np.array([len(q) for q in deps])
            if policy == "round robin":
                srv = rr % k; rr += 1
            elif policy == "random":
                srv = choices[i, 0]
            elif policy == "power of two choices":
                a, b = choices[i]; srv = a if active[a] <= active[b] else b
            elif policy == "least connections":
                srv = int(np.argmin(active))
            else:                                               # weighted least connections
                srv = int(np.argmin((active + 1) / speed))
            start_t = max(t, last[srv]); finish = start_t + w / speed[srv]
            last[srv] = finish; deps[srv].append(finish); lat[i] = finish - t
        return lat[n_req // 10:]                                # drop warm-up

    policies = ["random", "round robin", "power of two choices", "least connections", "weighted least conn."]
    res = {p: simulate(p) for p in policies}
    fig, ax = plt.subplots(figsize=(9.5, 4.2))
    x = np.arange(len(policies))
    p50 = [np.percentile(res[p], 50) for p in policies]; p99 = [np.percentile(res[p], 99) for p in policies]
    ax.bar(x - 0.2, p50, 0.4, color=BLUE, label="median latency")
    ax.bar(x + 0.2, p99, 0.4, color=RED, label="p99 latency (slowest 1%)")
    for i in range(len(policies)):
        ax.text(i + 0.2, p99[i] * 1.15, f"{p99[i]:.1f}s", ha="center", fontsize=8.5)
        ax.text(i - 0.2, p50[i] * 1.15, f"{p50[i]:.1f}s", ha="center", fontsize=8.5)
    ax.set_yscale("log")
    ax.set_xticks(x); ax.set_xticklabels(policies, fontsize=9)
    ax.set_ylabel("seconds (log scale)"); ax.legend(fontsize=9)
    ax.set_title("Simulated: 80,000 requests at ~85% load, heavy-tailed job sizes, 4 servers (one is half as fast)\n"
                 "blind algorithms overload the slow server; load- and capacity-aware ones protect the tail")
    save(fig, OUT, "05_load_balancer_sim.png")
    print("lb p50", dict(zip(policies, np.round(p50, 2))), "p99", dict(zip(policies, np.round(p99, 2))))


# ------------------------------------------------------------------ 06 consistent hashing
def _h(k):
    return int(hashlib.md5(k.encode()).hexdigest()[:12], 16)

def fig_consistent_hashing():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    ax = axes[0]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.45, 1.4)
    ax.set_title("The hash ring: a key goes to the next server clockwise", weight="bold")
    ax.add_patch(Circle((0, 0), 1, fill=False, ec=GRAY, lw=2))
    servers = {"A": 20, "B": 110, "C": 200, "D": 290}
    colors = {"A": BLUE, "B": GREEN, "C": AMBER, "D": PURPLE}
    for s, ang in servers.items():
        r = np.deg2rad(90 - ang)
        ax.scatter([np.cos(r)], [np.sin(r)], s=320, color=colors[s], zorder=3)
        ax.text(1.3 * np.cos(r), 1.3 * np.sin(r), f"server {s}", ha="center", va="center", fontsize=9, weight="bold", color=colors[s])
    for k, ang in [("user:7", 60), ("user:42", 150), ("user:99", 240), ("user:5", 330)]:
        r = np.deg2rad(90 - ang)
        owner = min(servers, key=lambda s: (servers[s] - ang) % 360)
        ax.scatter([np.cos(r)], [np.sin(r)], s=60, color="white", ec=colors[owner], lw=2, zorder=4)
        ax.text(0.72 * np.cos(r), 0.72 * np.sin(r), k, ha="center", va="center", fontsize=8, color=colors[owner])
    ax.text(0, -1.38, "Add server E between C and D: only keys in that arc move to E.", ha="center", fontsize=9)
    ax = axes[1]
    keys = [f"key{i}" for i in range(40000)]
    ns = np.arange(2, 21)
    mod_moved, ring_moved = [], []
    for n in ns:
        mod_moved.append(np.mean([_h(k) % n != _h(k) % (n + 1) for k in keys[:10000]]) * 100)
        def ring(nodes):
            pts = sorted((_h(f"{s}#{v}"), s) for s in nodes for v in range(50))
            return [p for p, _ in pts], [s for _, s in pts]
        p1, o1 = ring(range(n)); p2, o2 = ring(range(n + 1))
        moved = 0
        for k in keys[:10000]:
            hk = _h(k)
            moved += o1[bisect(p1, hk) % len(p1)] != o2[bisect(p2, hk) % len(p2)]
        ring_moved.append(moved / 100)
    ax.plot(ns, mod_moved, "o-", color=RED, lw=2.2, label="hash(key) % N  (IP-hash style)")
    ax.plot(ns, ring_moved, "o-", color=GREEN, lw=2.2, label="consistent hashing (50 virtual nodes/server)")
    ax.plot(ns, 100 / (ns + 1), ":", color=GRAY, label="ideal: 1/(N+1)")
    ax.set_xlabel("servers before adding one more (N)"); ax.set_ylabel("% of keys that change server")
    ax.set_title("Measured on 10,000 keys: adding ONE server\nmodulo reshuffles almost everything (cache stampede!)")
    ax.legend(fontsize=8.5); ax.grid(alpha=0.3)
    save(fig, OUT, "06_consistent_hashing.png")


# ------------------------------------------------------------------ 07 REST vs GraphQL round trips
def fig_rest_graphql():
    rtt = 0.12
    fig, ax = plt.subplots(figsize=(10, 3.4))
    rest = [("GET /users/123", 0), ("GET /users/123/posts", 1), ("GET /users/123/followers", 2)]
    for label, i in rest:
        ax.barh(1, rtt, left=i * rtt, color=[BLUE, PURPLE, TEAL][i], edgecolor="white")
        ax.text(i * rtt + rtt / 2, 1, label, ha="center", va="center", fontsize=7.5, color="white", weight="bold")
    ax.barh(0, rtt * 1.15, left=0, color=GREEN)
    ax.text(rtt * 0.575, 0, "POST /graphql\n{user{name posts{title} followers{name}}}", ha="center", va="center", fontsize=7.5, color="white", weight="bold")
    ax.set_yticks([0, 1]); ax.set_yticklabels(["GraphQL: 1 request", "REST: 3 sequential requests"])
    ax.set_xlabel("seconds on a mobile connection (120 ms per round trip)")
    ax.set_title("Loading a profile page: REST needs one round trip per resource (unless parallelized or a composite endpoint);\n"
                 "GraphQL fetches exactly the requested fields in one", fontsize=10)
    ax.set_xlim(0, 0.4)
    save(fig, OUT, "07_rest_vs_graphql_roundtrips.png")


# ------------------------------------------------------------------ 08 polling vs websocket
def fig_polling():
    T = 3600.0
    msg_times = np.sort(rng.uniform(0, T, 40))            # 40 chat messages in an hour
    intervals = [1, 2, 5, 10, 30, 60]
    delay, wasted = [], []
    for iv in intervals:
        polls = np.arange(iv, T + iv, iv)
        idx = np.searchsorted(polls, msg_times)
        delay.append(np.mean(polls[idx] - msg_times))
        nonempty = len(np.unique(idx))
        wasted.append((len(polls) - nonempty) / len(polls) * 100)
    fig, axes = plt.subplots(1, 2, figsize=(12, 3.9))
    ax = axes[0]
    ax.plot(intervals, delay, "o-", color=RED, lw=2.2, label="polling")
    ax.axhline(0.05, color=GREEN, lw=2.2, label="WebSocket push (~network latency)")
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("poll interval (s)"); ax.set_ylabel("avg delay before user sees message (s)")
    ax.set_title("Polling: delay ≈ half the interval"); ax.legend(fontsize=8.5); ax.grid(alpha=0.3, which="both")
    ax = axes[1]
    reqs = [T / iv for iv in intervals]
    ax.bar([str(i) for i in intervals], reqs, color=AMBER)
    for i, (r, w) in enumerate(zip(reqs, wasted)):
        ax.text(i, r * 1.05, f"{w:.0f}% empty", ha="center", fontsize=8.5)
    ax.axhline(41, color=GREEN, ls="--"); ax.text(-0.4, 30, "WebSocket: 1 handshake + 40 pushes", color=GREEN, fontsize=8.5)
    ax.set_yscale("log"); ax.set_ylim(20, 8000); ax.set_xlabel("poll interval (s)"); ax.set_ylabel("requests per user per hour")
    ax.set_title("…and most polls come back empty (simulated: 40 messages/hour)")
    save(fig, OUT, "08_polling_vs_websocket.png")


# ------------------------------------------------------------------ 09 TCP vs UDP
def fig_tcp_udp():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    for ax in axes:
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax = axes[0]; ax.set_title("TCP: handshake, ordering, retransmission", weight="bold")
    for x, l in [(1.5, "client"), (8.5, "server")]:
        node(ax, x, 9.3, l, w=2.2, h=0.7); ax.plot([x, x], [8.9, 0.3], color=LIGHT, lw=2)
    seq = [(1.5, 8.5, 8.2, "SYN", DARK), (8.5, 1.5, 7.5, "SYN-ACK", DARK), (1.5, 8.5, 6.8, "ACK  (connection open)", DARK),
           (1.5, 8.5, 5.8, "packet 1", BLUE), (1.5, 6.0, 5.1, "packet 2  ✗ lost", RED), (1.5, 8.5, 4.4, "packet 3", BLUE),
           (8.5, 1.5, 3.6, "ACK 1 … still waiting for 2", GRAY), (1.5, 8.5, 2.8, "packet 2 (retransmitted)", GREEN),
           (8.5, 1.5, 2.0, "ACK 3 → app receives 1, 2, 3 in order", GREEN)]
    for x1, x2, y, t, c in seq:
        arrow(ax, x1, y, x2, y - 0.3, color=c, lw=1.4)
        ax.text((x1 + x2) / 2, y - 0.05, t, ha="center", fontsize=8.5, color=c, bbox=dict(fc="white", ec="none", pad=0.2))
    ax.text(5, 0.6, "reliable & ordered, but extra round trips; a lost packet stalls the ones behind it", ha="center", fontsize=8.5, color=GRAY)
    ax = axes[1]; ax.set_title("UDP: fire and forget", weight="bold")
    for x, l in [(1.5, "client"), (8.5, "server")]:
        node(ax, x, 9.3, l, w=2.2, h=0.7); ax.plot([x, x], [8.9, 0.3], color=LIGHT, lw=2)
    seq = [(1.5, 8.5, 8.0, "video frame 1", BLUE), (1.5, 8.5, 7.0, "video frame 2", BLUE), (1.5, 6.0, 6.0, "video frame 3  ✗ lost", RED),
           (1.5, 8.5, 5.0, "video frame 4 (frame 3 is simply skipped)", BLUE), (1.5, 8.5, 4.0, "video frame 5", BLUE)]
    for x1, x2, y, t, c in seq:
        arrow(ax, x1, y, x2, y - 0.3, color=c, lw=1.4)
        ax.text((x1 + x2) / 2, y - 0.05, t, ha="center", fontsize=8.5, color=c, bbox=dict(fc="white", ec="none", pad=0.2))
    ax.text(5, 2.2, "no handshake, no retransmit, no ordering\n→ lowest latency for calls, games, live video\n\n"
                    "Modern twist: QUIC / HTTP/3 runs on UDP and rebuilds\nreliability per stream (no head-of-line blocking)",
            ha="center", fontsize=8.5, color=GRAY)
    save(fig, OUT, "09_tcp_vs_udp.png")


# ------------------------------------------------------------------ 10 caching
def fig_cache():
    n_items, n_req = 50_000, 150_000
    ranks = np.arange(1, n_items + 1)
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4))
    ax = axes[0]
    sizes = [50, 200, 1000, 5000, 20000]
    for s_exp, col in [(0.8, AMBER), (1.0, BLUE), (1.2, GREEN)]:
        p = 1 / ranks ** s_exp; p /= p.sum()
        reqs = rng.choice(n_items, n_req, p=p)
        hits_list = []
        for cap in sizes:
            cache, hits = OrderedDict(), 0
            for k in reqs:
                if k in cache:
                    hits += 1; cache.move_to_end(k)
                else:
                    cache[k] = 1
                    if len(cache) > cap:
                        cache.popitem(last=False)
            hits_list.append(hits / n_req * 100)
        ax.plot(np.array(sizes) / n_items * 100, hits_list, "o-", color=col, lw=2.2, label=f"popularity skew s = {s_exp}")
    ax.set_xscale("log"); ax.set_xlabel("cache size (% of all items)"); ax.set_ylabel("cache hit ratio (%)")
    ax.set_title("LRU cache simulation: a tiny cache catches most\nrequests when traffic is skewed (Zipf)"); ax.legend(fontsize=8.5); ax.grid(alpha=0.3, which="both")
    ax = axes[1]
    h = np.linspace(0, 1, 200)
    for db, col in [(20, AMBER), (50, BLUE), (200, RED)]:
        ax.plot(h * 100, h * 1 + (1 - h) * (1 + db), color=col, lw=2.2, label=f"DB query {db} ms")
    ax.set_xlabel("cache hit ratio (%)"); ax.set_ylabel("average latency (ms)")
    ax.set_title("avg latency = hit·t_cache + miss·(t_cache + t_db)\n(cache lookup = 1 ms)"); ax.legend(fontsize=8.5); ax.grid(alpha=0.3)
    save(fig, OUT, "10_caching.png")


# ------------------------------------------------------------------ 11 CDN latency physics
def fig_cdn():
    origin = (38.9, -77.4)  # Virginia
    cities = {"New York": (40.7, -74.0), "London": (51.5, -0.1), "São Paulo": (-23.5, -46.6), "Mumbai": (19.1, 72.9),
              "Tokyo": (35.7, 139.7), "Sydney": (-33.9, 151.2)}
    def dist_km(a, b):
        la1, lo1, la2, lo2 = map(np.deg2rad, (*a, *b))
        return 6371 * 2 * np.arcsin(np.sqrt(np.sin((la2 - la1) / 2) ** 2 + np.cos(la1) * np.cos(la2) * np.sin((lo2 - lo1) / 2) ** 2))
    names = list(cities)
    rtt_origin = [2 * dist_km(origin, cities[c]) * 1.5 / 200000 * 1000 for c in names]     # fiber ~200,000 km/s, path ×1.5
    rtt_edge = [2 * 50 * 1.5 / 200000 * 1000 + 2 for _ in names]                            # edge ~50 km away
    page = 6  # round trips to load a page (TCP+TLS handshakes + several requests, HTTP/1.1-ish)
    fig, ax = plt.subplots(figsize=(10, 4))
    x = np.arange(len(names))
    ax.bar(x - 0.2, np.array(rtt_origin) * page, 0.4, color=RED, label="served from origin in Virginia")
    ax.bar(x + 0.2, np.array(rtt_edge) * page, 0.4, color=GREEN, label="served from a nearby CDN edge (cache hit)")
    for i, r in enumerate(rtt_origin):
        ax.text(i - 0.2, r * page + 15, f"{r*page:.0f} ms", ha="center", fontsize=8.5)
    ax.set_xticks(x); ax.set_xticklabels(names); ax.set_ylabel(f"network time for {page} round trips (ms)")
    ax.set_title("Physics, not servers: light in fiber travels ~200,000 km/s, so distance sets a latency floor\n"
                 "(great-circle distance × 1.5 for real routes; computed, not measured)")
    ax.legend(fontsize=9)
    save(fig, OUT, "11_cdn_latency.png")


# ------------------------------------------------------------------ 12 sessions vs JWT
def fig_session_jwt():
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.6))
    for ax in axes:
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax = axes[0]; ax.set_title("Session (stateful)", weight="bold")
    node(ax, 1.5, 7.5, "browser\ncookie: sid=a8f3", fc="#f9fafb", ec=GRAY, w=2.6, h=1.2)
    for i, y in enumerate([8.4, 5.0]):
        node(ax, 5.3, y, f"app server {i+1}", fc="#eff6ff", ec=BLUE, w=2.4, h=0.9)
        arrow(ax, 7.9 - 1.4, y - 0.3, 7.9, 3.0, color=RED, lw=1)
    node(ax, 8.5, 2.3, "session store\n(Redis)\na8f3 → user 123", fc="#fee2e2", ec=RED, w=2.8, h=1.5, fs=8.5)
    arrow(ax, 2.8, 7.6, 4.1, 8.3); arrow(ax, 2.8, 7.3, 4.1, 5.2)
    ax.text(5, 0.5, "every request = a lookup in shared storage\n✓ easy to revoke (delete the session)   ✗ extra hop, shared state",
            ha="center", fontsize=8.5)
    ax = axes[1]; ax.set_title("JWT (stateless)", weight="bold")
    node(ax, 1.6, 7.5, "client\nAuthorization:\nBearer eyJ…", fc="#f9fafb", ec=GRAY, w=2.6, h=1.4, fs=8.5)
    for i, y in enumerate([8.4, 5.0]):
        node(ax, 5.3, y, f"app server {i+1}\nverifies signature\nlocally", fc="#eff6ff", ec=BLUE, w=2.6, h=1.2, fs=8.5)
    arrow(ax, 2.9, 7.7, 4.0, 8.3); arrow(ax, 2.9, 7.2, 4.0, 5.2)
    tok = "header . payload . signature\n{alg:HS256} . {sub:123, role:editor,\n exp:+15min} . HMAC(secret)"
    ax.text(7.3, 2.8, tok, fontsize=8, family="monospace", ha="center", bbox=dict(fc="#f5f3ff", ec=PURPLE, boxstyle="round,pad=0.4"))
    ax.text(5, 0.5, "no lookup per request   ✗ payload is READABLE (signed, not encrypted)\n"
                    "✗ hard to revoke before 'exp' → keep access tokens short, use refresh tokens", ha="center", fontsize=8.5)
    save(fig, OUT, "12_session_vs_jwt.png")


# ------------------------------------------------------------------ 13 OAuth + OIDC
def fig_oauth():
    fig, ax = canvas(13, 6.2, (0, 13), (0, 6.2))
    ax.text(6.5, 5.95, "'Sign in with Google': OAuth 2 authorization-code flow (+ PKCE) with OpenID Connect", ha="center",
            fontsize=12, weight="bold")
    cols = [(1.2, "user's\nbrowser", GRAY), (4.6, "your app\n(backend)", BLUE), (8.4, "Google auth\nserver", AMBER), (11.8, "Google APIs\n(e.g. Drive)", GREEN)]
    for x, t, c in cols:
        node(ax, x, 5.2, t, fc="white", ec=c, w=2.2, h=0.8)
        ax.plot([x, x], [4.75, 0.15], color=LIGHT, lw=2, zorder=1)
    msgs = [(1.2, 4.6, 4.4, "① click 'Sign in with Google'", GRAY),
            (4.6, 1.2, 4.0, "② redirect to Google with client_id, scope=openid email drive.read, code_challenge", BLUE),
            (1.2, 8.4, 3.55, "③ user logs in + sees consent screen → approves", AMBER),
            (8.4, 1.2, 3.1, "④ redirect back with one-time authorization CODE", AMBER),
            (1.2, 4.6, 2.7, "⑤ code arrives at your app", GRAY),
            (4.6, 8.4, 2.25, "⑥ exchange code (+ client secret / code_verifier)", BLUE),
            (8.4, 4.6, 1.8, "⑦ access token (OAuth) + ID TOKEN (OIDC, a JWT: who the user is)", AMBER),
            (4.6, 11.8, 1.3, "⑧ call Drive API with access token", GREEN)]
    for x1, x2, y, t, c in msgs:
        arrow(ax, x1, y, x2, y, color=c, lw=1.4)
        ax.text((x1 + x2) / 2, y + 0.06, t, ha="center", va="bottom", fontsize=8, color=c, bbox=dict(fc="white", ec="none", pad=0.2))
    ax.text(6.5, 0.45, "Access token = WHAT the app may do (authorization).  ID token = WHO the user is (authentication).  "
                       "The password never touches your app.", ha="center", fontsize=9)
    save(fig, OUT, "13_oauth_oidc_flow.png")


# ------------------------------------------------------------------ 14 RBAC ABAC ACL
def fig_authz_models():
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
    for ax in axes:
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax = axes[0]; ax.set_title("RBAC: users → roles → permissions", weight="bold")
    for i, u in enumerate(["Ann", "Bo", "Cy"]):
        node(ax, 1.5, 8 - i * 2.5, u, fc="#f9fafb", ec=GRAY, w=1.8, h=0.8)
    roles = [("admin", 8), ("editor", 5.5), ("viewer", 3)]
    for r, y in roles:
        node(ax, 5, y, r, fc="#eff6ff", ec=BLUE, w=2, h=0.8)
    for (ui, ry) in [(0, 8), (1, 5.5), (2, 3)]:
        arrow(ax, 2.4, 8 - ui * 2.5, 4.0, ry, lw=1)
    perms = {8: "create read\nupdate delete\nmanage users", 5.5: "create read\nupdate", 3: "read"}
    for y, p in perms.items():
        ax.text(6.3, y, p, fontsize=8.5, va="center")
    ax.text(5, 0.8, "simple, auditable · GitHub, Stripe, CMSs", ha="center", fontsize=8.5, color=GRAY)
    ax = axes[1]; ax.set_title("ABAC: policy over attributes", weight="bold")
    policy = ("ALLOW read\n IF user.department == 'HR'\n AND resource.classification == 'internal'\n"
              " AND env.time in 09:00–18:00\n AND env.device == 'managed'")
    ax.text(0.4, 7.8, policy, fontsize=9, family="monospace", va="top", bbox=dict(fc="#f5f3ff", ec=PURPLE, boxstyle="round,pad=0.5"))
    ax.text(5, 0.8, "very flexible · harder to reason about & audit\n(AWS IAM conditions, OPA / Cedar policies)", ha="center", fontsize=8.5, color=GRAY)
    ax = axes[2]; ax.set_title("ACL: a permission list on each resource", weight="bold")
    node(ax, 5, 8.3, "budget_2026.xlsx", fc="#f0fdf4", ec=GREEN, w=4, h=0.8)
    rows = [("Alyssa", "read"), ("Bob", "read + write"), ("Carol", "comment"), ("everyone else", "no access")]
    for i, (u, p) in enumerate(rows):
        ax.text(2.4, 6.8 - i * 1.0, u, fontsize=9.5); ax.text(6.0, 6.8 - i * 1.0, p, fontsize=9.5, color=GREEN if p != "no access" else RED)
    ax.text(5, 0.8, "precise per-object sharing · Google Drive, file systems\n(needs care at millions of objects)", ha="center", fontsize=8.5, color=GRAY)
    save(fig, OUT, "14_authorization_models.png")


# ------------------------------------------------------------------ 15 rate limiter windows
def fig_rate_limit():
    limit, window = 100, 60.0
    t_attack = np.concatenate([np.linspace(55, 59.9, 100), np.linspace(60, 64.9, 100)])   # burst straddles the boundary
    def fixed(ts):
        allowed = []; counts = {}
        for t in ts:
            w = int(t // window); c = counts.get(w, 0)
            if c < limit:
                counts[w] = c + 1; allowed.append(t)
        return np.array(allowed)
    def sliding(ts):
        allowed = []
        for t in ts:
            recent = [a for a in allowed if a > t - window]
            if len(recent) < limit:
                allowed.append(t)
        return np.array(allowed)
    fa, sa = fixed(t_attack), sliding(t_attack)
    fig, ax = plt.subplots(figsize=(9.5, 3.8))
    bins = np.arange(54, 66, 0.5)
    ax.hist(fa, bins=bins, histtype="step", color=RED, lw=2.5, label=f"fixed window: {len(fa)} allowed in 10 s")
    ax.hist(sa, bins=bins, color=GREEN, alpha=0.45, label=f"sliding window: {len(sa)} allowed in 10 s")
    ax.axvline(60, color=DARK, ls="--"); ax.text(60.1, 0.97, "window boundary", fontsize=8.5, transform=ax.get_xaxis_transform(), va="top")
    ax.set_xlabel("seconds"); ax.set_ylabel("requests allowed / 0.5 s"); ax.set_ylim(0, 16)
    ax.set_title("Limit = 100 requests per minute. An attacker bursts 200 requests around the boundary (simulation):\n"
                 "a fixed window lets 2× the limit through; a sliding window (or token bucket) doesn't")
    ax.legend(fontsize=9)
    save(fig, OUT, "15_rate_limit_windows.png")


# ------------------------------------------------------------------ 16 CSRF, XSS, CORS
def fig_web_attacks():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    for ax in axes:
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax = axes[0]; ax.set_title("CSRF: evil site rides your cookie", weight="bold")
    node(ax, 2.3, 8.5, "you (logged in to bank)\ncookie: session=…", fc="#f9fafb", ec=GRAY, w=4.2, h=1.1, fs=8.5)
    node(ax, 2.3, 5.3, "evil.com page with a\nhidden auto-submit form", fc="#fee2e2", ec=RED, w=4.2, h=1.1, fs=8.5)
    node(ax, 8.2, 5.3, "bank.com\n/transfer", fc="#eff6ff", ec=BLUE, w=2.6, h=1.1)
    arrow(ax, 2.3, 7.9, 2.3, 5.9, text="visit", fs=8)
    arrow(ax, 4.4, 5.3, 6.9, 5.3, color=RED)
    ax.text(5.6, 3.9, "POST, and the browser\nattaches your cookie!", ha="center", fontsize=8, color=RED)
    ax.text(5, 2.2, "Defenses: CSRF token the evil site can't read ·\nSameSite=Lax/Strict cookies · check Origin header ·\n"
                    "never change state with GET", ha="center", fontsize=8.5, color=GREEN)
    ax = axes[1]; ax.set_title("Stored XSS: your site serves attacker code", weight="bold")
    node(ax, 2.4, 8.5, "attacker posts a comment\ncontaining <script>…</script>", fc="#fee2e2", ec=RED, w=4.4, h=1.1, fs=8.5)
    node(ax, 7.5, 8.5, "API stores it\n(no sanitizing)", fc="#eff6ff", ec=BLUE, w=2.6, h=1.0, fs=8.5)
    node(ax, 6.9, 5.2, "victim opens the page →\nscript RUNS in their browser\n(steals data, acts as them)", fc="#fee2e2", ec=RED, w=5.4, h=1.4, fs=8.5)
    arrow(ax, 4.6, 8.5, 6.2, 8.5, color=RED); arrow(ax, 7.5, 8.0, 7.5, 5.9, color=RED)
    ax.text(5, 2.2, "Defenses: escape output by context (HTML/attr/JS) ·\nsanitize rich text (allow-list) · Content-Security-Policy ·\n"
                    "HttpOnly cookies (script can't read them)", ha="center", fontsize=8.5, color=GREEN)
    ax = axes[2]; ax.set_title("CORS: who may READ responses in a browser", weight="bold")
    node(ax, 2.3, 8.2, "JS on other-site.com\ncalls api.you.com/me", fc="#fef3c7", ec=AMBER, w=4.2, h=1.1, fs=8.5)
    node(ax, 8.0, 8.2, "api.you.com", fc="#eff6ff", ec=BLUE, w=2.6, h=0.9)
    arrow(ax, 4.4, 8.2, 6.7, 8.2, color=AMBER, text="request", fs=8)
    node(ax, 5, 5.2, "response has no\nAccess-Control-Allow-Origin\nfor other-site.com → the\nBROWSER hides it from that page", fc="#f0fdf4", ec=GREEN, w=7.6, h=1.8, fs=8.5)
    ax.text(5, 2.2, "CORS relaxes the browser's same-origin policy.\nIt is NOT an API firewall: curl/servers ignore it,\n"
                    "and it doesn't stop CSRF form posts by itself.", ha="center", fontsize=8.5, color=RED)
    save(fig, OUT, "16_web_attacks_csrf_xss_cors.png")


if __name__ == "__main__":
    fig_evolution(); fig_request_flow(); fig_data_models(); fig_availability(); fig_lb_sim(); fig_consistent_hashing()
    fig_rest_graphql(); fig_polling(); fig_tcp_udp(); fig_cache(); fig_cdn(); fig_session_jwt(); fig_oauth()
    fig_authz_models(); fig_rate_limit(); fig_web_attacks()
