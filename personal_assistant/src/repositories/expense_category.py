import uuid

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends

from personal_assistant.src.models.database_session import get_session
from personal_assistant.src.models.budget import ExpenseCategoryTable
from personal_assistant.src.schemas.budget.expense_category import (
    ExpenseCategoryCreate,
    ExpenseCategoryUpdate,
)


class ExpenseCategoryRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_categories(
        self, skip: int = 0, limit: int = 100
    ) -> list[ExpenseCategoryTable]:
        """
        Получает все существующие категории расходов.
        """
        stmt = select(ExpenseCategoryTable).offset(skip).limit(limit)
        result = await self.db_session.exec(stmt)
        return result.all()

    async def get_expense_category_by_id(
        self, id: uuid.UUID
    ) -> ExpenseCategoryTable | None:
        """
        Получает категорию расходов по id.
        """
        return (
            await self.db_session.exec(
                select(ExpenseCategoryTable).where(ExpenseCategoryTable.id == id)
            )
        ).one_or_none()

    async def get_expense_category_by_name(
        self, name: str
    ) -> ExpenseCategoryTable | None:
        """
        Получает категорию расходов по имени.
        """
        return (
            await self.db_session.exec(
                select(ExpenseCategoryTable).where(ExpenseCategoryTable.name == name)
            )
        ).one_or_none()

    async def create_expense_category(
        self,
        expense_category_data: ExpenseCategoryCreate,
    ) -> ExpenseCategoryTable:
        """
        Создаёт новую категорию расходов.
        """
        new_expense_category = ExpenseCategoryTable.model_validate(
            expense_category_data.model_dump()
        )

        self.db_session.add(new_expense_category)
        await self.db_session.commit()
        await self.db_session.refresh(new_expense_category)

        return new_expense_category

    async def update_expense_category(
        self,
        expense_category_data: str,
        update_data: ExpenseCategoryUpdate,
    ) -> ExpenseCategoryTable | None:
        """Обновляет существующую категорию расходов."""
        expense = await self.get_expense_category_by_name(expense_category_data)
        if not expense:
            return None

        update_fields = update_data.model_dump(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(expense, field, value)

        await self.db_session.commit()
        await self.db_session.refresh(expense)

        return expense

    async def delete_expense_category(self, expense_category_name: str) -> None:
        """
        Удаляет категорию расходов по имени.
        """
        category = await self.get_expense_category_by_name(expense_category_name)
        if not category:
            return

        await self.db_session.delete(category)
        await self.db_session.commit()


async def get_expense_category_repository(
    db: AsyncSession = Depends(get_session),
) -> ExpenseCategoryRepository:
    return ExpenseCategoryRepository(db)
