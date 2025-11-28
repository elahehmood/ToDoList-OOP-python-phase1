from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.task import Task


class TaskRepository(ABC):
    """
    Abstract base repository for tasks.
    """

    @abstractmethod
    def create_for_project(
        self,
        project_id: int,
        title: str,
        description: Optional[str],
        deadline: Optional[date],
        status: str = "todo",
    ) -> Task:
        raise NotImplementedError

    @abstractmethod
    def list_for_project(self, project_id: int) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def find_overdue_open_tasks(self, today: date) -> List[Task]:
        """Return all tasks that have a deadline before 'today' and are not done."""
        raise NotImplementedError
    

class SqlAlchemyTaskRepository(TaskRepository):
    """
    Task repository based on a shared SQLAlchemy Session.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def create_for_project(
        self,
        project_id: int,
        title: str,
        description: Optional[str],
        deadline: Optional[date],
        status: str = "todo",
    ) -> Task:
        task = Task(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline,
            status=status,
        )
        self._session.add(task)
        return task

    def list_for_project(self, project_id: int) -> List[Task]:
        return (
            self._session.query(Task)
            .filter(Task.project_id == project_id)
            .order_by(Task.id)
            .all()
        )

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self._session.query(Task).filter(Task.id == task_id).first()

    def delete(self, task_id: int) -> bool:
        task = self.get_by_id(task_id)
        if not task:
            return False
        self._session.delete(task)
        return True
    def find_overdue_open_tasks(self, today: date) -> List[Task]:
        return (
            self._session.query(Task)
            .filter(
                Task.deadline.isnot(None),
                Task.deadline < today,
                Task.status != "done",
            )
            .order_by(Task.id)
            .all()
        )    