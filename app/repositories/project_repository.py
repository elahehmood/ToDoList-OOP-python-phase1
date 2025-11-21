from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.project import Project


class ProjectRepository(ABC):
    """Interface for project persistence layer."""

    @abstractmethod
    def create(self, name: str, description: str | None) -> Project: ...
    
    @abstractmethod
    def get_by_id(self, project_id: int) -> Optional[Project]: ...
    
    @abstractmethod
    def list_all(self) -> List[Project]: ...
    
    @abstractmethod
    def delete(self, project_id: int) -> bool: ...


class SqlAlchemyProjectRepository(ProjectRepository):
    """SQLAlchemy implementation of ProjectRepository."""

    def __init__(self, session: Session) -> None:
        # constructor injection 
        self._session = session

    def create(self, name: str, description: str | None) -> Project:
        project = Project(name=name, description=description)
        self._session.add(project)
        try:
            self._session.commit()
        except IntegrityError:
            self._session.rollback()
            raise ValueError("Project name must be unique.")
        self._session.refresh(project)
        return project

    def get_by_id(self, project_id: int) -> Optional[Project]:
        return self._session.get(Project, project_id)

    def list_all(self) -> List[Project]:
        return self._session.query(Project).all()

    def delete(self, project_id: int) -> bool:
        project = self.get_by_id(project_id)
        if project is None:
            return False
        self._session.delete(project)
        self._session.commit()
        return True
