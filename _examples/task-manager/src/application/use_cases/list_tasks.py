from src.domain.entities.task import Task, TaskStatus
from src.domain.repositories.task_repository import TaskRepository


class ListTasks:
    def __init__(self, repo: TaskRepository) -> None:
        self._repo = repo

    def execute(self, status: TaskStatus | None = None) -> list[Task]:
        if status is not None:
            return self._repo.list_by_status(status)
        # Collect all statuses when no filter is given
        results: list[Task] = []
        for s in TaskStatus:
            results.extend(self._repo.list_by_status(s))
        results.sort(key=lambda t: t.created_at, reverse=True)
        return results
