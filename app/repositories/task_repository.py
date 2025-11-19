from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.task import Task


class TaskRepository(ABC):
    """Interface for task persistence layer."""

    @abstractmethod
    def create(self, **kwargs) -> Task: ...
    
    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]: ...
    
    @abstractmethod
    def list_by_project(self, project_id: int) -> List[Task]: ...
    
    @abstractmethod
    def get_overdue_not_done(self, today: date) -> List[Task]: ...


class SqlAlchemyTaskRepository(TaskRepository):
    """SQLAlchemy implementation of TaskRepository."""

    def __init__(self, session: Session) -> None:
        # constructor injection 
        self._session = session

    def create(self, **kwargs) -> Task:
        task = Task(**kwargs)
        self._session.add(task)
        self._session.commit()
        self._session.refresh(task)
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self._session.get(Task, task_id)

    def list_by_project(self, project_id: int) -> List[Task]:
        return (
            self._session.query(Task)
            .filter(Task.project_id == project_id)
            .all()
        )

    def get_overdue_not_done(self, today: date) -> List[Task]:
        return (
            self._session.query(Task)
            .filter(Task.deadline < today, Task.status != "done")
            .all()
        )
