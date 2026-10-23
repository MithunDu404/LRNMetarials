"""Middleware: code that wraps EVERY request, before routing and after the response.

This one gives each request an id, stores it in a ContextVar so any log line
can include it, and measures how long the request took.
"""
import logging
import time
import uuid
from contextvars import ContextVar

from fastapi import Request

log = logging.getLogger("shop.middleware")

# A ContextVar is like a global, but each request (each asyncio task) sees its own value.
request_id_var: ContextVar[str] = ContextVar("request_id", default="-")


async def request_context_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex[:8]
    token = request_id_var.set(request_id)
    start = time.perf_counter()
    log.info("middleware: start %s %s", request.method, request.url.path)
    try:
        response = await call_next(request)  # everything else happens inside this await
        elapsed_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.1f}"
        log.info("middleware: done %d in %.1f ms", response.status_code, elapsed_ms)
        return response
    finally:
        request_id_var.reset(token)


class RequestIdFilter(logging.Filter):
    """Attach the current request id to every log record as record.request_id."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        return True
