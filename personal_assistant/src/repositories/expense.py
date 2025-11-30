import uuid
from datetime import date

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional

from personal_assistant.src.models.expense import ExpenseTable
from personal_assistant.src.models.expense_category import ExpenseCategoryTable
from personal_assistant.src.models import UserTable
from personal_assistant.src.schemas.budget.expense import ExpenseCreate, ExpenseUpdate

class ExpenseRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_expenses(self) -> list[ExpenseTable]:
        return (
            await self.db_session.exec(
                select(ExpenseTable)
            )
        ).all()

    async def get_expense_by_id(self, id: uuid.UUID) -> ExpenseTable | None:
        return (
            await self.db_session.exec(
                select(ExpenseTable).where(ExpenseTable.id == id)
            )
        ).one_or_none()

    async def get_by_user(self, email: str) -> list[ExpenseTable]:
        result = await self.db_session.exec(
            select(ExpenseTable)
            .join(UserTable, ExpenseTable.user_id == UserTable.id)
            .where(UserTable.email == email)
        )
        return result.all()

    async def get_expense_by_category(self, category: str) -> list[ExpenseTable]:
        result = await self.db_session.exec(
            select(ExpenseTable)
            .join(ExpenseCategoryTable, ExpenseTable.category_id == ExpenseCategoryTable.id)
            .where(ExpenseCategoryTable.name == category))
        return result.all()

    async def get_expenses_by_date_range(
            self,
            start_date: Optional[date] = None,
            end_date: Optional[date] = None
    ) -> list[ExpenseTable]:
        """
        Возвращает список расходов в заданном диапазоне дат.
        Если start_date не указан — с начала,
        если end_date не указан — до конца.
        """
        stmt = select(ExpenseTable)
        if start_date:
            stmt = stmt.where(ExpenseTable.date >= start_date)
        if end_date:
            stmt = stmt.where(ExpenseTable.date <= end_date)

        result = await self.db_session.exec(stmt)
        return result.all()

    async def create_expense(
        self,
        expense_data: ExpenseCreate,
        user_id: uuid.UUID,
    ) -> ExpenseTable:
        """
        Создаёт новый расход.
        """
        new_expense = ExpenseTable(
            **expense_data.model_dump(),
            user_id=user_id
        )

        self.db_session.add(new_expense)
        await self.db_session.commit()
        await self.db_session.refresh(new_expense)

        return new_expense

    async def update_expense(
        self,
        expense_id: uuid.UUID,
        update_data: ExpenseUpdate,
    ) -> ExpenseTable | None:
        """
        Обновляет существующий расход.
        """
        expense = await self.get_expense_by_id(expense_id)
        if not expense:
            return None

        update_fields = update_data.model_dump(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(expense, field, value)

        await self.db_session.commit()
        await self.db_session.refresh(expense)

        return expense