from functools import lru_cache

from cassandra.cluster import Session

from src.application.use_cases.create_task import CreateTask
from src.application.use_cases.delete_task import DeleteTask
from src.application.use_cases.get_task import GetTask
from src.application.use_cases.list_tasks import ListTasks
from src.application.use_cases.update_task_status import UpdateTaskStatus
from src.infrastructure.cassandra.repositories.cassandra_task_repository import (
    CassandraTaskRepository,
)
from src.infrastructure.cassandra.session import create_session


@lru_cache
def get_cassandra_session() -> Session:
    return create_session()


def get_task_repo() -> CassandraTaskRepository:
    return CassandraTaskRepository(get_cassandra_session())


def get_create_use_case() -> CreateTask:
    return CreateTask(get_task_repo())


def get_get_use_case() -> GetTask:
    return GetTask(get_task_repo())


def get_list_use_case() -> ListTasks:
    return ListTasks(get_task_repo())


def get_update_use_case() -> UpdateTaskStatus:
    return UpdateTaskStatus(get_task_repo())


def get_delete_use_case() -> DeleteTask:
    return DeleteTask(get_task_repo())
