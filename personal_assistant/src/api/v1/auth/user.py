from fastapi import APIRouter, Security

from personal_assistant.src.api.dependencies import (
    DbSessionDepends,
    get_current_user_dependency,
)
from personal_assistant.src.repositories.user import UserRepository
from personal_assistant.src.schemas.auth.user import UserGet, UserCreate
from personal_assistant.src.services.auth.authenticate import AuthAuthenticate

user_router = APIRouter()


@user_router.get("/")
async def get_user(
    db_session: DbSessionDepends,
    token: object = Security(get_current_user_dependency, scopes=["users:read"]),
) -> list[UserGet]:
    return await UserRepository(db_session=db_session).get_all_users()


@user_router.get("/me")
async def get_current_user(
    db_session: DbSessionDepends,
    token: object = Security(get_current_user_dependency, scopes=["me:read"]),
) -> list[UserGet]:
    return await AuthAuthenticate(db_session=db_session).get_current_user(token=token)


@user_router.post("/")
async def create_user(user: UserCreate, db_session: DbSessionDepends) -> UserGet:
    return await UserRepository(db_session=db_session).create_user(user)
