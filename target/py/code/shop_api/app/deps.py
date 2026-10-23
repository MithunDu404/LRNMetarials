"""Dependencies: small functions FastAPI calls for you before an endpoint runs.

The `Annotated[X, Depends(f)]` aliases at the bottom are the modern style: a
route writes `user: CurrentUser` and FastAPI knows to run get_current_user.
"""
import logging
from typing import Annotated

import jwt
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from .config import Settings
from .db import get_session
from .errors import AuthError, Forbidden
from .models import User
from .repositories import UserRepository
from .security import decode_access_token
from .services import OrderService, UserService

log = logging.getLogger("shop.deps")

# Reads "Authorization: Bearer <token>" from the request. auto_error=False means
# a missing header gives us None instead of an automatic 401, so we own the error shape.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)


def get_app_settings(request: Request) -> Settings:
    return request.app.state.settings


SessionDep = Annotated[AsyncSession, Depends(get_session)]
SettingsDep = Annotated[Settings, Depends(get_app_settings)]


async def get_current_user(
    token: Annotated[str | None, Depends(oauth2_scheme)],
    session: SessionDep,
    settings: SettingsDep,
) -> User:
    log.info("get_current_user: checking bearer token")
    if not token:
        raise AuthError("missing bearer token")
    try:
        user_id = decode_access_token(token, settings)
    except jwt.InvalidTokenError:
        raise AuthError("invalid or expired token") from None
    user = await UserRepository(session).get(user_id)
    if user is None:
        raise AuthError("user no longer exists")
    log.info("get_current_user: token ok, user id=%d", user.id)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_admin(user: CurrentUser) -> User:
    if not user.is_admin:
        raise Forbidden("admin only")
    return user


AdminUser = Annotated[User, Depends(require_admin)]


def get_order_service(session: SessionDep) -> OrderService:
    log.info("get_order_service: building OrderService")
    return OrderService(session)


def get_user_service(session: SessionDep) -> UserService:
    return UserService(session)


OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
