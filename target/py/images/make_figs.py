"""Figures for the 'Reading a Python Backend' guide (target/py/).

Every figure is MEASURED on the machine that runs this script (timings will
differ on yours; the shapes will not). Needs numpy, matplotlib, sqlalchemy,
pwdlib[argon2]. Writes PNGs next to this script.
Run:  py -3.12 target/py/images/make_figs.py
"""
import asyncio
import hashlib
import os
import platform
import sys
import time

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, RED, GREEN, AMBER, GRAY, LIGHT = "#2563eb", "#dc2626", "#16a34a", "#d97706", "#6b7280", "#e5e7eb"
plt.rcParams.update({
    "figure.dpi": 150, "savefig.bbox": "tight", "savefig.facecolor": "white",
    "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
    "axes.titleweight": "bold", "axes.titlesize": 11, "legend.frameon": False,
})
OUT = os.path.dirname(os.path.abspath(__file__))
MACHINE = f"Measured: Python {sys.version.split()[0]}, {platform.system()}, {platform.machine()}"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name))
    plt.close(fig)
    print("wrote", name)


def note(ax, text, loc=(0.02, 0.97)):
    ax.text(*loc, text, transform=ax.transAxes, fontsize=8, color=GRAY, va="top",
            bbox=dict(fc="white", ec=LIGHT, pad=3))


# ------------------------------------------------------------------ fig 1
async def heartbeat_run(kind: str, duration=1.2, period=0.010):
    """Tick every 10 ms; at t=0.3 s a 0.5 s 'request handler' of the given kind starts."""
    loop = asyncio.get_running_loop()
    start = loop.time()
    samples = []

    async def handler():
        if kind == "await asyncio.sleep()":
            await asyncio.sleep(0.5)
        elif kind == "time.sleep() in async def":
            time.sleep(0.5)
        else:
            await asyncio.to_thread(time.sleep, 0.5)

    async def launch():
        await asyncio.sleep(0.3)
        await handler()

    task = asyncio.create_task(launch())
    due = start
    while loop.time() - start < duration:
        due += period
        await asyncio.sleep(max(0.0, due - loop.time()))
        now = loop.time()
        samples.append((now - start, (now - due) * 1000))
    await task
    return np.array(samples)


def fig01_event_loop_blocking():
    kinds = [("await asyncio.sleep()", GREEN), ("asyncio.to_thread(time.sleep)", BLUE),
             ("time.sleep() in async def", RED)]
    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    for kind, col in kinds:
        s = heartbeat_run_sync(kind)
        ax.plot(s[:, 0], s[:, 1], color=col, lw=1.8, label=f"{kind}  (worst {s[:, 1].max():.0f} ms)")
    ax.axvspan(0.3, 0.8, color=LIGHT, alpha=0.6, zorder=0)
    ax.text(0.60, 410, "a 0.5 s request\nhandler runs here", ha="center", fontsize=8, color=GRAY)
    ax.set_xlabel("time since start (s)")
    ax.set_ylabel("how late each 10 ms tick ran (ms)")
    ax.set_title("One blocking call inside async def freezes every other request")
    ax.legend(loc="upper left", fontsize=8)
    note(ax, MACHINE + "\nA ticker on the event loop stands in\nfor 'other requests'. The 10-30 ms\nsawtooth is Windows timer granularity.", (0.69, 0.62))
    save(fig, "fig01_event_loop_blocking.png")


def heartbeat_run_sync(kind):
    return asyncio.run(heartbeat_run(kind))


