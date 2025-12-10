from fastapi import Depends

from personal_assistant.src.repositories.expense_category import ExpenseCategoryRepository, get_expense_category_repository
from personal_assistant.src.schemas.budget.expense_category import (
    ExpenseCategoryCreate,
    ExpenseCategoryResponse,
    ExpenseCategoryUpdate,
)
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status


class ExpenseCategoryService:
    def __init__(self, repo: ExpenseCategoryRepository):
        self.repo = repo

    async def get_all(self, skip: int, limit: int) -> list[ExpenseCategoryResponse]:
        res = await self.repo.get_all_categories(skip=skip, limit=limit)

        return res

    async def get_by_name(self, name) -> ExpenseCategoryResponse:
        res = await self.repo.get_expense_category_by_name(name)

        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория с таким именем не существует",
            )

        return res

    async def get_by_id(self, id) -> ExpenseCategoryResponse:
        res = await self.repo.get_expense_category_by_id(id)

        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория с таким id не существует",
            )

        return res

    async def add_category(self, in_data: ExpenseCategoryCreate) -> ExpenseCategoryResponse:
        try:
            new_category = await self.repo.create_expense_category(in_data)
        except IntegrityError:
            await self.repo.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Категория с таким именем уже существует",
            )
        except Exception as exc:
            await self.repo.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при создании категории: {exc}",
            )
        return new_category

    async def update(self, name: str, in_data: ExpenseCategoryUpdate) -> ExpenseCategoryResponse:
        existing_category = await self.repo.get_expense_category_by_name(name)
        if not existing_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория с таким именем не существует",
            )


        res = await self.repo.update_expense_category(name, in_data)
        return res

    async def delete(self, name: str) -> None:
        existing_category = await self.repo.get_expense_category_by_name(name)
        if not existing_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория с таким именем не существует",
            )

        await self.repo.delete_expense_category(name)

async def get_category_service(
    repo: ExpenseCategoryRepository = Depends(get_expense_category_repository),
) -> ExpenseCategoryService:
    return ExpenseCategoryService(repo)