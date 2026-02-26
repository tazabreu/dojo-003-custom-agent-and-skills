from uuid import uuid4

from src.domain.entities.task import Task, TaskStatus


class TestTaskEntity:
    def test_defaults(self):
        task = Task(title="Test")
        assert task.title == "Test"
        assert task.description == ""
        assert task.status == TaskStatus.TODO
        assert task.id is not None
        assert task.created_at is not None

    def test_with_status_returns_new_instance(self):
        task = Task(title="Test")
        updated = task.with_status(TaskStatus.DONE)
        assert updated.status == TaskStatus.DONE
        assert updated.id == task.id
        assert updated.title == task.title
        assert task.status == TaskStatus.TODO  # original unchanged

    def test_frozen(self):
        task = Task(title="Test")
        try:
            task.title = "Changed"  # type: ignore[misc]
            assert False, "Should not allow mutation"
        except AttributeError:
            pass
