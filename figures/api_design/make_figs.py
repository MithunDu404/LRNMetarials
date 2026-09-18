"""Figures for 'REST API Design - The 8 Laws'.
Figures 02, 04 and 08 are simulations / real measurements (retries, backoff, SQLite pagination).
Run:  python figures/api_design/make_figs.py
"""
import sys, os, sqlite3, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _style import *

OUT = out_dir(__file__)
rng = np.random.default_rng(1)


# ------------------------------------------------------------------ 01 actions vs resources
def fig_resources():
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
    for ax in axes:
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax = axes[0]
    ax.set_title("✗ Action-named endpoints: the URL repeats the verb", color=RED)
    urls = ["POST /getUsers", "POST /createUser", "POST /updateUserEmail", "GET  /deleteUser?id=7",
            "POST /getOrdersForUser", "POST /cancelOrder", "GET  /fetchProductList", "POST /removeProduct",
            "POST /user/getProfile", "…one new URL for every new operation"]
    for i, u in enumerate(urls):
        ax.text(0.3, 9.2 - i * 0.92, u, fontsize=10, family="monospace", color=RED if i < 9 else GRAY)
    ax = axes[1]
    ax.set_title("✓ Resource-named endpoints: the METHOD is the verb", color=GREEN)
    rows = [("", "GET", "POST", "PUT", "PATCH", "DELETE"),
            ("/users", "list", "create", "", "", ""),
            ("/users/{id}", "read", "", "replace", "update", "delete"),
            ("/users/{id}/orders", "list", "create", "", "", ""),
            ("/orders/{id}", "read", "", "", "update", "delete"),
            ("/orders/{id}/cancellation", "", "cancel", "", "", "")]
    xs = [0.0, 3.9, 5.1, 6.4, 7.6, 8.9]
    for i, r in enumerate(rows):
        y = 9.0 - i * 1.25
        for j, (cell, x) in enumerate(zip(r, xs)):
            if i == 0 or j == 0:
                ax.text(x, y, cell, fontsize=10, weight="bold", family="monospace" if j == 0 else None,
                        color=DARK if i == 0 else BLUE)
            elif cell:
                ax.add_patch(FancyBboxPatch((x - 0.15, y - 0.3), 1.1, 0.75, boxstyle="round,pad=0.02",
                                            fc="#dcfce7", ec=GREEN, lw=1))
                ax.text(x + 0.4, y + 0.07, cell, fontsize=8.5, ha="center", va="center")
    ax.text(0, 1.0, "Nouns in the path, verbs in the method.\nActions that don't fit CRUD become a sub-resource\n(e.g. POST /orders/{id}/cancellation).",
            fontsize=9, color=GRAY)
    save(fig, OUT, "01_resources_vs_actions.png")


# ------------------------------------------------------------------ 02 idempotency under retries (simulation)
def fig_idempotency():
    n = 10000
    p_lost_response = np.linspace(0, 0.10, 11)   # server processed it, but the response got lost -> client retries
    dup_naive, dup_key = [], []
    for p in p_lost_response:
        charges_naive = 0; charges_key = 0
        for _ in range(n):
            processed_keys = set(); key = object()
            attempts = 0
            while True:
                attempts += 1
                charges_naive += 1                       # POST without idempotency: every attempt creates a charge
                if key not in processed_keys:
                    processed_keys.add(key); charges_key += 1   # with Idempotency-Key: only the first attempt charges
                if rng.random() > p or attempts == 3:
                    break
        dup_naive.append((charges_naive - n) / n * 100)
        dup_key.append((charges_key - n) / n * 100)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(p_lost_response * 100, dup_naive, "o-", color=RED, lw=2.3, label="POST /payments, client retries on timeout")
    ax.plot(p_lost_response * 100, dup_key, "o-", color=GREEN, lw=2.3, label="same, but with an Idempotency-Key header")
    ax.set_xlabel("% of requests whose RESPONSE is lost (server already processed them)")
    ax.set_ylabel("duplicate charges (% of payments)")
    ax.set_title("Why idempotency matters: simulated 10,000 payments per point\n(networks lose responses; clients retry)")
    ax.legend(fontsize=9); ax.grid(alpha=0.3)
    save(fig, OUT, "02_idempotency_retries.png")


