from __future__ import annotations

import os
from typing import List, Optional

from app.models.project import Project
from app.repositories.project_repository import SqlAlchemyProjectRepository


# Defaults match phase 1 .env semantics
MAX_PROJECTS = int(os.getenv("MAX_PROJECTS", "10"))


class ProjectService:
    """Service layer for project-related operations."""

    def __init__(self, project_repo: SqlAlchemyProjectRepository) -> None:
        self._project_repo = project_repo

    # ---------- CRUD ----------

    def create_project(self, name: str, description: Optional[str]) -> Optional[Project]:
        """
        Create a new project with phase-1 constraints:

        - name is required, non-empty
        - max number of projects: MAX_PROJECTS
        - name length <= 30
        - description length <= 150
        - name must be unique
        """
        name = (name or "").strip()
        description = (description or "").strip()

        if not name:
            print("Error: Project name cannot be empty.")
            return None

        # Limit on number of projects
        all_projects = self._project_repo.list_all()
        if len(all_projects) >= MAX_PROJECTS:
            print(f"Error: You have reached the maximum limit of {MAX_PROJECTS} projects.")
            return None

        # Length constraints
        if len(name) > 30:
            print("Error: Project name exceeds 30 characters.")
            return None

        if len(description) > 150:
            print("Error: Project description exceeds 150 characters.")
            return None

        # Unique name
        for p in all_projects:
            if p.name == name:
                print("Error: A project with this name already exists.")
                return None

        project = self._project_repo.create(name=name, description=description or None)
        # SqlAlchemyProjectRepository.create already commits + refreshes
        return project

    def get_project(self, project_id: int) -> Optional[Project]:
        """Return a single project by ID."""
        return self._project_repo.get_by_id(project_id)

    def list_projects(self) -> List[Project]:
        """
        List all projects, sorted by creation time if available,
        otherwise by ID.
        """
        projects = self._project_repo.list_all()
        return sorted(
            projects,
            key=lambda p: getattr(p, "created_at", p.id),
        )

    def delete_project(self, project_id: int) -> bool:
        """
        Delete a project by ID.

        Prints an error if project not found.
        """
        project = self.get_project(project_id)
        if project is None:
            print(f"Error: Project with ID '{project_id}' not found.")
            return False

        self._project_repo.delete(project_id)
        # repository handles commit
        return True

    def edit_project(
        self,
        project_id: int,
        new_name: Optional[str],
        new_description: Optional[str],
    ) -> Optional[Project]:
        """
        Edit an existing project (phase-1 rules):

        - Non-empty new_name / new_description only
        - new_name length <= 30
        - new_description length <= 150
        - new_name unique among other projects
        - If nothing changes, prints info.
        """
        project = self.get_project(project_id)
        if project is None:
            print(f"Error: Project with ID '{project_id}' not found.")
            return None

        name_input = (new_name or "").strip()
        desc_input = (new_description or "").strip()

        updated = False

        # --- Update name ---
        if name_input and name_input != project.name:
            if len(name_input) > 30:
                print("Error: New project name exceeds 30 characters.")
                return None

            all_projects = self._project_repo.list_all()
            for other in all_projects:
                if other.id != project.id and other.name == name_input:
                    print("Error: A project with this new name already exists.")
                    return None

            project.name = name_input
            updated = True

        # --- Update description ---
        if desc_input and desc_input != (project.description or ""):
            if len(desc_input) > 150:
                print("Error: New project description exceeds 150 characters.")
                return None

            project.description = desc_input
            updated = True

        if not updated:
            print("Info: No changes were made.")
            return project

        # Persist to DB
        self._project_repo._session.commit()
        self._project_repo._session.refresh(project)
        print(f"Project '{project.name}' updated successfully.")
        return project
