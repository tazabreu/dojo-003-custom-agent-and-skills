from src.domain.entities.task import Task
from src.domain.repositories.task_repository import TaskRepository


class CreateTask:
    def __init__(self, repo: TaskRepository) -> None:
        self._repo = repo

    def execute(self, task: Task) -> Task:
        self._repo.insert(task)
        return task
