from datetime import timedelta, datetime, timezone

import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from personal_assistant.src.configs.app import APPConfig, settings
from personal_assistant.src.schemas.auth.user import UserGet
from personal_assistant.src.services.auth.password import Password
from personal_assistant.src.repositories.user import UserRepository


class AuthAuthenticate:

    def __init__(self, db_session: AsyncSession):
        self.password_service = Password()
        self.user_repository = UserRepository(db_session=db_session)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.jwt.jwt_secret, algorithm=settings.jwt.jwt_algorithm)
        return encoded_jwt

    async def authenticate_user(self, email: str, password: str) -> UserGet | None:
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            return None
        if not self.password_service.verify_password(password, user.hashed_password):
            return None
        return UserGet(**user.model_dump())


