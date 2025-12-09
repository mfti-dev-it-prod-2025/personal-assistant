from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Query, Security

from personal_assistant.src.api.dependencies import (
    get_current_user_dependency,
    DbSessionDepends,
)
from personal_assistant.src.models import UserTable
from personal_assistant.src.schemas.tasks.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
    TasksStats,
)
from personal_assistant.src.services.tasks.service import TaskService

router = APIRouter(tags=["tasks"])


@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    session: DbSessionDepends,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["tasks:write"])
    ],
) -> TaskResponse:
    service = TaskService(session)
    return await service.create_task(current_user.id, task_data)


@router.get("/")
async def get_tasks(
    session: DbSessionDepends,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["tasks:read"])
    ],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
    completed: Annotated[bool, Query()] = False,
) -> TaskListResponse:
    service = TaskService(session)
    return await service.get_all_tasks(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        completed=completed,
    )


@router.get("/{task_id}")
async def get_task(
    task_id: UUID,
    session: DbSessionDepends,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["tasks:read"])
    ],
) -> TaskResponse:
    service = TaskService(session)
    task = await service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.put("/{task_id}")
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    session: DbSessionDepends,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["tasks:update"])
    ],
) -> TaskResponse:
    service = TaskService(session)
    task = await service.update_task(task_id, current_user.id, task_data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    session: DbSessionDepends,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["tasks:delete"])
    ],
) -> None:
    service = TaskService(session)
    deleted = await service.delete_task(task_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )




@router.get("/stats/me")
async def get_my_tasks_stats(
    session: DbSessionDepends,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["tasks:read"])
    ],
) -> TasksStats:
    service = TaskService(session)
    return await service.get_tasks_stats(current_user.id)