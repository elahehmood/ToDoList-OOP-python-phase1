from datetime import date, datetime
from typing import List, Optional

from app.models.task import Task
from app.repositories.task_repository import SqlAlchemyTaskRepository


class TaskService:
    def __init__(self, task_repo: SqlAlchemyTaskRepository) -> None:
        self._task_repo = task_repo


    def create_task_for_project(self, project_id: int, title: str, deadline: Optional[date]) -> Task:

        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")


        task = self._task_repo.create_for_project(
            project_id=project_id,
            title=title,
            deadline=deadline,
            status="todo",      
        )

        task.closed_at = None

        self._task_repo._session.commit()
        self._task_repo._session.refresh(task)
        return task
    

    def list_tasks_for_project(self, project_id: int) -> List[Task]:
        return self._task_repo.list_for_project(project_id)

    def get_task(self, task_id: int) -> Optional[Task]:
        return self._task_repo.get_by_id(task_id)

    def delete_task(self, task_id: int) -> bool:
        ok = self._task_repo.delete(task_id)
        if not ok:
            return False
        self._task_repo._session.commit()
        return True

    def update_task_status(self, task_id: int, new_status: str) -> Optional[Task]:

        if new_status not in {"todo", "doing", "done"}:
            raise ValueError("Status must be one of: todo, doing, done")

        task = self._task_repo.get_by_id(task_id)
        if not task:
            return None

        if new_status == "done" and task.status != "done":
            task.closed_at = datetime.utcnow()

        if new_status in {"todo", "doing"}:
            task.closed_at = None

        task.status = new_status

        self._task_repo._session.commit()
        self._task_repo._session.refresh(task)
        return task

    def edit_task(
        self,
        task_id: int,
        title: Optional[str],
        deadline: Optional[date],
        status: Optional[str],
    ) -> Optional[Task]:
        task = self._task_repo.get_by_id(task_id)
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

        self._task_repo._session.commit()
        self._task_repo._session.refresh(task)
        return task
