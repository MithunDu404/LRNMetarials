"""Auth routes: register and log in. Thin: validate, call a service, shape the reply."""
from fastapi import APIRouter, status

from ..deps import SettingsDep, UserServiceDep
from ..schemas import LoginIn, Token, UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, users: UserServiceDep):
    # Returns the ORM User (which HAS password_hash); response_model=UserOut filters it out.
    return await users.register(data)


@router.post("/token", response_model=Token)
async def login(data: LoginIn, users: UserServiceDep, settings: SettingsDep):
    # Note: the OAuth2 spec's login is a *form* post (needs python-multipart).
    # This demo takes JSON to keep dependencies small; the token that comes back is the same.
    token = await users.login(data.email, data.password, settings)
    return Token(access_token=token)
