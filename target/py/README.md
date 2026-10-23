# Python for Backends: Reading Order

This folder teaches you to **read, understand and judge a Python backend**: someone else's, or one an LLM wrote for you. It goes with your earlier Python notes. It doesn't replace them.

> **Facts re-checked:** 23 October 2026 (FastAPI 0.143, Starlette 1.7, Pydantic 2.14, SQLAlchemy 2.1, Uvicorn 0.54, Python 3.12).

## Reading order

| Step | File | What you get |
|---|---|---|
| (done) | `notes/py-dsa.md` | The Python object model and the C++ STL → stdlib mapping |
| **1** | [Part 1: The Python You Need](Reading%20a%20Python%20Backend%201%20-%20The%20Python%20You%20Need.md) | Imports, decorators, type hints that libraries act on, `with`/`yield`, async done right, exceptions, Pydantic, each shown in backend code with real output |
| **2** | [Part 2: A Codebase Tour and One Request Traced](Reading%20a%20Python%20Backend%202%20-%20A%20Codebase%20Tour%20and%20One%20Request%20Traced.md) | A real, runnable FastAPI app, walked file by file, and one request traced through every layer, with three measured surprises |
| **3** | [Part 3: Backend Concepts, Decisions and Unfamiliar Code](Reading%20a%20Python%20Backend%203%20-%20Backend%20Concepts%20Decisions%20and%20Unfamiliar%20Code.md) | Transactions, pools, N+1, security, state, timeouts, queues, workers; a 10-step method for any codebase (including Flask and Django); a review checklist for LLM-written code |
| alongside | `notes/py-backend.md` | Deeper notes per concept (GIL, ASGI, DI, SQLAlchemy, JWT, Celery, Docker). Corrections are marked inline |
| practice | [Python Mastery for C++ Engineers](../Python%20Mastery%20for%20C%2B%2B%20Engineers%20-%20DSA%20and%20Backend%20Systems.md) | 26 two-minute drills. Each Part 1 section names the matching drill |

## What's in the folder

| Path | What it is |
|---|---|
| [code/shop_api/](code/shop_api/README.md) | The demo backend: FastAPI + async SQLAlchemy + SQLite, Argon2 + JWT auth, orders with keyset pagination, 11 tests, and `trace_request.py` |
| [code/python_for_backend.py](code/python_for_backend.py) | 11 runnable demos used by Part 1 (output saved in `code/python_for_backend_output.txt`) |
| [images/make_figs.py](images/make_figs.py) | Builds the three figures. All three are **measured** on your machine: event-loop blocking, N+1 queries, password-hash cost |

## Run everything

From the repository root:

```bash
py -3.12 -m pip install fastapi uvicorn sqlalchemy aiosqlite greenlet pydantic-settings pyjwt "pwdlib[argon2]" pytest httpx matplotlib numpy
py -3.12 target/py/code/python_for_backend.py
py -3.12 target/py/images/make_figs.py
```

Then from `target/py/code/shop_api`:

```bash
py -3.12 -m pytest -q
py -3.12 trace_request.py
```