# ------------------------------------------------------------------ 03 status code decision tree
def fig_status_tree():
    fig, ax = canvas(13, 6.4, (0, 13), (0, 6.4))
    ax.text(6.5, 6.15, "Choosing a status code: a decision tree", ha="center", fontsize=12, weight="bold")
    box(ax, 5.3, 5.0, 2.4, 0.7, "Did it succeed?", fc="#f9fafb", ec=DARK, fs=10, weight="bold")
    # success branch
    box(ax, 0.3, 3.7, 3.6, 0.7, "yes → what kind of success?", fc="#f0fdf4", ec=GREEN, fs=9)
    arrow(ax, 5.3, 5.2, 2.1, 4.4, color=GREEN)
    for i, (code, txt) in enumerate([("200 OK", "read / general success"), ("201 Created", "new resource + Location"),
                                     ("202 Accepted", "queued, finishes later"), ("204 No Content", "success, empty body")]):
        box(ax, 0.3, 2.8 - i * 0.72, 3.6, 0.6, f"{code}  —  {txt}", fc="white", ec=GREEN, fs=8.5)
    # client error
    box(ax, 4.4, 3.7, 4.2, 0.7, "no, CLIENT's fault → 4xx (don't retry as-is)", fc="#fffbeb", ec=AMBER, fs=9)
    arrow(ax, 6.5, 5.0, 6.5, 4.4, color=AMBER)
    for i, (code, txt) in enumerate([("400", "malformed / invalid request"), ("401", "who are you? (no / bad auth)"),
                                     ("403", "I know you; you may not"), ("404", "no such resource"),
                                     ("409", "conflicts with current state"), ("422", "valid JSON, breaks business rules"),
                                     ("429", "too many requests (retry after)")]):
        box(ax, 4.4, 2.8 - i * 0.4, 4.2, 0.34, f"{code}  {txt}", fc="white", ec=AMBER, fs=8)
    # server error
    box(ax, 9.1, 3.7, 3.7, 0.7, "no, SERVER's fault → 5xx (may retry)", fc="#fef2f2", ec=RED, fs=9)
    arrow(ax, 7.7, 5.2, 10.9, 4.4, color=RED)
    for i, (code, txt) in enumerate([("500", "unexpected bug"), ("502", "bad upstream response"),
                                     ("503", "overloaded / maintenance"), ("504", "upstream timed out")]):
        box(ax, 9.1, 2.8 - i * 0.72, 3.7, 0.6, f"{code}  —  {txt}", fc="white", ec=RED, fs=8.5)
    save(fig, OUT, "03_status_code_tree.png")


# ------------------------------------------------------------------ 04 retries with backoff (simulation)
def fig_backoff():
    clients, T = 5000, 60.0
    outage_end = 10.0
    capacity = 400  # requests / second the service can take
    bins = np.arange(0, T + 0.5, 0.5)
    fig, ax = plt.subplots(figsize=(9, 4))
    for label, strat, col in [("immediate retry every 1 s (no backoff)", "fixed", RED),
                              ("exponential backoff, no jitter", "exp", AMBER),
                              ("exponential backoff + full jitter", "jitter", GREEN)]:
        times = []
        for c in range(clients):
            t = rng.uniform(0, 1.0)
            attempt = 0
            while t < T:
                times.append(t)
                if t >= outage_end:
                    break
                attempt += 1
                base = min(1.0 * 2 ** (attempt - 1), 30)
                wait = 1.0 if strat == "fixed" else (base if strat == "exp" else rng.uniform(0, base))
                t += wait
        h, _ = np.histogram(times, bins=bins)
        ax.plot(bins[:-1], h / 0.5, color=col, lw=2, label=label)
    ax.axvspan(0, outage_end, color=RED, alpha=0.07); ax.text(3.5, 25000, "service down (503)", color=RED, fontsize=9)
    ax.axhline(capacity, color=GRAY, ls="--"); ax.text(30, capacity * 1.25, "service capacity", color=GRAY, fontsize=9)
    ax.annotate("waves of synchronized\nretries (1, 3, 7, 15 s)", (15.2, 9000), (20, 3000), fontsize=8.5, color=AMBER,
                arrowprops=dict(arrowstyle="->", color=AMBER))
    ax.set_yscale("log"); ax.set_ylim(10, 60000)
    ax.set_xlabel("seconds"); ax.set_ylabel("requests per second hitting the API (log)")
    ax.set_title("5,000 clients retrying through a 10-second outage (simulation)\n"
                 "synchronized retries arrive in spikes; jitter spreads them out")
    ax.legend(fontsize=8.5); ax.set_xlim(0, 45)
    save(fig, OUT, "04_retry_backoff.png")


