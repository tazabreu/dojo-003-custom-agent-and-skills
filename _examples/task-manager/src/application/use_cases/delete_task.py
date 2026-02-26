from uuid import UUID

from src.domain.repositories.task_repository import TaskRepository
from src.application.use_cases.get_task import TaskNotFoundError


class DeleteTask:
    def __init__(self, repo: TaskRepository) -> None:
        self._repo = repo

    def execute(self, task_id: UUID) -> None:
        task = self._repo.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        self._repo.delete(task_id)
