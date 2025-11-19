from datetime import date, datetime
from typing import List, Optional
from app.repositories.task_repository import TaskRepository
from app.models.task import Task


class TaskService:
    """Business logic for tasks."""

    def __init__(self, task_repo: TaskRepository):
        self._task_repo = task_repo

    def create_task(
        self,
        title: str,
        project_id: int,
        deadline: date,
    ) -> Task:
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        return self._task_repo.create(
            title=title.strip(),
            project_id=project_id,
            deadline=deadline,
        )

    def get_task(self, task_id: int) -> Optional[Task]:
        return self._task_repo.get_by_id(task_id)

    def list_tasks_for_project(self, project_id: int) -> List[Task]:
        return self._task_repo.list_by_project(project_id)

    def auto_close_overdue(self, today: date) -> int:
        """Close tasks where deadline < today and status != done."""
        tasks = self._task_repo.get_overdue_not_done(today)
        count = 0

        for task in tasks:
            task.status = "done"
            task.closed_at = datetime.utcnow()
            count += 1

        return count
