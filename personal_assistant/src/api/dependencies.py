from typing import Annotated

from fastapi.params import Depends
from fastapi.security import SecurityScopes
from sqlmodel.ext.asyncio.session import AsyncSession

from personal_assistant.src.configs.auth import oauth2_scheme
from personal_assistant.src.models import UserTable
from personal_assistant.src.repositories.database_session import get_session
from personal_assistant.src.services.authenticate import AuthAuthenticate

DbSessionDepends = Annotated[AsyncSession, Depends(get_session)]


async def get_current_user_dependency(
    db_session: DbSessionDepends,
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserTable:
    auth_utils = AuthAuthenticate(db_session=db_session)
    return await auth_utils.get_current_user(
        security_scopes=security_scopes, token=token
    )