# ------------------------------------------------------------------ fig 2
def fig02_n_plus_one():
    from sqlalchemy import ForeignKey, create_engine, event, select
    from sqlalchemy.orm import DeclarativeBase, Mapped, Session, joinedload, mapped_column, relationship, selectinload

    class Base(DeclarativeBase):
        pass

    class User(Base):
        __tablename__ = "users"
        id: Mapped[int] = mapped_column(primary_key=True)
        orders: Mapped[list["Order"]] = relationship()

    class Order(Base):
        __tablename__ = "orders"
        id: Mapped[int] = mapped_column(primary_key=True)
        user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    sizes = [1, 10, 25, 50, 100, 200, 400]
    results = {"lazy (default)": ([], []), "selectinload": ([], []), "joinedload": ([], [])}
    for n in sizes:
        engine = create_engine("sqlite://")
        Base.metadata.create_all(engine)
        counter = {"q": 0}
        event.listen(engine, "before_cursor_execute", lambda *a: counter.__setitem__("q", counter["q"] + 1))
        with Session(engine) as s:
            s.add_all([User(id=i, orders=[Order(), Order(), Order()]) for i in range(1, n + 1)])
            s.commit()
        for label, opt in (("lazy (default)", None), ("selectinload", selectinload), ("joinedload", joinedload)):
            stmt = select(User) if opt is None else select(User).options(opt(User.orders))
            best = 1e9
            for _ in range(3):
                with Session(engine) as s:
                    counter["q"] = 0
                    t0 = time.perf_counter()
                    rows = s.execute(stmt).unique().scalars().all()
                    total = sum(len(u.orders) for u in rows)
                    best = min(best, (time.perf_counter() - t0) * 1000)
            assert total == 3 * n
            results[label][0].append(counter["q"])
            results[label][1].append(best)

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4))
    cols = {"lazy (default)": RED, "selectinload": GREEN, "joinedload": BLUE}
    for label, (qs, ms) in results.items():
        a1.plot(sizes, qs, "o-", color=cols[label], label=label)
        a2.plot(sizes, ms, "o-", color=cols[label], label=label)
    a1.set_xlabel("users loaded (3 orders each)"); a1.set_ylabel("SQL queries sent")
    a1.set_title("N+1: one query per user, plus one")
    a1.set_yscale("log"); a1.legend(fontsize=8)
    a2.set_xlabel("users loaded (3 orders each)"); a2.set_ylabel("time (ms, best of 3)")
    a2.set_title("Time, with an in-memory database")
    note(a2, MACHINE + "\nIn-memory SQLite: no network.\nOver a real network each query\nadds a round trip (~0.5 ms+),\nso the red line gets much steeper.", (0.02, 0.97))
    save(fig, "fig02_n_plus_one.png")


# ------------------------------------------------------------------ fig 3
def fig03_password_hashing():
    from pwdlib import PasswordHash
    pw = "correct-horse-battery-staple"
    argon = PasswordHash.recommended()

    def bench(fn, reps):
        t0 = time.perf_counter()
        for _ in range(reps):
            fn()
        return (time.perf_counter() - t0) / reps

    sha = bench(lambda: hashlib.sha256(pw.encode()).hexdigest(), 20000)
    pbk = bench(lambda: hashlib.pbkdf2_hmac("sha256", pw.encode(), b"salt1234", 600_000), 3)
    arg = bench(lambda: argon.hash(pw), 5)
    names = ["SHA-256\n(wrong for passwords)", "PBKDF2-SHA256\n600k iterations", "Argon2id\n(pwdlib default)"]
    secs = [sha, pbk, arg]
    fig, ax = plt.subplots(figsize=(8, 3.8))
    bars = ax.barh(names, secs, color=[RED, AMBER, GREEN])
    ax.set_xscale("log")
    ax.set_xlabel("seconds per hash (log scale)")
    ax.set_title("Password hashes are slow on purpose")
    for b, v in zip(bars, secs):
        guesses = 1 / v
        t = f"{v * 1e6:.2f} us" if v < 1e-3 else f"{v * 1000:.0f} ms"
        ax.text(v * 1.4, b.get_y() + b.get_height() / 2,
                f"{t}  ->  {guesses:,.0f} guesses/s per core", va="center", fontsize=8)
    ax.set_xlim(min(secs) / 3, max(secs) * 400)
    note(ax, MACHINE + "\nOne CPU core. GPUs speed up SHA-256\nfar more; Argon2id's 64 MiB memory\ncost is what blunts them.", (0.70, 0.29))
    save(fig, "fig03_password_hashing.png")


if __name__ == "__main__":
    fig01_event_loop_blocking()
    fig02_n_plus_one()
    fig03_password_hashing()
