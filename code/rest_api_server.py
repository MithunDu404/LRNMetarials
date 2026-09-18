"""A tiny REST API that follows the 8 laws, using only the Python standard library.

Run it:  python code/rest_api_server.py        (starts, runs a self-test client, then exits)
Laws shown: resources + methods, predictable URLs, correct status codes, one error shape (RFC 9457 style),
query params for filtering, cursor pagination, idempotency keys for POST, versioned path (/v1).
"""
import json, threading, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from urllib.request import Request, urlopen
from urllib.error import HTTPError

PRODUCTS = {i: {"id": i, "name": f"Shoe {i}", "category": "shoes" if i % 2 else "hats",
                "price": {"amount": 20 + i, "currency": "EUR"}, "created_at": f"2026-09-{i:02d}T10:00:00Z"}
            for i in range(1, 26)}
IDEMPOTENCY = {}                                   # Idempotency-Key -> (status, body)
LOCK = threading.Lock()

def problem(status, code, title, errors=None):
    body = {"type": f"https://api.example.com/errors/{code.lower()}", "title": title,
            "status": status, "code": code, "request_id": "req_" + uuid.uuid4().hex[:8]}
    if errors:
        body["errors"] = errors
    return status, body

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):                  # keep the demo output quiet
        pass

    def send(self, status, body=None, headers=None):
        self.send_response(status)
        is_problem = isinstance(body, dict) and "code" in body and status >= 400
        self.send_header("Content-Type", "application/problem+json" if is_problem else "application/json")
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if body is not None:
            self.wfile.write(json.dumps(body).encode())

    def route(self):
        url = urlparse(self.path)
        parts = [p for p in url.path.split("/") if p]
        if len(parts) < 2 or parts[0] != "v1" or parts[1] != "products":
            return None, None, url
        return "collection" if len(parts) == 2 else "item", (parts[2] if len(parts) > 2 else None), url

    # GET /v1/products?category=shoes&limit=5&cursor=10     GET /v1/products/{id}
    def do_GET(self):
        kind, pid, url = self.route()
        if kind == "collection":
            q = parse_qs(url.query)
            try:
                limit = min(int(q.get("limit", ["10"])[0]), 100)
                cursor = int(q.get("cursor", ["0"])[0])
            except ValueError:
                return self.send(*problem(400, "INVALID_QUERY", "limit and cursor must be integers"))
            items = [p for p in PRODUCTS.values() if p["id"] > cursor
                     and ("category" not in q or p["category"] == q["category"][0])]
            page = items[:limit]
            next_cursor = str(page[-1]["id"]) if len(items) > limit else None
            return self.send(200, {"data": page, "pagination": {"next_cursor": next_cursor, "limit": limit}})
        if kind == "item":
            p = PRODUCTS.get(int(pid)) if pid.isdigit() else None
            return self.send(200, p) if p else self.send(*problem(404, "PRODUCT_NOT_FOUND", f"No product with id {pid}"))
        self.send(*problem(404, "ROUTE_NOT_FOUND", "Unknown endpoint"))

    # POST /v1/products   (Idempotency-Key header makes retries safe)
    def do_POST(self):
        kind, _, _ = self.route()
        if kind != "collection":
            return self.send(*problem(405, "METHOD_NOT_ALLOWED", "POST is only allowed on /v1/products"))
        key = self.headers.get("Idempotency-Key")
        with LOCK:
            if key and key in IDEMPOTENCY:                         # retry of a request we already processed
                status, body = IDEMPOTENCY[key]
                return self.send(status, body, {"Idempotent-Replayed": "true"})
            try:
                data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            except json.JSONDecodeError:
                return self.send(*problem(400, "MALFORMED_JSON", "Body is not valid JSON"))
            errors = []
            if not isinstance(data.get("name"), str) or not data.get("name"):
                errors.append({"field": "name", "code": "REQUIRED"})
            amount = data.get("price", {}).get("amount") if isinstance(data.get("price"), dict) else None
            if not isinstance(amount, (int, float)) or amount <= 0:
                errors.append({"field": "price.amount", "code": "MUST_BE_POSITIVE"})
            if errors:
                return self.send(*problem(422, "VALIDATION_FAILED", "Request failed validation", errors))
            new_id = max(PRODUCTS) + 1
            PRODUCTS[new_id] = {"id": new_id, "name": data["name"], "category": data.get("category", "misc"),
                                "price": {"amount": amount, "currency": data["price"].get("currency", "EUR")},
                                "created_at": "2026-09-17T12:00:00Z"}
            result = (201, PRODUCTS[new_id])
            if key:
                IDEMPOTENCY[key] = result
        self.send(*result, {"Location": f"/v1/products/{new_id}"})

    # DELETE /v1/products/{id}  -> 204, repeated DELETE -> 404 (state is the same: it's gone)
    def do_DELETE(self):
        kind, pid, _ = self.route()
        if kind != "item" or not pid.isdigit():
            return self.send(*problem(404, "ROUTE_NOT_FOUND", "Unknown endpoint"))
        with LOCK:
            if PRODUCTS.pop(int(pid), None) is None:
                return self.send(*problem(404, "PRODUCT_NOT_FOUND", f"No product with id {pid}"))
        self.send(204)

def call(method, path, body=None, headers=None):
    req = Request(BASE + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                  headers={"Content-Type": "application/json", **(headers or {})})
    try:
        with urlopen(req) as r:
            raw = r.read(); return r.status, (json.loads(raw) if raw else None), dict(r.headers)
    except HTTPError as e:
        return e.code, json.loads(e.read()), dict(e.headers)

if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    BASE = f"http://127.0.0.1:{server.server_address[1]}"
    threading.Thread(target=server.serve_forever, daemon=True).start()

    s, b, _ = call("GET", "/v1/products?category=shoes&limit=3")
    print("1. filter + paginate:", s, [p["id"] for p in b["data"]], "next_cursor =", b["pagination"]["next_cursor"])
    s, b, _ = call("GET", f"/v1/products?category=shoes&limit=3&cursor={b['pagination']['next_cursor']}")
    print("   next page:        ", s, [p["id"] for p in b["data"]])
    s, b, _ = call("GET", "/v1/products/999")
    print("2. missing item:     ", s, b["code"])
    s, b, _ = call("POST", "/v1/products", {"name": "", "price": {"amount": -5}})
    print("3. validation:       ", s, b["code"], [e["field"] for e in b["errors"]])
    key = str(uuid.uuid4())
    s1, b1, h1 = call("POST", "/v1/products", {"name": "Trail runner", "price": {"amount": 89}}, {"Idempotency-Key": key})
    s2, b2, h2 = call("POST", "/v1/products", {"name": "Trail runner", "price": {"amount": 89}}, {"Idempotency-Key": key})
    print("4. create + retry:   ", s1, "id", b1["id"], "Location", h1.get("Location"), "| retry:", s2, "id", b2["id"],
          "replayed =", h2.get("Idempotent-Replayed"), "| total products:", len(PRODUCTS))
    s, _, _ = call("DELETE", f"/v1/products/{b1['id']}")
    s_again, b_again, _ = call("DELETE", f"/v1/products/{b1['id']}")
    print("5. delete twice:     ", s, "then", s_again, b_again["code"])
    server.shutdown()
