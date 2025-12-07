from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status, Query

from personal_assistant.src.schemas.budget.expense import (
    ExpenseResponse,
    ExpenseCreate,
    ExpenseUpdate,
)
from personal_assistant.src.services.budget.expense import ExpenseService, get_expense_service

expense_router = APIRouter()

# ------------------ GET ------------------

@expense_router.get(
    "/",
    response_model=List[ExpenseResponse],
    summary="Получить все расходы",
)
async def get_all_expenses(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    service: ExpenseService = Depends(get_expense_service),
):
    """
    Получить список всех расходов
    """
    expenses = await service.get_all(skip=skip, limit=limit)  # передаем skip и limit
    return expenses

@expense_router.get(
    "/{expense_id}",
    response_model=ExpenseResponse,
    summary="Получить расход по ID",
)
async def get_expense_by_id(
    expense_id: UUID,
    service: ExpenseService = Depends(get_expense_service),
):
    """
    Получить расход по идентификатору
    """
    expense = await service.get_by_id(expense_id)
    return expense

@expense_router.get(
    "/by-user/{email}",
    response_model=List[ExpenseResponse],
    summary="Получить расходы по пользователю",
)
async def get_expenses_by_user(
    email: str,
    service: ExpenseService = Depends(get_expense_service),
):
    """
    Получить список расходов по email пользователя
    """
    expenses = await service.get_by_user(email)
    return expenses

@expense_router.get(
    "/by-category/{category_name}",
    response_model=List[ExpenseResponse],
    summary="Получить расходы по категории",
)
async def get_expenses_by_category(
    category_name: str,
    service: ExpenseService = Depends(get_expense_service),
):
    """
    Получить список расходов по названию категории
    """
    expenses = await service.get_by_category(category_name)
    return expenses

@expense_router.get(
    "/by-date/",
    response_model=List[ExpenseResponse],
    summary="Получить расходы за диапазон дат",
)
async def get_expenses_by_date_range(
    start_date: Optional[str] = Query(None, description="Начальная дата в формате YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="Конечная дата в формате YYYY-MM-DD"),
    service: ExpenseService = Depends(get_expense_service),
):
    """
    Получить список расходов за указанный диапазон дат
    """
    expenses = await service.get_by_date_range(start_date=start_date, end_date=end_date)
    return expenses

# ------------------ POST ------------------

@expense_router.post(
    "/",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать расход",
)
async def create_expense(
    expense_data: ExpenseCreate,
    service: ExpenseService = Depends(get_expense_service),
):
    """
    Создать новый расход
    """
    new_expense = await service.add_expense(expense_data)
    return new_expense

# ------------------ PUT ------------------

@expense_router.put(
    "/{expense_id}",
    response_model=ExpenseResponse,
    summary="Обновить расход",
)
async def update_expense(
    expense_id: UUID,
    update_data: ExpenseUpdate,
    service: ExpenseService = Depends(get_expense_service),
):
    """
    Обновить существующий расход
    """
    updated_expense = await service.update_expense(expense_id, update_data)
    return updated_expense

# ------------------ DELETE ------------------

@expense_router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить расход",
)
async def delete_expense(
    expense_id: UUID,
    service: ExpenseService = Depends(get_expense_service),
):
    """
    Удалить расход
    """
    await service.delete_expense(expense_id)