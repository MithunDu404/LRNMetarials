"""End-to-end tests through the real HTTP layer (TestClient calls the ASGI app in-process)."""
from app.deps import get_current_user
from app.models import User


def test_register_never_returns_password_hash(client):
    r = client.post("/auth/register", json={"email": " Ada@Example.com ", "password": "correct-horse"})
    assert r.status_code == 201
    body = r.json()
    assert body == {"id": 1, "email": "ada@example.com", "is_admin": False}  # normalised, no hash


def test_duplicate_email_is_409_with_error_shape(client):
    payload = {"email": "ada@example.com", "password": "correct-horse"}
    client.post("/auth/register", json=payload)
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 409
    assert r.json() == {"error": {"code": "conflict", "message": "email already registered"}}


def test_wrong_password_is_401(client, auth_headers):
    r = client.post("/auth/token", data={"username": "ada@example.com", "password": "wrong-pass"})
    assert r.status_code == 401
    assert r.headers["WWW-Authenticate"] == "Bearer"


def test_orders_need_a_token(client):
    assert client.get("/orders").status_code == 401


def test_validation_error_is_422(client, auth_headers):
    r = client.post("/orders", json={"item": "pen", "quantity": 0, "unit_price_cents": 150}, headers=auth_headers)
    assert r.status_code == 422
    assert r.json()["detail"][0]["loc"] == ["body", "quantity"]


def test_create_and_read_order(client, auth_headers):
    r = client.post("/orders", json={"item": "pen", "quantity": 3, "unit_price_cents": 150}, headers=auth_headers)
    assert r.status_code == 201
    order = r.json()
    assert order["total_cents"] == 450
    assert client.get(f"/orders/{order['id']}", headers=auth_headers).json() == order
    assert client.get("/orders/999", headers=auth_headers).status_code == 404


def test_cursor_pagination(client, auth_headers):
    for i in range(5):
        client.post("/orders", json={"item": f"item{i}", "quantity": 1, "unit_price_cents": 100}, headers=auth_headers)
    page1 = client.get("/orders?limit=2", headers=auth_headers).json()
    page2 = client.get(f"/orders?limit=2&cursor={page1['next_cursor']}", headers=auth_headers).json()
    page3 = client.get(f"/orders?limit=2&cursor={page2['next_cursor']}", headers=auth_headers).json()
    assert [o["item"] for o in page1["items"] + page2["items"] + page3["items"]] == [f"item{i}" for i in range(5)]
    assert page3["next_cursor"] is None


def test_users_me_is_not_swallowed_by_user_id_route(client, auth_headers):
    assert client.get("/users/me", headers=auth_headers).json()["email"] == "ada@example.com"


def test_non_admin_cannot_read_other_users(client, auth_headers):
    assert client.get("/users/1", headers=auth_headers).status_code == 403


def test_dependency_override_skips_auth(client):
    # Swap a dependency for the duration of a test: no token needed.
    client.app.dependency_overrides[get_current_user] = lambda: User(id=42, email="fake@x.io", is_admin=True, password_hash="")
    try:
        assert client.get("/users/me").json() == {"id": 42, "email": "fake@x.io", "is_admin": True}
    finally:
        client.app.dependency_overrides.clear()


def test_health(client):
    assert client.get("/healthz").json() == {"status": "alive"}
    assert client.get("/readyz").json() == {"status": "ready"}
