"""Runnable demos for 'Reading a Python Backend' Part 1 (the Python you need).

Every section prints what it shows; the guide pastes this real output.
Run:  py -3.12 target/py/code/python_for_backend.py        (offline, no keys)
Needs: fastapi/pydantic, sqlalchemy, aiosqlite, greenlet (same as shop_api).
"""
import asyncio
import functools
import inspect
import threading
import time
from contextlib import AsyncExitStack, asynccontextmanager, contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Annotated, Any, Protocol, get_type_hints


def header(title: str) -> None:
    print(f"\n{'=' * 8} {title} {'=' * (60 - len(title))}")


# ---------------------------------------------------------------- 1. decorators
def demo_decorators() -> None:
    header("1. Decorators: how @app.get('/x') works")

    class MiniRouter:
        def __init__(self):
            self.routes: dict[tuple[str, str], Any] = {}

        def get(self, path: str):              # get("/ping") RETURNS a decorator...
            def decorator(func):               # ...which receives the function...
                self.routes[("GET", path)] = func
                return func                    # ...registers it, and hands it back unchanged
            return decorator

    app = MiniRouter()

    @app.get("/ping")                          # same as: ping = app.get("/ping")(ping)
    def ping():
        return {"pong": True}

    print("registered routes:", {k: v.__name__ for k, v in app.routes.items()})
    print("calling the handler the router found:", app.routes[("GET", "/ping")]())

    def timed(func):                           # a wrapping decorator
        @functools.wraps(func)                 # keep the name/docstring/signature of func
        def wrapper(*args, **kwargs):
            t0 = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                print(f"  {func.__name__} took {(time.perf_counter() - t0) * 1000:.2f} ms")
        return wrapper

    @timed
    def slow_add(a: int, b: int) -> int:
        time.sleep(0.01)
        return a + b

    print("slow_add(2, 3) =", slow_add(2, 3))
    print("name kept by functools.wraps:", slow_add.__name__, "| signature:", inspect.signature(slow_add))


# ---------------------------------------------------------------- 2. signatures
def demo_signature_reading() -> None:
    header("2. How FastAPI reads your function signature")

    class Depends:                              # stand-in marker, like fastapi.Depends
        def __init__(self, dep):
            self.dep = dep

        def __repr__(self):
            return f"Depends({self.dep.__name__})"

    def get_db():
        ...

    class Body:                                 # stand-in for a Pydantic model
        ...

    def create_order(order_id: int, data: Body, db: Annotated[str, Depends(get_db)], limit: int = 20):
        ...

    hints = get_type_hints(create_order, include_extras=True)
    for name, param in inspect.signature(create_order).parameters.items():
        hint = hints[name]
        meta = getattr(hint, "__metadata__", ())
        if meta:
            role = f"dependency -> run {meta[0]!r} first"
        elif name == "order_id":
            role = "path parameter (its name appears in the URL '/orders/{order_id}')"
        elif isinstance(hint, type) and hint is Body:
            role = "request body (a model class)"
        else:
            role = f"query parameter, default={param.default!r}"
        shown = hint.__name__ if isinstance(hint, type) else str(hint).replace("typing.", "")
        print(f"  {name:<9} {shown:<34} {role}")
    print("FastAPI does this once at startup, not on every request.")


# ---------------------------------------------------------------- 3. tiny DI
def demo_tiny_dependency_injection() -> None:
    header("3. A 40-line Depends(): yield, caching, cleanup order")

    class Depends:
        def __init__(self, dep):
            self.dep = dep

    async def get_session():
        print("    open session")
        try:
            yield "SESSION"
        finally:
            print("    close session")

    async def get_user(session: Annotated[str, Depends(get_session)]):
        print(f"    load user using {session}")
        return "ada"

    def get_service(session: Annotated[str, Depends(get_session)]):
        print(f"    build service using {session}")
        return "OrderService"

    async def solve(func, stack: AsyncExitStack, cache: dict):
        kwargs = {}
        for name, hint in get_type_hints(func, include_extras=True).items():
            if name == "return":
                continue
            dep = hint.__metadata__[0].dep
            if dep not in cache:                       # one call per request, then cached
                if inspect.isasyncgenfunction(dep):    # yield dependency: enter it like a context manager
                    cm = asynccontextmanager(dep)(**(await solve(dep, stack, cache)))
                    cache[dep] = await stack.enter_async_context(cm)
                else:
                    result = dep(**(await solve(dep, stack, cache)))
                    cache[dep] = await result if inspect.isawaitable(result) else result
            kwargs[name] = cache[dep]
        return kwargs

    async def endpoint(user: Annotated[str, Depends(get_user)], svc: Annotated[str, Depends(get_service)]):
        print(f"    endpoint runs with user={user}, svc={svc}")
        if user == "ada" and FAIL:
            raise RuntimeError("boom")
        return {"ok": True}

    async def handle_request():
        async with AsyncExitStack() as stack:          # cleanup runs when this block exits
            kwargs = await solve(endpoint, stack, cache={})
            return await endpoint(**kwargs)

    global FAIL
    FAIL = False
    print("  request 1 (succeeds):")
    print("    response:", asyncio.run(handle_request()))
    FAIL = True
    print("  request 2 (endpoint raises):")
    try:
        asyncio.run(handle_request())
    except RuntimeError as e:
        print("    exception reached the caller:", e)


