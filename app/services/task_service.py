from datetime import date, datetime
from typing import List, Optional

from app.models.task import Task
from app.repositories.task_repository import SqlAlchemyTaskRepository


class TaskService:
    def __init__(self, task_repo: SqlAlchemyTaskRepository) -> None:
        self._task_repo = task_repo

    def create_task_for_project(
        self,
        project_id: int,
        title: str,
        description: Optional[str],
        deadline: Optional[date],
    ) -> Task:
        """Create a new task under the given project."""
        normalized_title = title.strip()
        if not normalized_title:
            raise ValueError("Task title must not be empty")

        normalized_description = description.strip() if description is not None else None
        if normalized_description == "":
            normalized_description = None

        task = self._task_repo.create_for_project(
            project_id=project_id,
            title=normalized_title,
            description=normalized_description,
            deadline=deadline,
        )

        self._task_repo._session.commit()
        self._task_repo._session.refresh(task)
        return task

    def list_tasks_for_project(self, project_id: int) -> List[Task]:
        """Return all tasks belonging to a given project."""
        return self._task_repo.list_for_project(project_id)

    def get_task(self, task_id: int) -> Optional[Task]:
        """Return a single task by ID."""
        return self._task_repo.get_by_id(task_id)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID. Returns True if deleted, False if not found."""
        deleted = self._task_repo.delete(task_id)
        if not deleted:
            return False

        self._task_repo._session.commit()
        return True

    def update_task_status(self, task_id: int, new_status: str) -> Optional[Task]:
        """
        Update the status of a task and maintain closed_at correctly.

        - Status must be one of: "todo", "doing", "done"
        - When status changes to "done" from a different state,
          closed_at is set to the current UTC time.
        """
        normalized_status = new_status.strip().lower()
        if normalized_status not in {"todo", "doing", "done"}:
            raise ValueError("Status must be one of: todo, doing, done")

        task = self._task_repo.get_by_id(task_id)
        if task is None:
            return None

        previous_status = task.status
        task.status = normalized_status

        if previous_status != "done" and normalized_status == "done":
            task.closed_at = datetime.utcnow()

        self._task_repo._session.commit()
        self._task_repo._session.refresh(task)
        return task

    def edit_task(
        self,
        task_id: int,
        title: Optional[str],
        description: Optional[str],
        deadline: Optional[date],
        status: Optional[str],
    ) -> Optional[Task]:
        """
        Edit task fields:

        - title: if provided and non-empty, updates title
        - description: if provided, updates description (empty string → None)
        - deadline: if provided (even None), updates deadline
        - status: if provided and valid, updates status and closed_at
        """
        task = self._task_repo.get_by_id(task_id)
        if task is None:
            return None

        if title is not None:
            normalized_title = title.strip()
            if normalized_title:
                task.title = normalized_title

        if description is not None:
            normalized_description = description.strip()
            task.description = normalized_description or None

        if deadline is not None:
            task.deadline = deadline

        if status is not None:
            normalized_status = status.strip().lower()
            if normalized_status:
                if normalized_status not in {"todo", "doing", "done"}:
                    raise ValueError("Status must be one of: todo, doing, done")
                previous_status = task.status
                task.status = normalized_status
                if previous_status != "done" and normalized_status == "done":
                    task.closed_at = datetime.utcnow()

        self._task_repo._session.commit()
        self._task_repo._session.refresh(task)
        return task
    
    def close_overdue_tasks(self, today: Optional[date] = None) -> int:
        """
        Automatically close all overdue tasks.

        - Overdue = has a non-null deadline AND deadline < today AND status != "done".
        - For each such task:
            * status is set to "done"
            * closed_at is set to current UTC time (if not already set)
        Returns:
            number of tasks that were updated.
        """
        if today is None:
            today = date.today()

        overdue_tasks = self._task_repo.find_overdue_open_tasks(today)
        if not overdue_tasks:
            return 0

        now = datetime.utcnow()

        for task in overdue_tasks:
            task.status = "done"
            if task.closed_at is None:
                task.closed_at = now

        self._task_repo._session.commit()
        return len(overdue_tasks)