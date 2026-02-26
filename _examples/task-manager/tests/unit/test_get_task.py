from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.application.use_cases.get_task import GetTask, TaskNotFoundError
from src.domain.entities.task import Task


class TestGetTask:
    def test_returns_task_when_found(self):
        task = Task(title="Found me")
        repo = MagicMock()
        repo.get_by_id.return_value = task
        result = GetTask(repo).execute(task.id)
        assert result == task

    def test_raises_when_not_found(self):
        repo = MagicMock()
        repo.get_by_id.return_value = None
        with pytest.raises(TaskNotFoundError):
            GetTask(repo).execute(uuid4())
