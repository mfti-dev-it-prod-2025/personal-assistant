import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends

from personal_assistant.src.models.database_session import get_session
from personal_assistant.src.models.budget import ExpenseTable, ExpenseCategoryTable
from personal_assistant.src.models import UserTable
from personal_assistant.src.schemas.budget.expense import ExpenseCreate, ExpenseUpdate


class ExpenseRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session


    async def get_all_expenses(
        self, user_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> list[ExpenseTable]:
        stmt = select(ExpenseTable).where(ExpenseTable.user_id == user_id).offset(skip).limit(limit)
        result = await self.db_session.exec(stmt)
        return result.all()


    async def get_expense_by_id(self, id: uuid.UUID, user_id: uuid.UUID) -> ExpenseTable | None:
        return (
            await self.db_session.exec(
                select(ExpenseTable).where(ExpenseTable.id == id, ExpenseTable.user_id == user_id)
            )
        ).one_or_none()


    async def get_expense_by_name(self, name: str, user_id: uuid.UUID) -> ExpenseTable | None:
        return (
            await self.db_session.exec(
                select(ExpenseTable).where(ExpenseTable.name == name, ExpenseTable.user_id == user_id)
            )
        ).one_or_none()


    async def get_expenses_by_category(self, category: str, user_id: uuid.UUID) -> list[ExpenseTable]:
        result = await self.db_session.exec(
            select(ExpenseTable)
            .join(ExpenseCategoryTable, ExpenseTable.category_id == ExpenseCategoryTable.id)
            .where(ExpenseCategoryTable.name == category, ExpenseTable.user_id == user_id)
        )
        return result.all()


    async def get_expenses_by_date_range(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None, user_id: uuid.UUID = None
    ) -> list[ExpenseTable]:
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        stmt = select(ExpenseTable).where(ExpenseTable.user_id == user_id)
        if start_date:
            stmt = stmt.where(ExpenseTable.expense_date >= start_date)
        if end_date:
            stmt = stmt.where(ExpenseTable.expense_date <= end_date)

        result = await self.db_session.exec(stmt)
        return result.all()


    async def create_expense(
        self, expense_data: ExpenseCreate, user_id: uuid.UUID
    ) -> ExpenseTable:
        in_data = expense_data.model_dump()
        in_data["user_id"] = user_id
        new_expense = ExpenseTable.model_validate(in_data)

        self.db_session.add(new_expense)
        await self.db_session.commit()
        await self.db_session.refresh(new_expense)
        return new_expense


    async def update_expense(
        self,
        expense_id: uuid.UUID,
        update_data: ExpenseUpdate,
        user_id: uuid.UUID
    ) -> ExpenseTable | None:
        expense = await self.get_expense_by_id(expense_id, user_id=user_id)
        if not expense:
            return None

        update_fields = update_data.model_dump(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(expense, field, value)

        await self.db_session.commit()
        await self.db_session.refresh(expense)
        return expense


    async def delete_expense(self, expense_id: uuid.UUID, user_id: uuid.UUID) -> None:
        expense = await self.get_expense_by_id(expense_id, user_id=user_id)
        if not expense:
            return

        await self.db_session.delete(expense)
        await self.db_session.commit()


async def get_expense_repository(
    db: AsyncSession = Depends(get_session),
) -> ExpenseRepository:
    return ExpenseRepository(db)