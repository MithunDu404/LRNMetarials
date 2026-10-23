"""User routes. Note the ORDER: /users/me must be registered before /users/{user_id}.

Starlette tries routes one by one, in the order they were added, and takes the
first match. If /users/{user_id} came first, "me" would be tried as a user_id.
"""
from fastapi import APIRouter

from ..deps import AdminUser, CurrentUser, SessionDep
from ..errors import NotFound
from ..repositories import UserRepository
from ..schemas import UserOut

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
async def read_me(user: CurrentUser):
    return user


@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: int, _admin: AdminUser, session: SessionDep):
    user = await UserRepository(session).get(user_id)
    if user is None:
        raise NotFound(f"user {user_id} not found")
    return user
