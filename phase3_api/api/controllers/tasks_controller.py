from typing import List, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from phase3_api.api.controller_schemas.requests.task_request_schema import (
    TaskCreateRequest,
    TaskUpdateRequest,
)
from phase3_api.api.controller_schemas.responses.task_response_schema import (
    TaskResponse,
)
from phase3_api.db.session import SessionLocal
from phase3_api.repositories.task_repository import SqlAlchemyTaskRepository
from phase3_api.repositories.project_repository import SqlAlchemyProjectRepository
from phase3_api.services.task_service import TaskService
from phase3_api.services.project_service import ProjectService

router = APIRouter()


def get_db() -> Session:
    """
    FastAPI dependency that provides a SQLAlchemy Session.
    The session is created per-request and closed automatically.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    """
    FastAPI dependency that builds a TaskService with a SQLAlchemy repository.
    """
    task_repo = SqlAlchemyTaskRepository(session=db)
    return TaskService(task_repo=task_repo)


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    """
    FastAPI dependency that builds a ProjectService with a SQLAlchemy repository.
    This is used to validate that a project exists before operating on its tasks.
    """
    project_repo = SqlAlchemyProjectRepository(session=db)
    return ProjectService(project_repo=project_repo)


class CloseOverdueResult(BaseModel):
    """
    Response model for closing overdue tasks.
    """
    closed_count: int
    scope: Literal["all", "project"]
    project_id: int | None = None


@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    project_id: int | None = Query(
        default=None,
        description="Project ID whose tasks should be listed. Required.",
    ),
    task_service: TaskService = Depends(get_task_service),
    project_service: ProjectService = Depends(get_project_service),
):
    """
    List tasks for a given project.

    - If the project_id is missing → 400 Bad Request.
    - If the project does not exist → 404 Project not found.
    - If the project exists → return the current list of tasks for that project.

    NOTE:
    This endpoint is a pure read operation (no side effects).
    Closing overdue tasks is handled by a dedicated POST endpoint.
    """
    if project_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query parameter 'project_id' is required.",
        )

    # Check if the project exists first (business rule).
    project = project_service.get_project(project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    # Just list tasks; do not modify any state here.
    tasks = task_service.list_tasks_for_project(project_id=project_id)
    return tasks


@router.post(
    "/close-overdue",
    response_model=CloseOverdueResult,
    status_code=status.HTTP_200_OK,
)
def close_overdue_tasks(
    project_id: int | None = Query(
        default=None,
        description=(
            "If provided, only overdue tasks for this project will be closed. "
            "If omitted, all overdue tasks in the system will be closed."
        ),
    ),
    task_service: TaskService = Depends(get_task_service),
    project_service: ProjectService = Depends(get_project_service),
):
    """
    Close overdue tasks.

    - If project_id is provided:
        * validate that the project exists
        * close overdue tasks only for that project
    - If project_id is omitted:
        * close overdue tasks for all projects

    This is a state-changing operation, so it is exposed as POST,
    keeping GET /tasks as a safe read-only operation.
    """
    # Close overdue tasks for a specific project
    if project_id is not None:
        project = project_service.get_project(project_id)
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found.",
            )

        closed_count = task_service.close_overdue_tasks_for_project(project_id=project_id)
        return CloseOverdueResult(
            closed_count=closed_count,
            scope="project",
            project_id=project_id,
        )

    # Close overdue tasks for all projects
    closed_count = task_service.close_overdue_tasks()
    return CloseOverdueResult(
        closed_count=closed_count,
        scope="all",
        project_id=None,
    )


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    payload: TaskCreateRequest,
    task_service: TaskService = Depends(get_task_service),
    project_service: ProjectService = Depends(get_project_service),
):
    """
    Create a new task inside a given project.

    - If the project does not exist → 404 Project not found.
    - If business rules in the service fail → 400 Bad Request.
    """
    # Ensure project exists before creating a task for it.
    project = project_service.get_project(payload.project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    task = task_service.create_task_for_project(
        project_id=payload.project_id,
        title=payload.title,
        description=payload.description,
        deadline=payload.deadline,
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task could not be created due to validation rules.",
        )

    return task


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
):
    """
    Retrieve a single task by its ID.
    """
    task = task_service.get_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    payload: TaskUpdateRequest,
    task_service: TaskService = Depends(get_task_service),
):
    """
    Partially update an existing task.
    All fields in the payload are optional; only provided fields will be updated.
    """
    task = task_service.edit_task(
        task_id=task_id,
        title=payload.title,
        description=payload.description,
        deadline=payload.deadline,
        status=payload.status,
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task could not be updated (not found or validation failed).",
        )

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
):
    """
    Delete a task by ID.
    """
    success = task_service.delete_task(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )
    return None
