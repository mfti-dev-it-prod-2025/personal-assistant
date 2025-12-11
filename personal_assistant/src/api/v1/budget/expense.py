from uuid import UUID
from fastapi import status, HTTPException

from personal_assistant.src.schemas.budget.expense import (
    ExpenseResponse,
    ExpenseCreate,
    ExpenseUpdate,
)
from personal_assistant.src.services.budget.expense import (
    ExpenseService,
    get_expense_service,
)
from personal_assistant.src.api.v1.budget.params import ExpensesParams, ExpenseParams
from typing import Annotated
from fastapi import APIRouter, Security, Depends
from personal_assistant.src.api.dependencies import (
    get_current_user_dependency,
)
from personal_assistant.src.models import UserTable

expense_router = APIRouter()


@expense_router.get(
    "/",
    summary="Получить расход",
)
async def get_expense(
    params: Annotated[ExpenseParams, Depends()],
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=[])
    ],
    service: ExpenseService = Depends(get_expense_service),
) -> ExpenseResponse:
    """Получить расход по id или name"""
    if params.id is not None:
        return await service.get_by_id(params.id)

    if params.name is not None:
        return await service.get_by_name(params.name)

    raise HTTPException(status_code=400, detail="Необходимо указать 'id' либо 'name'.")


@expense_router.get(
    "/all",
    summary="Получить расходы по параметрам (если параметры не указаны - будут выведены все расходы)",
)
async def get_expenses(
    params: Annotated[ExpensesParams, Depends()],
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=[])
    ],
    service: ExpenseService = Depends(get_expense_service),
) -> list[ExpenseResponse]:
    """
    Получить список расходов с фильтрами (одновременно работает только 1 фильтр):
    - email
    - category_name
    - start_date, end_date
    - если параметры не указаны — вернуть все расходы.
    """

    if params.email:
        return await service.get_by_user(params.email)

    if params.category_name:
        return await service.get_by_category(params.category_name)

    if params.start_date or params.end_date:
        return await service.get_by_date_range(
            start_date=params.start_date,
            end_date=params.end_date,
        )

    return await service.get_all()


@expense_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать расход",
)
async def create_expense(
    expense_data: ExpenseCreate,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=[])
    ],
    service: ExpenseService = Depends(get_expense_service),
) -> ExpenseResponse:
    """Создать новый расход"""
    new_expense = await service.add_expense(expense_data, current_user)
    return new_expense


@expense_router.put(
    "/{expense_id}",
    summary="Обновить расход",
)
async def update_expense(
    expense_id: UUID,
    update_data: ExpenseUpdate,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=[])
    ],
    service: ExpenseService = Depends(get_expense_service),
) -> ExpenseResponse:
    """Обновить существующий расход"""
    updated_expense = await service.update_expense(expense_id, update_data)
    return updated_expense


@expense_router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить расход",
)
async def delete_expense(
    expense_id: UUID,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=[])
    ],
    service: ExpenseService = Depends(get_expense_service),
):
    """Удалить расход"""
    await service.delete_expense(expense_id)