# ------------------------------------------------------------------ 05 error anatomy
def fig_error():
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.6), gridspec_kw=dict(width_ratios=[0.7, 1.3]))
    for ax in axes:
        ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax = axes[0]; ax.set_title("✗ Unhelpful", color=RED)
    ax.text(0.5, 7, 'HTTP/1.1 200 OK\n\n{\n  "success": false,\n  "msg": "something went wrong"\n}', family="monospace",
            fontsize=10, va="top", bbox=dict(fc="#fef2f2", ec=RED, boxstyle="round,pad=0.6"))
    ax.text(0.5, 1.5, "status says success, body says failure,\nno code a program can branch on,\nno field-level detail", fontsize=9, color=RED)
    ax = axes[1]; ax.set_title("✓ Structured (RFC 9457 'Problem Details' style)", color=GREEN)
    code = ('HTTP/1.1 422 Unprocessable Content\n'
            'Content-Type: application/problem+json\n\n'
            '{\n'
            '  "type": "https://api.shop.com/errors/validation",\n'
            '  "title": "Validation failed",\n'
            '  "status": 422,\n'
            '  "code": "VALIDATION_FAILED",\n'
            '  "detail": "2 fields are invalid",\n'
            '  "errors": [\n'
            '    {"field": "email", "code": "INVALID_FORMAT"},\n'
            '    {"field": "age",   "code": "MIN_VALUE", "min": 18}\n'
            '  ],\n'
            '  "request_id": "req_8f3a2c"\n'
            '}')
    ax.text(-0.3, 9.6, code, family="monospace", fontsize=8.3, va="top", bbox=dict(fc="#f0fdf4", ec=GREEN, boxstyle="round,pad=0.5"))
    ax.text(7.2, 9.5, "type / code  → machine-readable:\n    the client's code branches on it\n\n"
                      "title / detail  → human-readable:\n    show to the user or log it\n\n"
                      "status  → repeats the HTTP status\n\n"
                      "errors[]  → exactly which fields\n    failed and why\n\n"
                      "request_id  → find this exact\n    request in the server logs",
            fontsize=9, color=GREEN, va="top")
    save(fig, OUT, "05_error_anatomy.png")


# ------------------------------------------------------------------ 06 URL anatomy
def fig_url():
    fig, ax = canvas(13, 4.6, (0, 13), (0, 4.6))
    ax.text(0.2, 4.3, "GET https://api.shop.com/v1/products?category=shoes&in_stock=true&min_price=20&sort=-price&limit=20&cursor=eyJpZCI6NDJ9",
            family="monospace", fontsize=9.3, weight="bold")
    parts = [("GET", DARK, "method: the operation (read)"), ("https://api.shop.com", GRAY, "host"),
             ("/v1", PURPLE, "version: one consistent strategy for the whole API"),
             ("/products", BLUE, "path: WHICH resource (a plural noun)"),
             ("?category=shoes&in_stock=true&min_price=20", AMBER, "query: optional filters that refine the collection"),
             ("&sort=-price&limit=20&cursor=eyJpZCI6NDJ9", TEAL, "query: sorting & pagination, same names on every endpoint")]
    for i, (text, col, lab) in enumerate(parts):
        y = 3.6 - i * 0.5
        ax.text(0.4, y, text, family="monospace", fontsize=10, color=col, weight="bold", va="center")
        ax.text(7.2, y, lab, fontsize=9.5, color=col, va="center")
    ax.text(0.4, 0.35, "✗  GET /products/category/shoes/instock/true/price/20/sort/price-desc      "
                       "✗  GET /products?action=delete&id=7", family="monospace", fontsize=9.5, color=RED)
    save(fig, OUT, "06_url_anatomy.png")


