
from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from phase3_api.models.project import Project


class ProjectRepository(ABC):
    """Interface for project persistence layer."""

    @abstractmethod
    def create(self, name: str, description: str | None) -> Project: ...

    @abstractmethod
    def get_by_id(self, project_id: int) -> Optional[Project]: ...

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Project]: ...

    @abstractmethod
    def list_all(self) -> List[Project]: ...

    @abstractmethod
    def delete(self, project_id: int) -> None: ...


class SqlAlchemyProjectRepository(ProjectRepository):
    """SQLAlchemy implementation of ProjectRepository."""

    def __init__(self, session: Session) -> None:
        # constructor injection
        self._session = session

    def create(self, name: str, description: str | None) -> Project:
        project = Project(name=name, description=description)
        try:
            self._session.add(project)
            self._session.commit()
            self._session.refresh(project)
            return project
        except IntegrityError:
            # VERY IMPORTANT: rollback so the Session is usable again
            self._session.rollback()
            # re‑raise so upper layers can show a friendly message
            raise

    def get_by_id(self, project_id: int) -> Optional[Project]:
        return self._session.get(Project, project_id)

    def get_by_name(self, name: str) -> Optional[Project]:
        stmt = select(Project).where(Project.name == name)
        return self._session.execute(stmt).scalar_one_or_none()

    def list_all(self) -> List[Project]:
        return self._session.query(Project).all()

    def delete(self, project_id: int) -> None:
        project = self.get_by_id(project_id)
        if project is not None:
            self._session.delete(project)
            self._session.commit()

