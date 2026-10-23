"""pytest fixtures shared by every test file in this folder.

A fixture is a function pytest runs for you and passes in by parameter name --
the same idea as FastAPI's Depends, just for tests.
"""
import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


@pytest.fixture
def client(tmp_path):
    # A brand-new SQLite file per test: tests can't leak data into each other.
    settings = Settings(database_url=f"sqlite+aiosqlite:///{tmp_path / 'test.db'}", jwt_secret="test-secret-at-least-32-bytes-long-xyz")
    app = create_app(settings)
    with TestClient(app) as c:  # `with` runs the lifespan (startup/shutdown)
        yield c


@pytest.fixture
def auth_headers(client):
    """Register a user, log in, and return the Authorization header."""
    client.post("/auth/register", json={"email": "ada@example.com", "password": "correct-horse"})
    token = client.post("/auth/token", json={"email": "ada@example.com", "password": "correct-horse"}).json()
    return {"Authorization": f"Bearer {token['access_token']}"}