# ------------------------------------------------------------------ 07 versioning timeline
def fig_versioning():
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.4), gridspec_kw=dict(width_ratios=[1.2, 1]))
    ax = axes[0]
    months = np.arange(0, 19)
    v1 = np.clip(100 - np.maximum(0, months - 3) * 9, 0, 100)
    v1[months >= 15] = 0
    ax.fill_between(months, 0, v1, color=BLUE, alpha=0.7, label="clients on v1")
    ax.fill_between(months, v1, 100, where=months >= 3, color=GREEN, alpha=0.7, label="clients on v2")
    for m, lab, yy in [(3, "v2 released\n+ migration guide", 101), (6, "v1 deprecated\n(Deprecation header)", 113),
                       (12, "sunset date\nreminders sent", 101), (15, "v1 removed\n(410 Gone)", 113)]:
        ax.axvline(m, color=DARK, ls=":", lw=1); ax.text(m + 0.15, yy, lab, fontsize=7.5, va="bottom")
    ax.set_xlim(0, 18); ax.set_ylim(0, 135); ax.set_xlabel("months"); ax.set_ylabel("% of API traffic")
    ax.set_title("A well-run breaking change: overlap, warn, measure, then sunset", pad=30)
    ax.legend(loc="lower left", fontsize=8)
    ax = axes[1]; ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.set_title("Breaking or not?")
    rows = [("add an optional response field", False), ("add an optional request parameter", False),
            ("add a new endpoint", False), ("remove or rename a field", True), ("change a field's type\n(price: 19.99 → {amount, currency})", True),
            ("make an optional parameter required", True), ("change default sort / page size", True),
            ("add a new enum value", None)]
    for i, (t, br) in enumerate(rows):
        y = 9.2 - i * 1.15
        sym, col, lab = ("✓", GREEN, "safe") if br is False else (("✗", RED, "breaking") if br else ("⚠", AMBER, "can break strict clients"))
        ax.text(0.2, y, sym, fontsize=14, color=col, va="center")
        ax.text(0.9, y, t, fontsize=9, va="center")
        ax.text(9.9, y, lab, fontsize=8.5, color=col, va="center", ha="right")
    save(fig, OUT, "07_versioning.png")


# ------------------------------------------------------------------ 08 offset vs cursor pagination (measured)
def fig_pagination():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE products(id INTEGER PRIMARY KEY, name TEXT, price REAL, created_at INTEGER)")
    N = 1_000_000
    db.executemany("INSERT INTO products VALUES (?,?,?,?)",
                   ((i, f"p{i}", float(i % 997), i) for i in range(1, N + 1)))
    db.commit()
    offsets = [0, 10_000, 100_000, 250_000, 500_000, 750_000, 990_000]
    t_off, t_cur = [], []
    for off in offsets:
        reps = 5
        t0 = time.perf_counter()
        for _ in range(reps):
            db.execute("SELECT * FROM products ORDER BY id LIMIT 20 OFFSET ?", (off,)).fetchall()
        t_off.append((time.perf_counter() - t0) / reps * 1000)
        t0 = time.perf_counter()
        for _ in range(reps):
            db.execute("SELECT * FROM products WHERE id > ? ORDER BY id LIMIT 20", (off,)).fetchall()
        t_cur.append((time.perf_counter() - t0) / reps * 1000)
    fig, ax = plt.subplots(figsize=(8, 4))
    pages = np.array(offsets) / 20
    ax.plot(pages, t_off, "o-", color=RED, lw=2.3, label="offset:  ?page=N   (LIMIT 20 OFFSET 20·N)")
    ax.plot(pages, t_cur, "o-", color=GREEN, lw=2.3, label="cursor:  ?cursor=<last id>   (WHERE id > last LIMIT 20)")
    ax.set_xlabel("page number"); ax.set_ylabel("query time (ms, measured)")
    ax.set_title("Measured on SQLite with 1,000,000 rows:\ndeep offset pages get slower, cursor pages stay flat")
    ax.legend(fontsize=9); ax.grid(alpha=0.3)
    save(fig, OUT, "08_pagination_offset_vs_cursor.png")
    print("offset ms", [round(t, 2) for t in t_off]); print("cursor ms", [round(t, 3) for t in t_cur])


if __name__ == "__main__":
    fig_resources(); fig_idempotency(); fig_status_tree(); fig_backoff(); fig_error(); fig_url(); fig_versioning()
    fig_pagination()
