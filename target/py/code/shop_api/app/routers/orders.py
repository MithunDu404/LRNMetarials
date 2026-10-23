"""Order routes."""
import logging
from typing import Annotated

from fastapi import APIRouter, Query, status

from ..deps import CurrentUser, OrderServiceDep
from ..schemas import OrderCreate, OrderOut, Page

log = logging.getLogger("shop.route")
router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(data: OrderCreate, user: CurrentUser, orders: OrderServiceDep):
    # By the time this line runs: the JSON body is parsed and validated into
    # `data`, the token is checked and `user` loaded, and the service is built.
    log.info("route create_order: body valid, user=%d, calling service", user.id)
    order = await orders.place_order(user, data)
    log.info("route create_order: returning ORM object; FastAPI will serialise it")
    return order


@router.get("", response_model=Page[OrderOut])
async def list_orders(
    user: CurrentUser,
    orders: OrderServiceDep,
    cursor: int | None = None,                              # ?cursor=12
    limit: Annotated[int, Query(ge=1, le=100)] = 20,        # ?limit=5, validated 1..100
):
    rows, next_cursor = await orders.list_orders(user, cursor, limit)
    return Page[OrderOut](items=[OrderOut.model_validate(r) for r in rows], next_cursor=next_cursor)


@router.get("/{order_id}", response_model=OrderOut)
async def read_order(order_id: int, user: CurrentUser, orders: OrderServiceDep):
    return await orders.get_order(user, order_id)
