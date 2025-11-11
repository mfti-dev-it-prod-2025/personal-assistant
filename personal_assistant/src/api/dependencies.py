from typing import Annotated

from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from personal_assistant.src.models.database_session import get_session

DbSessionDepends = Annotated[AsyncSession, Depends(get_session)]
