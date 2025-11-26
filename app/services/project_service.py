from typing import Optional, List
from sqlalchemy.exc import IntegrityError

from app.models.project import Project
from app.repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(self, project_repo: ProjectRepository) -> None:
        self._project_repo = project_repo

    def create_project(self, name: str, description: Optional[str]) -> Optional[Project]:
        """Create a new project. Returns None if name is duplicated."""
        try:
            project = self._project_repo.create(name=name, description=description)
            self._project_repo._session.commit()
            self._project_repo._session.refresh(project)
            return project
        except IntegrityError:
            print(f"Error: Project with name '{name}' already exists.")
            self._project_repo._session.rollback()
            return None

    def list_projects(self) -> List[Project]:
        return self._project_repo.list_all()

    def get_project(self, project_id: int) -> Optional[Project]:
        return self._project_repo.get_by_id(project_id)

    def delete_project(self, project_id: int) -> bool:
        ok = self._project_repo.delete(project_id)
        if not ok:
            print("Project not found.")
            return False
        self._project_repo._session.commit()
        return True

    def edit_project(
        self,
        project_id: int,
        new_name: Optional[str],
        new_description: Optional[str],
    ) -> Optional[Project]:
        """Edit an existing project. Returns None on duplicate name or not found."""
        project = self._project_repo.get_by_id(project_id)
        if project is None:
            print("Project not found.")
            return None

        project.name = new_name
        project.description = new_description

        try:
            self._project_repo._session.commit()
            self._project_repo._session.refresh(project)
            return project
        except IntegrityError:
            self._project_repo._session.rollback()
            print(f"Error: Project with name '{new_name}' already exists.")
            return None
