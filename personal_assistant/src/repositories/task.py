from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from personal_assistant.src.models.todo import Task
from personal_assistant.src.schemas.tasks.schemas import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: UUID, task_data: TaskCreate) -> Task:
        """Создать новую задачу"""
        task = Task(**task_data.model_dump(), user_id=user_id)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_by_id(self, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """Получить задачу по ID (с проверкой владельца)"""
        result = await self.session.execute(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
            self,
            user_id: UUID,
            skip: int = 0,
            limit: int = 100,
            completed: Optional[bool] = None
    ) -> List[Task]:
        """Получить все задачи пользователя с фильтрацией"""
        query = select(Task).where(Task.user_id == user_id)

        if completed is not None:
            query = query.where(Task.is_completed == completed)

        result = await self.session.execute(
            query.order_by(Task.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def update(
            self,
            task_id: UUID,
            user_id: UUID,
            task_data: TaskUpdate
    ) -> Optional[Task]:
        """Обновить задачу"""
        task = await self.get_by_id(task_id, user_id)
        if not task:
            return None

        # Обновляем только переданные поля
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete(self, task_id: UUID, user_id: UUID) -> bool:
        """Удалить задачу"""
        task = await self.get_by_id(task_id, user_id)
        if not task:
            return False

        await self.session.delete(task)
        await self.session.commit()
        return True

    async def mark_completed(
            self,
            task_id: UUID,
            user_id: UUID,
            completed: bool = True
    ) -> Optional[Task]:
        """Отметить задачу как выполненную/невыполненную"""
        task = await self.get_by_id(task_id, user_id)
        if not task:
            return None

        task.is_completed = completed
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def count(self, user_id: UUID, completed: Optional[bool] = None) -> int:
        """Посчитать количество задач пользователя"""
        query = select(func.count()).where(Task.user_id == user_id)

        if completed is not None:
            query = query.where(Task.is_completed == completed)

        result = await self.session.execute(query)
        return result.scalar()