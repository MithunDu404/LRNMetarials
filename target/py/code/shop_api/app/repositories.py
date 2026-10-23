"""Repositories: the only code that builds SQL queries.

A repository answers questions like "find the user with this email". It does
not decide whether that is allowed, and it never commits -- the service decides
when a unit of work is complete.
"""
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Order, User

log = logging.getLogger("shop.repo")


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, user_id: int) -> User | None:
        log.info("UserRepository.get(%d)", user_id)
        return await self.session.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    def add(self, user: User) -> None:
        self.session.add(user)  # not written yet: it is written on flush/commit


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def add(self, order: Order) -> None:
        log.info("OrderRepository.add(item=%r)", order.item)
        self.session.add(order)

    async def get_for_user(self, order_id: int, user_id: int) -> Order | None:
        stmt = select(Order).where(Order.id == order_id, Order.user_id == user_id)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def list_for_user(self, user_id: int, after_id: int | None, limit: int) -> list[Order]:
        """Keyset ("cursor") pagination: WHERE id > last_seen ORDER BY id LIMIT n.

        Unlike OFFSET, the database jumps straight to the right place via the index,
        and rows inserted meanwhile cannot shift the page under the client.
        """
        stmt = select(Order).where(Order.user_id == user_id)
        if after_id is not None:
            stmt = stmt.where(Order.id > after_id)
        stmt = stmt.order_by(Order.id).limit(limit)
        return list((await self.session.execute(stmt)).scalars())
