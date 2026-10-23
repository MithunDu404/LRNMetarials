"""Domain errors and the one place that turns them into HTTP responses.

Services raise plain Python exceptions that know nothing about HTTP.
register_error_handlers() maps them to status codes and one JSON error shape.
"""
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

log = logging.getLogger("shop.errors")


class DomainError(Exception):
    status_code = 400
    code = "bad_request"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class NotFound(DomainError):
    status_code = 404
    code = "not_found"


class Conflict(DomainError):
    status_code = 409
    code = "conflict"


class AuthError(DomainError):
    status_code = 401
    code = "unauthorized"


class Forbidden(DomainError):
    status_code = 403
    code = "forbidden"


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def handle_domain_error(request: Request, exc: DomainError) -> JSONResponse:
        log.info("error handler: %s -> %d", type(exc).__name__, exc.status_code)
        headers = {"WWW-Authenticate": "Bearer"} if exc.status_code == 401 else None
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.code, "message": exc.message}},
            headers=headers,
        )
