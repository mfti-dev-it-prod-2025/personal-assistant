from fastapi.params import Depends
from sqlalchemy.sql.annotation import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession

from personal_assistant.src.models.database_session import get_session

DbSessionDepends = Annotated[AsyncSession, Depends(get_session)]
