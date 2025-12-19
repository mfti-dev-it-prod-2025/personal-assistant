from typing import Any

import sqlalchemy
from sqlalchemy import GenerativeSelect, func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from personal_assistant.src.exceptions import UserAlreadyExist
from personal_assistant.src.models import UserTable
from personal_assistant.src.schemas.user import UserParams, UserCreate
from personal_assistant.src.services.password import Password


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_users(self, params: UserParams) -> list[UserTable]:
        statement = select(UserTable)
        if params.limit:
            statement = statement.limit(params.limit)
        if params.offset:
            statement = statement.offset(params.offset)
        statement = self._filter_by_params(params, statement)
        return (await self.db_session.exec(statement)).all()

    def _filter_by_params(
        self,
        params: UserParams,
        statement: SelectOfScalar[Any] | GenerativeSelect | Any,
    ) -> Any:
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
        return statement

    async def get_response_count(self, params: UserParams) -> int:
        statement = select(func.count()).select_from(UserTable)
        statement = self._filter_by_params(params=params, statement=statement)
        return await self.db_session.scalar(statement)

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
