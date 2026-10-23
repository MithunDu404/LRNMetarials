"""The entry point. `uvicorn app.main:app` imports this module and looks up `app`.

Read this file first in any FastAPI project: it tells you which routers exist,
which middleware wraps them, and what happens at startup and shutdown.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from . import models  # noqa: F401  -- importing registers the tables on Base.metadata
from .config import Settings, get_settings
from .db import Base
from .errors import register_error_handlers
from .middleware import request_context_middleware
from .routers import auth, health, orders, users

log = logging.getLogger("shop.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Runs once per process: code before `yield` at startup, after it at shutdown."""
    settings: Settings = app.state.settings
    engine = create_async_engine(settings.database_url)  # owns the connection pool
    async with engine.begin() as conn:
        # Demo shortcut. A real project runs Alembic migrations instead of create_all.
        await conn.run_sync(Base.metadata.create_all)
    app.state.sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    log.info("lifespan: startup complete")
    yield
    await engine.dispose()  # close pooled connections cleanly
    log.info("lifespan: shutdown complete")


def create_app(settings: Settings | None = None) -> FastAPI:
    """An 'app factory': tests call create_app(test_settings) to get a fresh app."""
    app = FastAPI(title="Shop API", version="1.0", lifespan=lifespan)
    app.state.settings = settings or get_settings()

    # Middleware added LAST runs FIRST (it becomes the outermost layer).
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app.state.settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.middleware("http")(request_context_middleware)

    register_error_handlers(app)
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(orders.router)
    return app


app = create_app()
