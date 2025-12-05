from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from phase3_api.api.controller_schemas.requests.project_request_schema import (
    ProjectCreateRequest,
    ProjectUpdateRequest,
)
from phase3_api.api.controller_schemas.responses.project_response_schema import (
    ProjectResponse,
)
from phase3_api.db.session import SessionLocal
from phase3_api.repositories.project_repository import SqlAlchemyProjectRepository
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


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    """
    FastAPI dependency that builds a ProjectService with a SQLAlchemy repository.
    """
    repo = SqlAlchemyProjectRepository(session=db)
    return ProjectService(project_repo=repo)


@router.get("/", response_model=List[ProjectResponse])
def list_projects(service: ProjectService = Depends(get_project_service)):
    """
    List all projects.
    """
    projects = service.list_projects()
    return projects


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    payload: ProjectCreateRequest,
    service: ProjectService = Depends(get_project_service),
):
    """
    Create a new project using the same business rules as in Phase 2.
    """
    project = service.create_project(
        name=payload.name,
        description=payload.description,
    )

    if project is None:
        # Service uses prints for error reporting; here we expose a generic 400.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project could not be created due to validation rules.",
        )

    return project


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service),
):
    """
    Retrieve a single project by its ID.
    """
    project = service.get_project(project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )
    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    payload: ProjectUpdateRequest,
    service: ProjectService = Depends(get_project_service),
):
    """
    Partially update an existing project.
    Only non-null fields from the payload will be considered.
    """
    project = service.edit_project(
        project_id=project_id,
        new_name=payload.name,
        new_description=payload.description,
    )

    if project is None:
        # Service prints the exact reason; here we map it to a generic 400/404.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project could not be updated (not found or validation failed).",
        )

    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service),
):
    """
    Delete a project by ID.
    """
    success = service.delete_project(project_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )
    # 204 responses do not return a body
    return None
