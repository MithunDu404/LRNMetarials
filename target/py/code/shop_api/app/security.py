"""Password hashing and JWT tokens.

Uses the libraries FastAPI's own security tutorial uses (checked 2026-10-23):
pwdlib with Argon2 for passwords, PyJWT for tokens.
"""
from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from .config import Settings

_hasher = PasswordHash.recommended()  # Argon2id: slow on purpose, salted automatically


def hash_password(plain: str) -> str:
    return _hasher.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return _hasher.verify(plain, hashed)


def create_access_token(user_id: int, settings: Settings) -> str:
    expires = datetime.now(UTC) + timedelta(minutes=settings.access_token_minutes)
    payload = {"sub": str(user_id), "exp": expires}  # "sub" = subject = who this token is for
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str, settings: Settings) -> int:
    """Return the user id inside a valid token; raise jwt.InvalidTokenError otherwise.

    PyJWT checks the signature AND the expiry ("exp") for us.
    """
    payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    return int(payload["sub"])
