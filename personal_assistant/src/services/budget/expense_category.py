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

        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категории не найдены",
            )

        return res

    async def get_by_name(self, name) -> ExpenseCategoryResponse:
        res = await self.repo.get_expense_category_by_name(name)

        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория с таким именем не существует",
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

        return new_category #ExpenseCategoryResponse.from_orm(new_category)

    async def update(self, name: str, in_data: ExpenseCategoryUpdate) -> ExpenseCategoryResponse:
        existing_category = await self.repo.get_expense_category_by_name(name)
        if not existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Категория с таким именем не существует",
            )

        update_dict = {k: v for k, v in in_data.model_dump().items() if v is not None}

        if update_dict:
            res = await self.repo.update_expense_category(name, update_dict)
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