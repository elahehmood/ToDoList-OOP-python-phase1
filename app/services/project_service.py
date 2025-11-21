from typing import List, Optional

from app.models.project import Project
from app.repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(self, project_repo: ProjectRepository) -> None:
        self._project_repo = project_repo

    def create_project(self, name: str, description: Optional[str]) -> Project:
        name = (name or "").strip()
        if not name:
            raise ValueError("Project name cannot be empty.")

        if description is not None:
            description = description.strip()
            if description == "":
                description = None

        return self._project_repo.create(name, description)

    def list_projects(self) -> List[Project]:
        return self._project_repo.list_all()

    def get_project(self, project_id: int) -> Optional[Project]:
        return self._project_repo.get_by_id(project_id)

    def delete_project(self, project_id: int) -> bool:
        return self._project_repo.delete(project_id)
