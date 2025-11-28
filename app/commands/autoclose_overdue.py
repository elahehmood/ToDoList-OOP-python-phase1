# app/commands/autoclose_overdue.py

from app.db.session import SessionLocal
from app.repositories.task_repository import SqlAlchemyTaskRepository
from app.services.task_service import TaskService


def autoclose_overdue_tasks() -> None:
    """Close all overdue tasks once and exit."""
    session = SessionLocal()
    try:
        task_repo = SqlAlchemyTaskRepository(session)
        task_service = TaskService(task_repo)

        # Service decides what "overdue" means (uses Task.is_overdue + dates inside)
        closed_count = task_service.close_overdue_tasks()

        print(f"Closed {closed_count} overdue task(s).")
    finally:
        session.close()


if __name__ == "__main__":
    autoclose_overdue_tasks()
