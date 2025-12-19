from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from personal_assistant.src.repositories.expense_category import (
    ExpenseCategoryRepository,
    get_expense_category_repository,
)
from personal_assistant.src.schemas.expense_category import (
    ExpenseCategoryCreate,
    ExpenseCategoryResponse,
    ExpenseCategoryUpdate,
)


class ExpenseCategoryService:
    def __init__(self, repo: ExpenseCategoryRepository):
        self.repo = repo

    async def get_all(
        self, skip: int, limit: int, user_id
    ) -> list[ExpenseCategoryResponse]:
        """
        Получить категории только текущего пользователя
        """
        res = await self.repo.get_all_categories(
            skip=skip,
            limit=limit,
            user_id=user_id,
        )
        return res

    async def get_by_name(self, name, user_id) -> ExpenseCategoryResponse:
        """
        Получить категорию по имени (только свою)
        """
        res = await self.repo.get_expense_category_by_name(
            name,
            user_id=user_id,
        )

        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "Категория с таким именем не существует "
                    "или не принадлежит пользователю"
                ),
            )

        return res

    async def get_by_id(self, id, user_id) -> ExpenseCategoryResponse:
        """
        Получить категорию по ID (только свою)
        """
        res = await self.repo.get_expense_category_by_id(
            id,
            user_id=user_id,
        )

        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "Категория с таким id не существует или не принадлежит пользователю"
                ),
            )

        return res

    async def add_category(
        self, in_data: ExpenseCategoryCreate, user_id
    ) -> ExpenseCategoryResponse:
        """
        Создать категорию для пользователя
        """
        try:
            new_category = await self.repo.create_expense_category(
                in_data,
                user_id=user_id,
            )
        except IntegrityError:
            await self.repo.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Категория с таким именем уже существует",
            )
        return new_category

    async def update(
        self, name: str, in_data: ExpenseCategoryUpdate, user_id
    ) -> ExpenseCategoryResponse:
        """
        Обновить только свою категорию
        """
        existing_category = await self.repo.get_expense_category_by_name(
            name,
            user_id=user_id,
        )
        if not existing_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "Категория с таким именем не существует "
                    "или не принадлежит пользователю"
                ),
            )

        res = await self.repo.update_expense_category(
            name,
            in_data,
            user_id=user_id,
        )
        return res

    async def delete(self, name: str, user_id) -> None:
        """
        Удалить только свою категорию
        """
        existing_category = await self.repo.get_expense_category_by_name(
            name,
            user_id=user_id,
        )
        if not existing_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "Категория с таким именем не существует "
                    "или не принадлежит пользователю"
                ),
            )

        await self.repo.delete_expense_category(name, user_id=user_id)


async def get_category_service(
    repo: Annotated[
        ExpenseCategoryRepository, Depends(get_expense_category_repository)
    ],
) -> ExpenseCategoryService:
    return ExpenseCategoryService(repo)
