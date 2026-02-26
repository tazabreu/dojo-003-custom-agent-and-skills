from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4


class TaskStatus(StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


@dataclass(frozen=True)
class Task:
    title: str
    id: UUID = field(default_factory=uuid4)
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def with_status(self, new_status: TaskStatus) -> "Task":
        """Return a copy with updated status and updated_at timestamp."""
        return Task(
            id=self.id,
            title=self.title,
            description=self.description,
            status=new_status,
            created_at=self.created_at,
            updated_at=datetime.now(timezone.utc),
        )
