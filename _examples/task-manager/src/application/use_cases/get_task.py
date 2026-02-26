from uuid import UUID

from src.domain.entities.task import Task
from src.domain.repositories.task_repository import TaskRepository


class TaskNotFoundError(Exception):
    def __init__(self, task_id: UUID) -> None:
        super().__init__(f"Task not found: {task_id}")
        self.task_id = task_id


class GetTask:
    def __init__(self, repo: TaskRepository) -> None:
        self._repo = repo

    def execute(self, task_id: UUID) -> Task:
        task = self._repo.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task
