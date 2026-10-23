"""Pydantic schemas: the shapes of data crossing the HTTP boundary.

Models (models.py) describe the database. Schemas describe the API.
Keeping them separate is what stops password_hash from leaking into a response.
"""
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator

T = TypeVar("T")


# ---- input schemas: what a client may send -------------------------------
class UserCreate(BaseModel):
    email: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def normalise_email(cls, v: str) -> str:
        v = v.strip().lower()
        if "@" not in v or v.startswith("@") or v.endswith("@"):
            raise ValueError("not a valid email address")
        return v


class LoginIn(BaseModel):
    email: str
    password: str


class OrderCreate(BaseModel):
    item: str = Field(min_length=1, max_length=100)
    quantity: int = Field(gt=0, le=100)
    unit_price_cents: int = Field(gt=0)


# ---- output schemas: what the server sends back ---------------------------
class UserOut(BaseModel):
    # from_attributes=True lets Pydantic read fields off an ORM object (user.id, user.email)
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    is_admin: bool


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item: str
    quantity: int
    total_cents: int
    status: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Page(BaseModel, Generic[T]):
    """A generic page: Page[OrderOut] is 'a list of OrderOut plus a cursor'."""

    items: list[T]
    next_cursor: int | None = None
