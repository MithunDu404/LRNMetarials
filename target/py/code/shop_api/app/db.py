"""Database plumbing: the declarative base and the per-request session dependency.

The engine (which owns the connection pool) is created once, in main.lifespan,
and stored on app.state. Each request borrows one AsyncSession from it.
"""
import logging
from collections.abc import AsyncIterator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

log = logging.getLogger("shop.db")


class Base(DeclarativeBase):
    """Every ORM model inherits from this, so Base.metadata knows every table."""


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    """A 'yield dependency': code before yield is setup, code after is cleanup.

    `async with` guarantees the session is closed (its connection goes back to
    the pool) even if the endpoint raised an exception.
    """
    sessionmaker = request.app.state.sessionmaker
    async with sessionmaker() as session:
        log.info("get_session: opened a session")
        try:
            yield session
        except Exception:
            # Anything uncommitted is thrown away; the exception keeps propagating.
            await session.rollback()
            log.info("get_session: rolled back after an error")
            raise
        finally:
            log.info("get_session: closing session")
