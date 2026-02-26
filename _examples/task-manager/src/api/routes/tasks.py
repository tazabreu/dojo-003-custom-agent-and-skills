from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.api.dependencies import (
    get_create_use_case,
    get_delete_use_case,
    get_get_use_case,
    get_list_use_case,
    get_update_use_case,
)
from src.api.schemas.task import TaskCreate, TaskListResponse, TaskResponse, TaskStatusUpdate
from src.application.use_cases.create_task import CreateTask
from src.application.use_cases.delete_task import DeleteTask
from src.application.use_cases.get_task import GetTask, TaskNotFoundError
from src.application.use_cases.list_tasks import ListTasks
from src.application.use_cases.update_task_status import UpdateTaskStatus
from src.domain.entities.task import Task, TaskStatus

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


def _to_response(task: Task) -> TaskResponse:
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status.value,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def create_task(
    body: TaskCreate,
    use_case: CreateTask = Depends(get_create_use_case),
) -> TaskResponse:
    entity = Task(title=body.title, description=body.description)
    created = use_case.execute(entity)
    return _to_response(created)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: UUID,
    use_case: GetTask = Depends(get_get_use_case),
) -> TaskResponse:
    try:
        task = use_case.execute(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return _to_response(task)


@router.get("", response_model=TaskListResponse)
def list_tasks(
    task_status: str | None = Query(default=None, alias="status"),
    use_case: ListTasks = Depends(get_list_use_case),
) -> TaskListResponse:
    status_filter = TaskStatus(task_status) if task_status else None
    tasks = use_case.execute(status_filter)
    return TaskListResponse(count=len(tasks), tasks=[_to_response(t) for t in tasks])


@router.patch("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_task_status(
    task_id: UUID,
    body: TaskStatusUpdate,
    use_case: UpdateTaskStatus = Depends(get_update_use_case),
) -> None:
    try:
        use_case.execute(task_id, TaskStatus(body.status))
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: UUID,
    use_case: DeleteTask = Depends(get_delete_use_case),
) -> None:
    try:
        use_case.execute(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
