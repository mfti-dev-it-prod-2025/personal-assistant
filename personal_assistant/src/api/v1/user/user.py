from typing import Annotated

from fastapi import APIRouter, Security, Depends
from fastapi.security import SecurityScopes

from personal_assistant.src.api.dependencies import (
    DbSessionDepends,
    get_current_user_dependency,
)
from personal_assistant.src.api.v1.user.params import UserParams
from personal_assistant.src.models import UserTable
from personal_assistant.src.repositories.user import UserRepository
from personal_assistant.src.schemas.auth.user import UserGet, UserCreate
from personal_assistant.src.services.auth.authenticate import AuthAuthenticate

user_router = APIRouter()


@user_router.get("/")
async def get_user(
    db_session: DbSessionDepends,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["users:read"])
    ],
    user_params: Annotated[UserParams, Depends()]
) -> list[UserGet]:
    return await UserRepository(db_session=db_session).get_users(params=user_params)


@user_router.get("/me")
async def get_current_user(
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["me:read"])
    ],
) -> UserGet:
    return current_user


@user_router.post("/")
async def create_user(user: UserCreate, db_session: DbSessionDepends) -> UserGet:
    return await UserRepository(db_session=db_session).create_user(user)
