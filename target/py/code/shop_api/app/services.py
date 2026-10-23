"""Services: the business rules. No HTTP, no SQL strings -- just decisions.

Because a service only needs a session, the same code could be called from an
HTTP route, a CLI command, a test, or a background worker.
"""
import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .config import Settings
from .errors import AuthError, Conflict, NotFound
from .models import Order, User
from .repositories import OrderRepository, UserRepository
from .schemas import OrderCreate, UserCreate
from .security import create_access_token, hash_password, verify_password

log = logging.getLogger("shop.service")


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = UserRepository(session)

    async def register(self, data: UserCreate) -> User:
        if await self.users.get_by_email(data.email):
            raise Conflict("email already registered")
        user = User(email=data.email, password_hash=hash_password(data.password))
        self.users.add(user)
        try:
            await self.session.commit()
        except IntegrityError:
            # Two requests raced past the check above; the UNIQUE index caught it.
            await self.session.rollback()
            raise Conflict("email already registered") from None
        return user

    async def login(self, email: str, password: str, settings: Settings) -> str:
        user = await self.users.get_by_email(email.strip().lower())
        # Same message for "no such user" and "wrong password": don't reveal which emails exist.
        if user is None or not verify_password(password, user.password_hash):
            raise AuthError("incorrect email or password")
        return create_access_token(user.id, settings)


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.orders = OrderRepository(session)

    async def place_order(self, user: User, data: OrderCreate) -> Order:
        log.info("OrderService.place_order: computing total")
        order = Order(
            user_id=user.id,
            item=data.item,
            quantity=data.quantity,
            total_cents=data.quantity * data.unit_price_cents,
        )
        self.orders.add(order)
        await self.session.commit()  # the unit of work is complete
        log.info("OrderService.place_order: committed order id=%d", order.id)
        return order

    async def get_order(self, user: User, order_id: int) -> Order:
        order = await self.orders.get_for_user(order_id, user.id)
        if order is None:
            # 404, not 403: don't confirm that someone else's order id exists.
            raise NotFound(f"order {order_id} not found")
        return order

    async def list_orders(self, user: User, cursor: int | None, limit: int) -> tuple[list[Order], int | None]:
        # Ask for one extra row: if it comes back, there is a next page.
        rows = await self.orders.list_for_user(user.id, cursor, limit + 1)
        has_more = len(rows) > limit
        rows = rows[:limit]
        next_cursor = rows[-1].id if has_more else None
        return rows, next_cursor
