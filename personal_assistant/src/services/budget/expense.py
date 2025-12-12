from uuid import UUID
from fastapi import HTTPException, status
from typing import List, Optional
from fastapi import Depends
from personal_assistant.src.repositories.expense import (
    ExpenseRepository,
    get_expense_repository,
)
from personal_assistant.src.schemas.budget.expense import ExpenseCreate, ExpenseUpdate
from personal_assistant.src.models.budget import ExpenseTable


class ExpenseService:
    def __init__(self, repo: ExpenseRepository):
        self.repo = repo


    async def get_all(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[ExpenseTable]:
        expenses = await self.repo.get_all_expenses(user_id=user_id, skip=skip, limit=limit)
        return expenses


    async def get_by_id(self, id: UUID, user_id: UUID) -> ExpenseTable:
        expense = await self.repo.get_expense_by_id(id, user_id=user_id)
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Расход не найден или не принадлежит текущему пользователю",
            )
        return expense


    async def get_by_name(self, name: str, user_id: UUID) -> ExpenseTable:
        expense = await self.repo.get_expense_by_name(name, user_id=user_id)
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Расход не найден или не принадлежит текущему пользователю",
            )
        return expense


    async def get_by_category(self, category: str, user_id: UUID) -> List[ExpenseTable]:
        expenses = await self.repo.get_expenses_by_category(category, user_id=user_id)
        return expenses


    async def get_by_date_range(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None, user_id: UUID = None
    ) -> List[ExpenseTable]:
        expenses = await self.repo.get_expenses_by_date_range(
            start_date=start_date, end_date=end_date, user_id=user_id
        )
        return expenses


    async def add_expense(self, in_data: ExpenseCreate, current_user) -> ExpenseTable:
        new_expense = await self.repo.create_expense(in_data, current_user.id)
        return new_expense


    async def update_expense(
        self, expense_id: UUID, in_data: ExpenseUpdate, user_id: UUID
    ) -> ExpenseTable:
        updated_expense = await self.repo.update_expense(expense_id, in_data, user_id=user_id)
        if not updated_expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Расход не найден или не принадлежит текущему пользователю",
            )
        return updated_expense

    async def delete_expense(self, expense_id: UUID, user_id: UUID) -> None:
        """
        Удаляет расход по ID, только если принадлежит текущему пользователю
        """
        expense = await self.repo.get_expense_by_id(expense_id, user_id=user_id)
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Расход не найден или не принадлежит текущему пользователю",
            )

        await self.repo.delete_expense(expense_id, user_id=user_id)


async def get_expense_service(
    repo: ExpenseRepository = Depends(get_expense_repository),
) -> ExpenseService:
    return ExpenseService(repo)