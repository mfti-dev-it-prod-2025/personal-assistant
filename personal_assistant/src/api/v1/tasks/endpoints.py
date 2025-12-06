from typing import Optional
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
)
from personal_assistant.src.services.tasks.service import TaskService

router = APIRouter(tags=["tasks"])  # Убрал prefix="/tasks"


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    session: DbSessionDepends,
    current_user: UserTable = Security(get_current_user_dependency, scopes=["tasks:write"]),
):
    service = TaskService(session)
    return await service.create_task(current_user.id, task_data)


@router.get("/", response_model=TaskListResponse)
async def get_tasks(
    session: DbSessionDepends,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    completed: Optional[bool] = None,
    current_user: UserTable = Security(get_current_user_dependency, scopes=["tasks:read"]),
):
    service = TaskService(session)
    return await service.get_all_tasks(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        completed=completed,
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    session: DbSessionDepends,
    current_user: UserTable = Security(get_current_user_dependency, scopes=["tasks:read"]),
):
    service = TaskService(session)
    task = await service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    session: DbSessionDepends,
    current_user: UserTable = Security(get_current_user_dependency, scopes=["tasks:write"]),
):
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
    current_user: UserTable = Security(get_current_user_dependency, scopes=["tasks:write"]),
):
    service = TaskService(session)
    deleted = await service.delete_task(task_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )


@router.post("/{task_id}/complete", response_model=TaskResponse)
async def mark_task_completed(
    task_id: UUID,
    session: DbSessionDepends,
    current_user: UserTable = Security(get_current_user_dependency, scopes=["tasks:write"]),
):
    service = TaskService(session)
    task = await service.mark_task_completed(task_id, current_user.id, completed=True)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.post("/{task_id}/uncomplete", response_model=TaskResponse)
async def mark_task_uncompleted(
    task_id: UUID,
    session: DbSessionDepends,
    current_user: UserTable = Security(get_current_user_dependency, scopes=["tasks:write"]),
):
    service = TaskService(session)
    task = await service.mark_task_completed(task_id, current_user.id, completed=False)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.get("/stats/me")
async def get_my_tasks_stats(
    session: DbSessionDepends,
    current_user: UserTable = Security(get_current_user_dependency, scopes=["tasks:read"]),
):
    service = TaskService(session)
    return await service.get_tasks_stats(current_user.id)