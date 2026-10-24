"""Trace one POST /orders request through every layer of the app and print the order.

Run from this folder:  py -3.12 trace_request.py
Uses a throw-away SQLite file in a temp folder; needs no network and no keys.
"""
import logging
import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.engine import Engine

from app.config import Settings
from app.main import create_app
from app.middleware import RequestIdFilter

TRACING = False


@event.listens_for(Engine, "before_cursor_execute")
def show_sql(conn, cursor, statement, parameters, context, executemany):
    if TRACING:
        first_line = " ".join(statement.split())[:90]
        logging.getLogger("shop.sql").info("SQL  %s  %s", first_line, parameters)


def main() -> None:
    global TRACING
    handler = logging.StreamHandler(sys.stdout)
    handler.addFilter(RequestIdFilter())
    handler.setFormatter(logging.Formatter("[req %(request_id)s] %(name)-15s %(message)s"))
    root = logging.getLogger("shop")
    root.addHandler(handler)
    root.setLevel(logging.INFO)

    tmp = Path(tempfile.mkdtemp())
    settings = Settings(database_url=f"sqlite+aiosqlite:///{tmp / 'trace.db'}",
                        jwt_secret="trace-secret-at-least-32-bytes-long-abc")
    root.setLevel(logging.WARNING)  # keep setup quiet
    with TestClient(create_app(settings)) as client:
        client.post("/auth/register", json={"email": "ada@example.com", "password": "correct-horse"})
        token = client.post("/auth/token", data={"username": "ada@example.com", "password": "correct-horse"}).json()["access_token"]

        print("=== POST /orders  (X-Request-ID: demo-001) ===")
        root.setLevel(logging.INFO)
        TRACING = True
        r = client.post(
            "/orders",
            json={"item": "pen", "quantity": 3, "unit_price_cents": 150},
            headers={"Authorization": f"Bearer {token}", "X-Request-ID": "demo-001"},
        )
        print("=== client received ===")
        print("status :", r.status_code)
        print("headers:", {k: v for k, v in r.headers.items() if k.startswith("x-")})
        print("body   :", r.json())

        print("\n=== POST /orders with quantity=0 (X-Request-ID: demo-002) ===")
        r = client.post(
            "/orders",
            json={"item": "pen", "quantity": 0, "unit_price_cents": 150},
            headers={"Authorization": f"Bearer {token}", "X-Request-ID": "demo-002"},
        )
        TRACING = False
        print("status :", r.status_code)
        print("body   :", r.json())
        root.setLevel(logging.WARNING)


if __name__ == "__main__":
    main()
