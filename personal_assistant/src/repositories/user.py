import uuid

import sqlalchemy
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from personal_assistant.src.api.v1.user.params import UserParams
from personal_assistant.src.exceptions import UserAlreadyExist
from personal_assistant.src.models import UserTable
from personal_assistant.src.schemas.auth.user import UserCreate
from personal_assistant.src.services.auth.password import Password


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_users(self, params: UserParams) -> list[UserTable]:
        statement = select(UserTable)
        if params.limit:
            statement = statement.limit(params.limit)
        if params.offset:
            statement = statement.offset(params.offset)
        for param, value in params.model_dump().items():
            if value is None:
                continue
            if param in {"limit", "offset"}:
                continue
            if "__" in param:
                field_name, operator = param.split("__", 1)
                if operator == "contains":
                    statement = statement.where(
                        getattr(UserTable, field_name).contains(value)
                    )
                    continue
            statement = statement.where(getattr(UserTable, param) == value)
        return (await self.db_session.exec(statement)).all()

    async def create_user(self, user: UserCreate) -> UserTable:
        user_table = UserTable.model_validate(
            user,
            update={"hashed_password": Password().get_password_hash(user.password)},
        )
        try:
            self.db_session.add(user_table)
            await self.db_session.commit()
            await self.db_session.refresh(user_table)
        except sqlalchemy.exc.IntegrityError:
            raise UserAlreadyExist(f"User with email {user.email} already exists")
        return user_table
