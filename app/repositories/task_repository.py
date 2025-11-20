from typing import Optional, List
from datetime import date
from sqlalchemy.orm import Session
from app.models.task import Task


class TaskRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_for_project(
        self,
        project_id: int,
        title: str,
        description: Optional[str],
        deadline: Optional[date],
    ) -> Task:
        task = Task(
            project_id=project_id,
            title=title,
            status="todo",
            deadline=deadline,
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

    def get(self, task_id: int) -> Optional[Task]:
        return self._session.query(Task).filter(Task.id == task_id).first()

    def delete(self, task_id: int) -> bool:
        task = self.get(task_id)
        if not task:
            return False
        self._session.delete(task)
        return True

    def save(self, task: Task) -> Task:
      
        return task
