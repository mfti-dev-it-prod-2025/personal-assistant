from uuid import UUID
from fastapi import HTTPException, status
from typing import List, Optional
from fastapi import Depends
from personal_assistant.src.repositories.expense import ExpenseRepository, get_expense_repository

from personal_assistant.src.schemas.budget.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate

class ExpenseService:
    def __init__(self, repo: ExpenseRepository):
        self.repo = repo

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ExpenseResponse]:
        expenses = await self.repo.get_all_expenses(skip=skip, limit=limit)
        return [ExpenseResponse.from_orm(e) for e in expenses]

    async def get_by_id(self, id: UUID) -> ExpenseResponse:
        expense = await self.repo.get_expense_by_id(id)
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Расход не найден",
            )
        return ExpenseResponse.from_orm(expense)

    async def get_by_user(self, email: str) -> List[ExpenseResponse]:
        expenses = await self.repo.get_by_user(email)
        return [ExpenseResponse.from_orm(e) for e in expenses]

    async def get_by_category(self, category: str) -> List[ExpenseResponse]:
        expenses = await self.repo.get_expenses_by_category(category)
        return [ExpenseResponse.from_orm(e) for e in expenses]

    async def get_by_date_range(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[ExpenseResponse]:
        expenses = await self.repo.get_expenses_by_date_range(start_date=start_date, end_date=end_date)
        return [ExpenseResponse.from_orm(e) for e in expenses]

    async def add_expense(self, in_data: ExpenseCreate) -> ExpenseResponse:
        new_expense = await self.repo.create_expense(in_data)
        return ExpenseResponse.from_orm(new_expense)

    async def update_expense(self, expense_id: UUID, in_data: ExpenseUpdate) -> ExpenseResponse:
        updated_expense = await self.repo.update_expense(expense_id, in_data)
        if not updated_expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Расход не найден",
            )
        return ExpenseResponse.from_orm(updated_expense)


    async def delete_expense(self, expense_id: UUID) -> None:
        """
        Удаляет расход по ID.
        """
        expense = await self.repo.get_expense_by_id(expense_id)
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Расход не найден",
            )

        await self.repo.delete_expense(expense_id)
async def get_category_service(
    repo: ExpenseRepository = Depends(get_expense_repository),
) -> ExpenseService:
    return ExpenseService(repo)