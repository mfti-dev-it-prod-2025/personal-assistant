import uuid
from datetime import date

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional

from personal_assistant.src.models.expense_category import ExpenseCategoryTable
from personal_assistant.src.schemas.budget.expense_category import ExpenseCategoryCreate, ExpenseCategoryUpdate

class ExpenseCategoryRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_categories(self) -> list[ExpenseCategoryTable]:
        return (
            await self.db_session.exec(
                select(ExpenseCategoryTable)
            )
        ).all()

    # async def get_expense_category_by_id(self, id: uuid.UUID) -> ExpenseCategoryTable | None:
    #     return (
    #         await self.db_session.exec(
    #             select(ExpenseCategoryTable).where(ExpenseCategoryTable.id == id)
    #         )
    #     ).one_or_none()

    async def get_expense_category_by_name(self, name: str) -> ExpenseCategoryTable | None:
        return (
            await self.db_session.exec(
                select(ExpenseCategoryTable).where(ExpenseCategoryTable.name == name)
            )
        ).one_or_none()

    async def create_expense_category(
        self,
        expense_data: ExpenseCategoryCreate,
        user_id: uuid.UUID,
    ) -> ExpenseCategoryTable:
        """
        Создаёт новую категоррию расходов.
        """
        new_expense_category = ExpenseCategoryTable(
            **expense_data.model_dump(),
            user_id=user_id
        )

        self.db_session.add(new_expense_category)
        await self.db_session.commit()
        await self.db_session.refresh(new_expense_category)

        return new_expense_category

    async def update_expense_category(
        self,
        expense_name: str,
        update_data: ExpenseCategoryUpdate,
    ) -> ExpenseCategoryTable | None:
        """
        Обновляет существующий расход.
        """
        expense = await self.get_expense_category_by_name(expense_name)
        if not expense:
            return None

        update_fields = update_data.model_dump(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(expense, field, value)

        await self.db_session.commit()
        await self.db_session.refresh(expense)

        return expense