from datetime import date, datetime
from typing import Optional, List

from app.db.session import SessionLocal
from app.models.task import Task
from app.repositories.task_repository import TaskRepository


class TaskService:
    def __init__(self) -> None:
        self._session_factory = SessionLocal

    def create_task_for_project(
        self,
        project_id: int,
        title: str,
        description: Optional[str],
        deadline: Optional[date],
    ) -> Task:
        with self._session_factory() as session:
            repo = TaskRepository(session)
            task = repo.create_for_project(project_id, title, description, deadline)
            session.commit()
            session.refresh(task)
            return task

    def list_tasks_for_project(self, project_id: int) -> List[Task]:
        with self._session_factory() as session:
            repo = TaskRepository(session)
            return repo.list_for_project(project_id)

    def get_task(self, task_id: int) -> Optional[Task]:
        with self._session_factory() as session:
            repo = TaskRepository(session)
            return repo.get(task_id)

    def update_task_status(self, task_id: int, new_status: str) -> Optional[Task]:
        if new_status not in {"todo", "doing", "done"}:
            raise ValueError("Status must be one of: todo, doing, done")

        with self._session_factory() as session:
            repo = TaskRepository(session)
            task = repo.get(task_id)
            if not task:
                return None

            task.status = new_status
            if new_status == "done" and task.closed_at is None:
                task.closed_at = datetime.utcnow()

            repo.save(task)
            session.commit()
            session.refresh(task)
            return task

    def edit_task(
        self,
        task_id: int,
        title: Optional[str],
        description: Optional[str],
        deadline: Optional[date],
        status: Optional[str],
    ) -> Optional[Task]:
        with self._session_factory() as session:
            repo = TaskRepository(session)
            task = repo.get(task_id)
            if not task:
                return None

            if title:
                task.title = title
            if deadline:
                task.deadline = deadline
            if status:
                if status not in {"todo", "doing", "done"}:
                    raise ValueError("Status must be one of: todo, doing, done")
                task.status = status
                if status == "done" and task.closed_at is None:
                    task.closed_at = datetime.utcnow()

            repo.save(task)
            session.commit()
            session.refresh(task)
            return task

    def delete_task(self, task_id: int) -> bool:
        with self._session_factory() as session:
            repo = TaskRepository(session)
            ok = repo.delete(task_id)
            if not ok:
                return False
            session.commit()
            return True
