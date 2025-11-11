from fastapi import APIRouter

from personal_assistant.src.api.dependencies import DbSessionDepends
from personal_assistant.src.api.v1.auth.user import user_router

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status

from personal_assistant.src.configs.app import settings
from personal_assistant.src.schemas.auth.token import Token
from personal_assistant.src.schemas.auth.token_request import TokenRequest
from personal_assistant.src.services.auth.authenticate import AuthAuthenticate

auth_router = APIRouter()

auth_router.include_router(user_router, prefix="/user")



@auth_router.post("/token")
async def login_for_access_token(
        token_data: TokenRequest,
        db_session: DbSessionDepends
) -> Token:
    auth_service = AuthAuthenticate(db_session=db_session)
    user = await auth_service.authenticate_user(token_data.email, token_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.jwt.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        data=user.model_dump(), expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")