from typing import Annotated

from fastapi import APIRouter, Security, Depends

from personal_assistant.src.api.dependencies import (
    DbSessionDepends,
    get_current_user_dependency,
)
from personal_assistant.src.api.v1.user.params import UserParams
from personal_assistant.src.models import UserTable
from personal_assistant.src.schemas.auth.user import UserGet, UserCreate
from personal_assistant.src.services.user_service import UserService

user_router = APIRouter()


def get_user_service(session: DbSessionDepends) -> UserService:
    return UserService(session)


user_service_dependency = Annotated[UserService, Depends(get_user_service)]


@user_router.get("/")
async def get_user(
    user_service: user_service_dependency,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["users:read"])
    ],
    user_params: Annotated[UserParams, Depends()],
) -> list[UserGet]:
    return await user_service.get_users(params=user_params)


@user_router.get("/me")
async def get_current_user(
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["me:read"])
    ],
) -> UserGet:
    return current_user


@user_router.post("/")
async def create_user(
    user: UserCreate, user_service: user_service_dependency
) -> UserGet:
    return await user_service.create_user(user)
