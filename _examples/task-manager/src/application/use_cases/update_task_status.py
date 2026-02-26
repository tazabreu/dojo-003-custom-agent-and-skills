from uuid import UUID

from src.domain.entities.task import TaskStatus
from src.domain.repositories.task_repository import TaskRepository
from src.application.use_cases.get_task import TaskNotFoundError


class UpdateTaskStatus:
    def __init__(self, repo: TaskRepository) -> None:
        self._repo = repo

    def execute(self, task_id: UUID, new_status: TaskStatus) -> None:
        task = self._repo.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        updated = task.with_status(new_status)
        self._repo.update(updated)
