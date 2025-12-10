from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from personal_assistant.src.api.dependencies import DbSessionDepends
from personal_assistant.src.schemas.auth.token import Token
from personal_assistant.src.services.auth.authenticate import AuthAuthenticate

auth_router = APIRouter()


def get_auth_service(session: DbSessionDepends) -> AuthAuthenticate:
    return AuthAuthenticate(session)


auth_service_dependency = Annotated[AuthAuthenticate, Depends(get_auth_service)]


@auth_router.post("/token")
async def login_for_access_token(
    auth_service: auth_service_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    return await auth_service.form_token(form_data)
