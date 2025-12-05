from __future__ import annotations

import os
from datetime import date, datetime
from typing import List, Optional

from phase3_api.models.task import Task
from phase3_api.repositories.task_repository import SqlAlchemyTaskRepository


MAX_TASKS_PER_PROJECT = int(os.getenv("MAX_TASKS_PER_PROJECT", "20"))
VALID_STATUSES = {"todo", "doing", "done"}


class TaskService:
    """Service layer for task-related operations."""

    def __init__(self, task_repo: SqlAlchemyTaskRepository) -> None:
        self._task_repo = task_repo

    # ---------- CRUD ----------

    def create_task_for_project(
        self,
        project_id: int,
        title: str,
        description: Optional[str],
        deadline: Optional[date],
    ) -> Optional[Task]:
        """
        Create a new task under the given project, with phase-1 constraints:

        - title required, non-empty
        - title length <= 30
        - description length <= 150
        - per-project task limit: MAX_TASKS_PER_PROJECT
        - deadline already parsed (or None) by CLI
        """
        title_norm = (title or "").strip()
        description_norm = (description or "").strip()

        if not title_norm:
            print("Error: Task title cannot be empty.")
            return None

        if len(title_norm) > 30:
            print("Error: Task title exceeds 30 characters.")
            return None

        if len(description_norm) > 150:
            print("Error: Task description exceeds 150 characters.")
            return None

        # Per-project limit
        existing_tasks = self._task_repo.list_for_project(project_id)
        if len(existing_tasks) >= MAX_TASKS_PER_PROJECT:
            print(
                f"Error: This project has reached the maximum limit of "
                f"{MAX_TASKS_PER_PROJECT} tasks."
            )
            return None

        task = self._task_repo.create_for_project(
            project_id=project_id,
            title=title_norm,
            description=description_norm or None,
            deadline=deadline,
            status="todo",
        )
        # repository does NOT commit, service does
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
        """
        Delete a task by ID.

        Prints an error if not found.
        """
        deleted = self._task_repo.delete(task_id)
        if not deleted:
            print(f"Error: Task with ID '{task_id}' not found.")
            return False

        self._task_repo._session.commit()
        return True

    # ---------- Status / editing ----------

    def update_task_status(self, task_id: int, new_status: str) -> Optional[Task]:
        normalized_status = (new_status or "").strip().lower()
        if normalized_status not in VALID_STATUSES:
            print("Error: Status must be one of: todo, doing, done.")
            return None

        task = self._task_repo.get_by_id(task_id)
        if task is None:
            print(f"Error: Task with ID '{task_id}' not found.")
            return None

        previous_status = task.status
        task.status = normalized_status

        if normalized_status == "done":
            # going to done → ensure closed_at is set (even if it was done before)
            if previous_status != "done":
                task.closed_at = datetime.utcnow()
        else:
            # any non-done status → always clear closed_at
            task.closed_at = None

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

        - title: if provided and non-empty, updates title (<= 30 chars)
        - description: if provided and non-empty, updates description (<= 150 chars)
        - deadline: if provided (non-None), updates deadline
        - status: if provided and valid, updates status and closed_at
        """
        task = self._task_repo.get_by_id(task_id)
        if task is None:
            print(f"Error: Task with ID '{task_id}' not found.")
            return None

        updated = False

        # Title
        if title is not None:
            title_norm = title.strip()
            if title_norm:
                if len(title_norm) > 30:
                    print("Error: New task title exceeds 30 characters.")
                    return None
                task.title = title_norm
                updated = True

        # Description
        if description is not None:
            desc_norm = description.strip()
            if desc_norm:
                if len(desc_norm) > 150:
                    print("Error: New task description exceeds 150 characters.")
                    return None
                task.description = desc_norm
                updated = True

        # Deadline
        if deadline is not None:
            task.deadline = deadline
            updated = True

        # Status
        if status is not None:
            status_norm = status.strip().lower()
            if status_norm:
                if status_norm not in VALID_STATUSES:
                    print("Error: Status must be one of: todo, doing, done.")
                    return None

                previous_status = task.status
                task.status = status_norm

                if status_norm == "done":
                    if previous_status != "done":
                        task.closed_at = datetime.utcnow()
                else:
                    # any non-done status → clear closed_at
                    task.closed_at = None

                updated = True

        if not updated:
            print("Info: No changes were made.")
            return task

        self._task_repo._session.commit()
        self._task_repo._session.refresh(task)
        return task

    # ---------- Overdue auto-close ----------

    def close_overdue_tasks(self) -> int:
        """
        Close all overdue tasks:

        - A task is considered overdue based on Task.is_overdue
        - Only non-"done" tasks are affected
        - Sets status="done" and closed_at if needed

        Returns the number of tasks closed.
        """
        session = self._task_repo._session
        tasks = session.query(Task).all()
        now = datetime.utcnow()

        closed_count = 0
        for task in tasks:
            if task.status != "done" and task.is_overdue:
                task.status = "done"
                if task.closed_at is None:
                    task.closed_at = now
                closed_count += 1

        if closed_count > 0:
            session.commit()

        return closed_count
