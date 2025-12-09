from sqlmodel.ext.asyncio.session import AsyncSession

from personal_assistant.src.api.v1.user.params import UserParams
from personal_assistant.src.models import UserTable
from personal_assistant.src.repositories import UserRepository


class UserService:
    def __init__(self, db_session: AsyncSession):
        self.repository = UserRepository(db_session)

    async def get_users(self, params: UserParams) -> list[UserTable]:
        return await self.repository.get_users(params)

    async def create_user(self, user) -> UserTable:
        return await self.repository.create_user(user)
