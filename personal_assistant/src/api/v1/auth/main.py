from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from personal_assistant.src.api.dependencies import DbSessionDepends
from personal_assistant.src.api.v1.user.user import user_router
from personal_assistant.src.configs.app import settings
from personal_assistant.src.schemas.auth.token import Token
from personal_assistant.src.services.auth.authenticate import AuthAuthenticate


auth_router = APIRouter()

auth_router.include_router(user_router, prefix="/user")


@auth_router.post("/token")
async def login_for_access_token(
    db_session: DbSessionDepends,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    auth_service = AuthAuthenticate(db_session=db_session)
    user = await auth_service.authenticate_user(
        email=form_data.username.lower(), password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    allowed_scopes = set(auth_service.get_user_scopes(user))
    requested_scopes = set(form_data.scopes or [])
    granted_scopes = (
        list(requested_scopes.intersection(allowed_scopes))
        if requested_scopes
        else list(allowed_scopes)
    )

    access_token_expires = timedelta(
        minutes=settings.jwt.jwt_access_token_expire_minutes
    )
    access_token = auth_service.create_access_token(
        subject=str(user.id), scopes=granted_scopes, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