FAIL = False


# ---------------------------------------------------------------- 4. context managers
def demo_context_managers() -> None:
    header("4. Context managers: Python's RAII")

    @contextmanager
    def transaction(name: str):
        print(f"  BEGIN {name}")
        try:
            yield
        except Exception as e:
            print(f"  ROLLBACK {name} because: {e}")
            raise
        else:
            print(f"  COMMIT {name}")

    with transaction("t1"):
        print("  ...work in t1")
    try:
        with transaction("t2"):
            raise ValueError("stock went negative")
    except ValueError:
        print("  caller still sees the ValueError")


# ---------------------------------------------------------------- 5. async
async def fake_io(name: str, seconds: float) -> str:
    await asyncio.sleep(seconds)       # gives the event loop back while "waiting on the network"
    return name


def demo_async() -> None:
    header("5. async/await: sequential vs concurrent, and blocking the loop")

    async def sequential():
        return [await fake_io("db", 0.2), await fake_io("cache", 0.2), await fake_io("api", 0.2)]

    async def concurrent():
        return await asyncio.gather(fake_io("db", 0.2), fake_io("cache", 0.2), fake_io("api", 0.2))

    async def with_taskgroup():
        async with asyncio.TaskGroup() as tg:          # Python 3.11+: if one fails, the rest are cancelled
            tasks = [tg.create_task(fake_io(n, 0.2)) for n in ("db", "cache", "api")]
        return [t.result() for t in tasks]

    for fn in (sequential, concurrent, with_taskgroup):
        t0 = time.perf_counter()
        out = asyncio.run(fn())
        print(f"  {fn.__name__:<15} {out}  {time.perf_counter() - t0:.2f} s")

    async def forgot_await():
        coro = fake_io("db", 0.1)                      # no await: nothing runs!
        print("  without await you get:", type(coro).__name__, "- the function body never ran")
        coro.close()

    asyncio.run(forgot_await())

    async def ping_lateness(handler) -> float:
        """A 'ping' is due 10 ms after a slow request starts. How late does it answer?"""
        t0 = time.perf_counter()                       # perf_counter: fine-grained on every OS
        slow = asyncio.create_task(handler())          # the slow request starts first
        await asyncio.sleep(0.010)                     # ping wants to run at t0 + 10 ms
        late_ms = max(0.0, (time.perf_counter() - t0 - 0.010) * 1000)
        await slow
        return late_ms

    async def good():                                  # await-able sleep
        await asyncio.sleep(0.5)

    async def bad():                                   # blocking sleep inside async def
        time.sleep(0.5)

    async def offloaded():                             # blocking work moved to a thread
        await asyncio.to_thread(time.sleep, 0.5)

    for h in (good, bad, offloaded):
        print(f"  ping answered {asyncio.run(ping_lateness(h)):6.1f} ms late while a '{h.__name__}' handler ran")


# ---------------------------------------------------------------- 6. contextvars
def demo_contextvars() -> None:
    header("6. ContextVar: per-request 'globals'")
    request_id: ContextVar[str] = ContextVar("request_id", default="-")

    async def log(msg):
        print(f"  [{request_id.get()}] {msg}")

    async def handle(rid: str, delay: float):
        request_id.set(rid)
        await log("start")
        await asyncio.sleep(delay)
        await log("end (still my own id after other requests ran)")

    async def main():
        await asyncio.gather(handle("req-A", 0.02), handle("req-B", 0.01))

    asyncio.run(main())


# ---------------------------------------------------------------- 7. pydantic
def demo_pydantic() -> None:
    header("7. Pydantic: parse, validate, coerce, dump")
    from pydantic import BaseModel, ConfigDict, Field, ValidationError

    class OrderIn(BaseModel):
        item: str = Field(min_length=1)
        quantity: int = Field(gt=0)

    print("  '3' coerced to int:", OrderIn.model_validate({"item": "pen", "quantity": "3"}))
    try:
        OrderIn.model_validate({"item": "", "quantity": "three"})
    except ValidationError as e:
        for err in e.errors():
            print(f"  rejected {err['loc']}: {err['msg']}")

    class StrictIn(BaseModel):
        model_config = ConfigDict(strict=True)
        quantity: int

    try:
        StrictIn.model_validate({"quantity": "3"})
    except ValidationError as e:
        print("  strict mode refuses '3':", e.errors()[0]["msg"])

    @dataclass
    class OrmLikeRow:                                  # pretend ORM object with a secret field
        id: int
        email: str
        password_hash: str

    class UserOut(BaseModel):
        model_config = ConfigDict(from_attributes=True)
        id: int
        email: str

    row = OrmLikeRow(1, "ada@example.com", "$argon2id$...")
    print("  UserOut from an object:", UserOut.model_validate(row).model_dump(), "<- no password_hash")


