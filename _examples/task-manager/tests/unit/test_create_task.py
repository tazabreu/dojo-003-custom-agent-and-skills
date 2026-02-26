from unittest.mock import MagicMock
from uuid import uuid4

from src.application.use_cases.create_task import CreateTask
from src.domain.entities.task import Task


class TestCreateTask:
    def test_creates_and_returns_task(self):
        repo = MagicMock()
        use_case = CreateTask(repo)
        task = Task(title="Write tests")
        result = use_case.execute(task)
        repo.insert.assert_called_once_with(task)
        assert result == task
