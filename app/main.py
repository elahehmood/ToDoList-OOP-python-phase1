from app.db.session import SessionLocal
from app.repositories.project_repository import SqlAlchemyProjectRepository
from app.repositories.task_repository import SqlAlchemyTaskRepository
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.cli.console import Console


def main() -> None:

 # === CLI deprecation banner (Phase 3 requirement) ===
    print(
        "[DEPRECATION] The CLI interface is deprecated and will be removed in a future version.\n"
        "Please use the FastAPI-based Web API (Phase 3) instead.\n"
        "Run: poetry run uvicorn phase3_api.api_main:app --reload\n"
    )

   
   
    session = SessionLocal()

    # constructor injection → session → repositories
    project_repo = SqlAlchemyProjectRepository(session)
    task_repo = SqlAlchemyTaskRepository(session)

    # constructor injection → repos → services
    project_service = ProjectService(project_repo)
    task_service = TaskService(task_repo)

    # constructor injection → services → CLI
    console = Console(project_service, task_service)
    console.run()


if __name__ == "__main__":
    main()
