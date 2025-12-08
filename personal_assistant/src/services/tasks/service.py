from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from personal_assistant.src.repositories.task import TaskRepository
from personal_assistant.src.schemas.tasks.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
    TasksStats,
)
from personal_assistant.src.models.todo import Task


class TaskService:
    def __init__(self, session: AsyncSession):
        self.repository = TaskRepository(session)

    async def create_task(self, user_id: UUID, task_data: TaskCreate) -> TaskResponse:
        task = await self.repository.create(user_id, task_data)
        return TaskResponse.model_validate(task)

    async def get_task(self, task_id: UUID, user_id: UUID) -> Optional[TaskResponse]:
        task = await self.repository.get_by_id(task_id, user_id)
        if task:
            return TaskResponse.model_validate(task)
        return None

    async def get_all_tasks(
            self,
            user_id: UUID,
            skip: int = 0,
            limit: int = 100,
            completed: Optional[bool] = None
    ) -> TaskListResponse:
        tasks = await self.repository.get_all(user_id, skip, limit, completed)
        total = await self.repository.count(user_id, completed)

        return TaskListResponse(
            tasks=[TaskResponse.model_validate(task) for task in tasks],
            total=total
        )

    async def update_task(
            self,
            task_id: UUID,
            user_id: UUID,
            task_data: TaskUpdate
    ) -> Optional[TaskResponse]:
        task = await self.repository.update(task_id, user_id, task_data)
        if task:
            return TaskResponse.model_validate(task)
        return None

    async def delete_task(self, task_id: UUID, user_id: UUID) -> bool:
        return await self.repository.delete(task_id, user_id)

    async def mark_task_completed(
            self,
            task_id: UUID,
            user_id: UUID,
            completed: bool = True
    ) -> Optional[TaskResponse]:
        task = await self.repository.mark_completed(task_id, user_id, completed)
        if task:
            return TaskResponse.model_validate(task)
        return None

    async def get_completed_tasks(self, user_id: UUID) -> TaskListResponse:
        tasks = await self.repository.get_all(user_id, completed=True)
        total = await self.repository.count(user_id, completed=True)

        return TaskListResponse(
            tasks=[TaskResponse.model_validate(task) for task in tasks],
            total=total
        )

    async def get_pending_tasks(self, user_id: UUID) -> TaskListResponse:
        tasks = await self.repository.get_all(user_id, completed=False)
        total = await self.repository.count(user_id, completed=False)

        return TaskListResponse(
            tasks=[TaskResponse.model_validate(task) for task in tasks],
            total=total
        )

    async def get_tasks_stats(self, user_id: UUID) -> TasksStats:
        total_tasks = await self.repository.count(user_id)
        completed_tasks = await self.repository.count(user_id, completed=True)
        pending_tasks = await self.repository.count(user_id, completed=False)

        return TasksStats(
            total=total_tasks,
            completed=completed_tasks,
            pending=pending_tasks,
            completion_rate=(
                completed_tasks / total_tasks if total_tasks > 0 else 0
            )
        )