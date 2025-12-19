from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Security, Depends
from fastapi import status, HTTPException

from personal_assistant.src.api.dependencies import (
    get_current_user_dependency,
)
from personal_assistant.src.api.v1.expense.expense_category import (
    expense_category_router,
)
from personal_assistant.src.models import UserTable
from personal_assistant.src.schemas.expense import (
    ExpenseResponse,
    ExpenseCreate,
    ExpenseUpdate, ExpensesParams, ExpenseParams,
)
from personal_assistant.src.services.expense import (
    ExpenseService,
    get_expense_service,
)

expense_router = APIRouter()

expense_router.include_router(router=expense_category_router, prefix="/category")

expense_service_dep = Annotated[ExpenseService, Depends(get_expense_service)]


@expense_router.get(
    "",
    summary="Получить расход",
)
async def get_expense(
    params: Annotated[ExpenseParams, Depends()],
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["expenses:read"])
    ],
    service: expense_service_dep,
) -> ExpenseResponse:
    """Получить расход по id или name"""
    if params.id is not None:
        return await service.get_by_id(params.id, current_user.id)

    if params.name is not None:
        return await service.get_by_name(params.name, current_user.id)

    raise HTTPException(status_code=400, detail="Необходимо указать 'id' либо 'name'.")


@expense_router.get(
    "/all",
    summary="Получить расходы по параметрам (если не указаны - будут выведены все)",
)
async def get_expenses(
    params: Annotated[ExpensesParams, Depends()],
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["expenses:read"])
    ],
    service: expense_service_dep,
) -> list[ExpenseResponse]:
    """
    Получить список расходов с фильтрами (одновременно работает только 1 фильтр):
    - category_name
    - start_date, end_date
    - если параметры не указаны — вернуть все расходы.
    """
    user_id = current_user.id

    if params.category_name:
        return await service.get_by_category(params.category_name, user_id)

    if params.start_date or params.end_date:
        return await service.get_by_date_range(
            start_date=params.start_date,
            end_date=params.end_date,
            user_id=user_id,
        )

    return await service.get_all(user_id=user_id)


@expense_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Создать расход",
)
async def create_expense(
    expense_data: ExpenseCreate,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["expenses:create"])
    ],
    service: expense_service_dep,
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
        UserTable, Security(get_current_user_dependency, scopes=["expenses:update"])
    ],
    service: expense_service_dep,
) -> ExpenseResponse:
    """Обновить существующий расход"""

    updated_expense = await service.update_expense(
        expense_id, update_data, current_user.id
    )
    return updated_expense


@expense_router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить расход",
)
async def delete_expense(
    expense_id: UUID,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["expenses:delete"])
    ],
    service: expense_service_dep,
):
    """Удалить расход"""

    await service.delete_expense(expense_id, current_user.id)
