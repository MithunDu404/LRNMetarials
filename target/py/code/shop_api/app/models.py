"""ORM models: Python classes that map to database tables (SQLAlchemy 2.x style).

`Mapped[int]` is a type hint that tells SQLAlchemy the column type and tells
your editor/mypy what the attribute holds. `mapped_column(...)` adds details.
"""
from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))  # never leaves the server
    is_admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # One user has many orders. "Order" is a string because the class is defined below.
    orders: Mapped[list["Order"]] = relationship(back_populates="user")


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (CheckConstraint("quantity > 0", name="quantity_positive"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    item: Mapped[str] = mapped_column(String(100))
    quantity: Mapped[int]
    total_cents: Mapped[int]  # money as integer cents: no float rounding errors
    status: Mapped[str] = mapped_column(String(20), default="pending")

    user: Mapped[User] = relationship(back_populates="orders")