# ---------------------------------------------------------------- 8. mutable default
def demo_mutable_default() -> None:
    header("8. The mutable-default-argument bug")

    def add_tag(tag, tags=[]):                         # the [] is created ONCE, at def time
        tags.append(tag)
        return tags

    print("  add_tag('a') ->", add_tag("a"))
    print("  add_tag('b') ->", add_tag("b"), " <- 'a' leaked from the previous call")

    def add_tag_fixed(tag, tags=None):
        tags = [] if tags is None else tags
        tags.append(tag)
        return tags

    print("  fixed:", add_tag_fixed("a"), add_tag_fixed("b"))


# ---------------------------------------------------------------- 9. Protocol
def demo_protocol() -> None:
    header("9. Protocol: duck typing you can type-check")

    class UserStore(Protocol):
        def get_email(self, user_id: int) -> str | None: ...

    class FakeStore:                                   # does NOT inherit from UserStore
        def get_email(self, user_id: int) -> str | None:
            return {1: "ada@example.com"}.get(user_id)

    def greeting(store: UserStore, user_id: int) -> str:
        email = store.get_email(user_id)
        return f"hello {email}" if email else "who are you?"

    print("  with a fake store:", greeting(FakeStore(), 1), "|", greeting(FakeStore(), 2))


# ---------------------------------------------------------------- 10. ORM traps
def demo_orm_traps() -> None:
    header("10. ORM: N+1 queries, and the async lazy-load crash")
    from sqlalchemy import ForeignKey, create_engine, event, select
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, selectinload

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

    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    count = {"n": 0}
    event.listen(engine, "before_cursor_execute", lambda *a: count.__setitem__("n", count["n"] + 1))
    with Session(engine) as s:
        s.add_all([User(id=i, orders=[Order(), Order()]) for i in range(1, 51)])
        s.commit()

    for label, stmt in [("lazy (default)", select(User)), ("selectinload", select(User).options(selectinload(User.orders)))]:
        with Session(engine) as s:
            count["n"] = 0
            total = sum(len(u.orders) for u in s.scalars(stmt))
            print(f"  {label:<15} 50 users, {total} orders -> {count['n']} SQL queries")

    async def async_lazy():
        aengine = create_async_engine("sqlite+aiosqlite://")
        from sqlalchemy.ext.asyncio import AsyncSession
        async with aengine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        async with AsyncSession(aengine) as s:
            s.add(User(id=1, orders=[Order()]))
            await s.commit()
        async with AsyncSession(aengine) as s:
            user = (await s.execute(select(User))).scalar_one()
            try:
                print(len(user.orders))
            except Exception as e:
                print(f"  async lazy load -> {type(e).__name__}: {str(e).splitlines()[0][:70]}...")
            user = (await s.execute(select(User).options(selectinload(User.orders)).execution_options(populate_existing=True))).scalar_one()
            print(f"  async + selectinload -> {len(user.orders)} order(s), no error")
        await aengine.dispose()

    asyncio.run(async_lazy())


# ---------------------------------------------------------------- 11. threads + GIL
def demo_gil() -> None:
    header("11. Threads: fine for waiting, useless for CPU (with the GIL)")
    import sys

    def cpu(n=3_000_000):
        x = 0
        for i in range(n):
            x += i
        return x

    def io():
        time.sleep(0.2)

    def run_serial(fn):
        t0 = time.perf_counter()
        for _ in range(4):
            fn()
        return time.perf_counter() - t0

    def run_threads(fn):
        t0 = time.perf_counter()
        ts = [threading.Thread(target=fn) for _ in range(4)]
        for t in ts:
            t.start()
        for t in ts:
            t.join()
        return time.perf_counter() - t0

    for label, fn in (("CPU work", cpu), ("I/O wait", io)):
        serial = min(run_serial(fn) for _ in range(3))     # best of 3 to remove noise
        threaded = min(run_threads(fn) for _ in range(3))
        print(f"  {label}: 4 in a row {serial:.2f} s | 4 threads {threaded:.2f} s")
    gil = getattr(sys, "_is_gil_enabled", lambda: True)()
    print(f"  (Python {sys.version.split()[0]}, GIL enabled: {gil})")


if __name__ == "__main__":
    demo_decorators()
    demo_signature_reading()
    demo_tiny_dependency_injection()
    demo_context_managers()
    demo_async()
    demo_contextvars()
    demo_pydantic()
    demo_mutable_default()
    demo_protocol()
    demo_orm_traps()
    demo_gil()
