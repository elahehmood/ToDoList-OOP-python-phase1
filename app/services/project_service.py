from typing import List, Optional
from app.repositories.project_repository import ProjectRepository
from app.models.project import Project


class ProjectService:
    """Business logic for projects."""

    def __init__(self, project_repo: ProjectRepository):
        self._project_repo = project_repo

    def create_project(self, name: str, description: Optional[str]) -> Project:
        if not name or not name.strip():
            raise ValueError("Project name cannot be empty")

        return self._project_repo.create(
            name=name.strip(),
            description=description,
        )

    def list_projects(self) -> List[Project]:
        return self._project_repo.list_all()

    def get_project(self, project_id: int) -> Optional[Project]:
        return self._project_repo.get_by_id(project_id)

    def delete_project(self, project_id: int) -> None:
        self._project_repo.delete(project_id)
