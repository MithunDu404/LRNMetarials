"""Auth routes: register and log in. Thin: validate, call a service, shape the reply."""
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from ..deps import SettingsDep, UserServiceDep
from ..schemas import Token, UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, users: UserServiceDep):
    # Returns the ORM User (which HAS password_hash); response_model=UserOut filters it out.
    return await users.register(data)


@router.post("/token", response_model=Token)
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], users: UserServiceDep, settings: SettingsDep):
    # The OAuth2 "password flow" sends a FORM (username=...&password=...), not JSON.
    # That is what the "Authorize" button on /docs sends, so /docs works out of the box.
    # The field is called "username" by the spec; this app puts the email in it.
    token = await users.login(form.username, form.password, settings)
    return Token(access_token=token)
