"""Health checks: liveness ("is the process up?") vs readiness ("can it do work?")."""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text

from ..deps import SessionDep

router = APIRouter(tags=["health"])


@router.get("/healthz")
def liveness():
    # Plain `def`: FastAPI runs it in a worker thread. Nothing here blocks anyway.
    return {"status": "alive"}


@router.get("/readyz")
async def readiness(session: SessionDep):
    try:
        await session.execute(text("SELECT 1"))
    except Exception:
        return JSONResponse(status_code=503, content={"status": "database unavailable"})
    return {"status": "ready"}
