from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from personal_assistant.src.models import UserTable
from personal_assistant.src.schemas.auth.user import UserCreate
from personal_assistant.src.services.auth.password import Password


class UserRepository:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_by_email(self, email: str) -> UserTable:
        return (await self.db_session.exec(select(UserTable).where(UserTable.email == email))).one()

    async def get_all_users(self) -> list[UserTable]:
        return (await self.db_session.exec(select(UserTable))).all()

    async def create_user(self, user: UserCreate) -> UserTable:
        user_table = UserTable(**user.model_dump())
        user_table.hashed_password = Password().get_password_hash(user.password)
        self.db_session.add(user_table)
        await self.db_session.commit()
        await self.db_session.refresh(user_table)
        return user_table

