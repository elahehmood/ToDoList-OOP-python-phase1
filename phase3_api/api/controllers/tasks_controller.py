from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
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
from phase3_api.services.task_service import TaskService

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
    repo = SqlAlchemyTaskRepository(session=db)
    return TaskService(task_repo=repo)


@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    project_id: int | None = Query(
        default=None,
        description="Project ID whose tasks should be listed. Required.",
    ),
    service: TaskService = Depends(get_task_service),
):
    """
    List tasks for a given project.

    For now, a project_id is required, because the underlying repository
    only supports listing tasks per project.
    """
    if project_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query parameter 'project_id' is required.",
        )

    tasks = service.list_tasks_for_project(project_id=project_id)
    return tasks


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    payload: TaskCreateRequest,
    service: TaskService = Depends(get_task_service),
):
    """
    Create a new task inside a given project.
    """
    task = service.create_task_for_project(
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
    service: TaskService = Depends(get_task_service),
):
    """
    Retrieve a single task by its ID.
    """
    task = service.get_task(task_id)
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
    service: TaskService = Depends(get_task_service),
):
    """
    Partially update an existing task.
    All fields in the payload are optional; only provided fields will be updated.
    """
    task = service.edit_task(
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
    service: TaskService = Depends(get_task_service),
):
    """
    Delete a task by ID.
    """
    success = service.delete_task(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )
    return None
