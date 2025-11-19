from datetime import date

from app.db.session import SessionLocal
from app.repositories.task_repository import SqlAlchemyTaskRepository
from app.services.task_service import TaskService


def autoclose_overdue_tasks() -> None:
    session = SessionLocal()
    try:
        task_repo = SqlAlchemyTaskRepository(session)
        task_service = TaskService(task_repo)

        today = date.today()
        closed_count = task_service.auto_close_overdue(today)
        session.commit()

        print(f"Closed {closed_count} overdue tasks")
    finally:
        session.close()


if __name__ == "__main__":
    autoclose_overdue_tasks()
