import uuid
from datetime import timedelta, datetime, timezone
from personal_assistant.src.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

from personal_assistant.src.configs.auth import ROLES_TO_SCOPES, oauth2_scheme
from personal_assistant.src.models import UserTable
from personal_assistant.src.schemas.auth.user import UserGet
from personal_assistant.src.services.auth.password import Password
from typing import Optional, Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes

from personal_assistant.src.repositories.user import UserRepository
from personal_assistant.src.configs.app import settings


class AuthAuthenticate:
    def __init__(self, db_session: AsyncSession):
        self.password_service = Password()
        self.user_repository = UserRepository(db_session=db_session)

    def create_access_token(
        self,
        *,
        subject: str,
        scopes: list[str] | None = None,
        expires_delta: timedelta | None = None,
    ) -> str:
        to_encode: dict = {"sub": subject}
        if scopes:
            to_encode.update({"scopes": scopes})
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.jwt.jwt_secret,
            algorithm=settings.jwt.jwt_algorithm,
        )
        return encoded_jwt

    async def authenticate_user(self, email: str, password: str) -> UserGet | None:
        logger.info(f"authentificating user with email: {email}")
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            logger.info(f"User was not found with credentials: {email}")
            return None
        if not self.password_service.verify_password(password, user.hashed_password):
            logger.info(f"User provided incorrect password: {email}")
            return None
        logger.info(f"User was found, returning the instance: {email}")
        return UserGet(**user.model_dump())

    def get_user_scopes(self, user: UserGet) -> list[str]:
        return ROLES_TO_SCOPES[user.role.value]

    async def get_current_user(
        self,
        security_scopes: SecurityScopes,
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> UserTable:
        if settings.jwt.jwt_bypass_auth:
            return UserTable(
                id=uuid.UUID,
                email="test@test.ru",
                role="admin",
                hashed_password=self.password_service.get_password_hash("test"),
                telegram_id=1234567890,
                name="Test",
            )
        authenticate_value = (
            f'Bearer scope="{" ".join(security_scopes.scopes)}"'
            if security_scopes.scopes
            else "Bearer"
        )
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )

        payload = jwt.decode(
            token, settings.jwt.jwt_secret, algorithms=[settings.jwt.jwt_algorithm]
        )
        subject: Optional[str] = payload.get("sub")
        token_scopes: list[str] = payload.get("scopes", [])
        if subject is None:
            raise credentials_exception

        user = await self.user_repository.get_user_by_id(subject)
        if not user:
            raise credentials_exception

        for scope in security_scopes.scopes:
            if scope not in token_scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )

        return user
