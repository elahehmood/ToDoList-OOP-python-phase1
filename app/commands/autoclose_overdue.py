from __future__ import annotations

from datetime import datetime

from app.db.session import SessionLocal
from app.repositories.task_repository import SqlAlchemyTaskRepository
from app.services.task_service import TaskService


def autoclose_overdue_tasks() -> int:
    """
    Close all overdue tasks once and return how many were updated.
    Overdue logic is encapsulated in TaskService.close_overdue_tasks().
    """
    session = SessionLocal()
    try:
        task_repo = SqlAlchemyTaskRepository(session)
        task_service = TaskService(task_repo)

        closed_count = task_service.close_overdue_tasks()

        now = datetime.utcnow().isoformat(timespec="seconds")
        print(f"[{now}] Closed {closed_count} overdue task(s).")

        return closed_count
    finally:
        session.close()


if __name__ == "__main__":
    autoclose_overdue_tasks()
