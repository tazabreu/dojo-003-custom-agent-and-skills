from uuid import UUID

from cassandra.cluster import Session

from src.domain.entities.task import Task, TaskStatus


class CassandraTaskRepository:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._insert_task = session.prepare(
            "INSERT INTO tasks (id, title, description, status, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?)"
        )
        self._insert_by_status = session.prepare(
            "INSERT INTO tasks_by_status (status, created_at, id, title) "
            "VALUES (?, ?, ?, ?)"
        )
        self._select_by_id = session.prepare(
            "SELECT id, title, description, status, created_at, updated_at "
            "FROM tasks WHERE id = ?"
        )
        self._select_by_status = session.prepare(
            "SELECT status, created_at, id, title "
            "FROM tasks_by_status WHERE status = ?"
        )
        self._delete_task = session.prepare("DELETE FROM tasks WHERE id = ?")
        self._delete_by_status = session.prepare(
            "DELETE FROM tasks_by_status WHERE status = ? AND created_at = ? AND id = ?"
        )
        self._update_task = session.prepare(
            "UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?"
        )

    def insert(self, task: Task) -> None:
        self._session.execute(
            self._insert_task,
            (task.id, task.title, task.description, task.status.value,
             task.created_at, task.updated_at),
        )
        self._session.execute(
            self._insert_by_status,
            (task.status.value, task.created_at, task.id, task.title),
        )

    def get_by_id(self, task_id: UUID) -> Task | None:
        row = self._session.execute(self._select_by_id, (task_id,)).one()
        if row is None:
            return None
        return Task(
            id=row.id,
            title=row.title,
            description=row.description,
            status=TaskStatus(row.status),
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def list_by_status(self, status: TaskStatus) -> list[Task]:
        rows = self._session.execute(self._select_by_status, (status.value,))
        tasks: list[Task] = []
        for row in rows:
            # Fetch full data from main table
            full = self.get_by_id(row.id)
            if full is not None:
                tasks.append(full)
        return tasks

    def update(self, task: Task) -> None:
        # Retrieve old record to remove old status index entry
        old = self._session.execute(self._select_by_id, (task.id,)).one()
        if old and old.status != task.status.value:
            self._session.execute(
                self._delete_by_status,
                (old.status, old.created_at, task.id),
            )
            self._session.execute(
                self._insert_by_status,
                (task.status.value, task.created_at, task.id, task.title),
            )
        self._session.execute(
            self._update_task,
            (task.status.value, task.updated_at, task.id),
        )

    def delete(self, task_id: UUID) -> None:
        old = self._session.execute(self._select_by_id, (task_id,)).one()
        if old:
            self._session.execute(
                self._delete_by_status,
                (old.status, old.created_at, task_id),
            )
        self._session.execute(self._delete_task, (task_id,))
