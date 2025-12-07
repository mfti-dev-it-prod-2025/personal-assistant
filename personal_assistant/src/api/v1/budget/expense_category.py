from typing import List
from fastapi import APIRouter, Depends, status, Query


from personal_assistant.src.schemas.budget.expense_category import (
    ExpenseCategoryResponse,
    ExpenseCategoryCreate,
    ExpenseCategoryUpdate,
)
from personal_assistant.src.services.budget.expense_category import ExpenseCategoryService, get_category_service


expense_category_router = APIRouter()

@expense_category_router.get(
    "/",
    response_model=List[ExpenseCategoryResponse],
    summary="Получить все категории",
)
async def get_all_categories(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    service: ExpenseCategoryService = Depends(get_category_service),
):
    """
    Получить список всех категорий
    """
    expense_categories = await service.get_all(skip=skip, limit=limit)
    return expense_categories

@expense_category_router.post(
    "/",
    response_model=ExpenseCategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать категорию",
)
async def create_category(
    category_data: ExpenseCategoryCreate,
    service: ExpenseCategoryService = Depends(get_category_service),
):
    """
    Создать новую категорию
    """

    res = await service.add_category(category_data)
    return res

@expense_category_router.get(
    "/{category_name}",
    response_model=ExpenseCategoryResponse,
    summary="Получить категорию по названию",
)
async def get_category(
    category_name: str, service: ExpenseCategoryService = Depends(get_category_service)
):
    """
    Получить категорию по названию
    """
    category = await service.get_by_name(category_name)

    return category


@expense_category_router.put(
    "/{category_name}",
    response_model=ExpenseCategoryResponse,
    summary="Обновить категорию",
)
async def update_category(
    category_name: str,
    update_data: ExpenseCategoryUpdate,
    service: ExpenseCategoryService = Depends(get_category_service),
):
    """
    Обновить данные категории
    """

    category = await service.update(category_name, update_data)

    return category

@expense_category_router.delete(
    "/{category_name}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить категорию",
)
async def delete_category(
    category_name: str, service: ExpenseCategoryService = Depends(get_category_service)
):
    """
    Удалить категорию
    """
    await service.delete(category_name)
