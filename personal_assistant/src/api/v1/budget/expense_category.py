from typing import List
from fastapi import status, Query, HTTPException
from personal_assistant.src.models import UserTable

from personal_assistant.src.schemas.budget.expense_category import (
    ExpenseCategoryResponse,
    ExpenseCategoryCreate,
    ExpenseCategoryUpdate,
)
from personal_assistant.src.services.budget.expense_category import (
    ExpenseCategoryService,
    get_category_service,
)
from personal_assistant.src.api.v1.budget.params import ExpenseCategoryParams
from typing import Annotated
from fastapi import APIRouter, Security, Depends
from personal_assistant.src.api.dependencies import (
    get_current_user_dependency,
)

expense_category_router = APIRouter()

@expense_category_router.get(
    "/all",
    summary="Получить все категории текущего пользователя",  # 🔥 UPDATED
)
async def get_all_categories(
    current_user: Annotated[
            UserTable, Security(get_current_user_dependency, scopes=[])
        ],
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),

    service: ExpenseCategoryService = Depends(get_category_service),
) -> List[ExpenseCategoryResponse]:
    """
    Получить список всех категорий текущего пользователя
    """
    expense_categories = await service.get_all(
        skip=skip,
        limit=limit,
        user_id=current_user.id,
    )
    return expense_categories


@expense_category_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать категорию",
)
async def create_category(
    category_data: ExpenseCategoryCreate,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=[])
    ],
    service: ExpenseCategoryService = Depends(get_category_service),
) -> ExpenseCategoryResponse:
    """
    Создать новую категорию (только для текущего юзера)
    """
    try:
        res = await service.add_category(category_data, user_id=current_user.id)
        return res
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@expense_category_router.get(
    "/",
    summary="Получить категорию",
)
async def get_category(
    params: Annotated[ExpenseCategoryParams, Depends()],
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=[])
    ],
    service: ExpenseCategoryService = Depends(get_category_service),
) -> ExpenseCategoryResponse:
    """
    Получить категорию пользователя по id или name     # 🔥 UPDATED
    """

    # 🔥 UPDATED — добавляем фильтрацию по user_id
    if params.id is not None:
        return await service.get_by_id(params.id, user_id=current_user.id)

    if params.name is not None:
        return await service.get_by_name(params.name, user_id=current_user.id)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Необходимо указать 'id' либо 'name'.",
    )


@expense_category_router.put(
    "/{category_name}",
    summary="Обновить категорию",
)
async def update_category(
    category_name: str,
    update_data: ExpenseCategoryUpdate,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=[])
    ],
    service: ExpenseCategoryService = Depends(get_category_service),
) -> ExpenseCategoryResponse:
    """
    Обновить данные своей категории
    """

    try:
        category = await service.update(
            category_name,
            update_data,
            user_id=current_user.id,
        )
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена.",
            )
        return category
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@expense_category_router.delete(
    "/{category_name}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить категорию",
)
async def delete_category(
    category_name: str,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=[])
    ],
    service: ExpenseCategoryService = Depends(get_category_service),
):
    """
    Удалить свою категорию
    """

    await service.delete(category_name, user_id=current_user.id)