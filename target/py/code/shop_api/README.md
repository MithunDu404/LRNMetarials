# shop_api: a small, realistic FastAPI backend

The demo codebase for [Reading a Python Backend, Part 2](../../Reading%20a%20Python%20Backend%202%20-%20A%20Codebase%20Tour%20and%20One%20Request%20Traced.md).
Users register and log in (Argon2 + JWT), then create and list orders (keyset pagination).
It uses SQLite through `aiosqlite`, so it runs offline with no keys and no server to install.

```text
app/main.py          entry point: app factory, lifespan, middleware, routers
app/config.py        settings from environment variables (prefix SHOP_)
app/db.py            declarative Base + the per-request session dependency
app/models.py        SQLAlchemy tables (User, Order)
app/schemas.py       Pydantic request/response shapes
app/security.py      password hashing and JWTs
app/repositories.py  the only place that builds queries
app/services.py      business rules, commits
app/deps.py          dependencies: current user, services, Annotated aliases
app/errors.py        domain exceptions -> one JSON error shape
app/middleware.py    request id + timing for every request
app/routers/         HTTP endpoints, thin
tests/               pytest suite (TestClient)
trace_request.py     prints every layer one request passes through
```

Run from this folder (`target/py/code/shop_api`):

```bash
py -3.12 -m pip install fastapi uvicorn sqlalchemy aiosqlite greenlet pydantic-settings pyjwt "pwdlib[argon2]" pytest httpx
py -3.12 -m pytest -q
py -3.12 trace_request.py
py -3.12 -m uvicorn app.main:app --reload
```

The last command serves the app at http://127.0.0.1:8000 with interactive docs at `/docs`.
It creates `shop.db` in this folder; delete it to start fresh.
