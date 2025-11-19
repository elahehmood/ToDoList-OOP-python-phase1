from datetime import datetime, date

from app.services.project_service import ProjectService
from app.services.task_service import TaskService


class Console:
    def __init__(
        self,
        project_service: ProjectService,
        task_service: TaskService,
    ) -> None:
        self.project_service = project_service
        self.task_service = task_service

    def run(self) -> None:
        while True:
            self._print_main_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self._list_projects()
            elif choice == "2":
                self._create_project()
            elif choice == "3":
                self._delete_project()
            elif choice == "4":
                self._list_tasks_for_project()
            elif choice == "5":
                self._create_task()
            elif choice == "6":
                print("Goodbye")
                break
            else:
                print("Invalid choice, try again.")

    def _print_main_menu(self) -> None:
        print("\n=== ToDo List ===")
        print("1) List projects")
        print("2) Create project")
        print("3) Delete project")
        print("4) List tasks for a project")
        print("5) Create task for a project")
        print("6) Exit")

    def _list_projects(self) -> None:
        projects = self.project_service.list_projects()
        if not projects:
            print("No projects found.")
            return

        for p in projects:
            print(f"{p.id}: {p.name} - {p.description or ''}")

    def _create_project(self) -> None:
        name = input("Project name: ").strip()
        description = input("Project description (optional): ").strip() or None
        try:
            project = self.project_service.create_project(name, description)
            print(f"Project created with ID {project.id}")
        except ValueError as e:
            print(f"Error: {e}")

    def _delete_project(self) -> None:
        project_id_str = input("Project ID to delete: ").strip()
        if not project_id_str.isdigit():
            print("Invalid ID.")
            return

        project_id = int(project_id_str)
        self.project_service.delete_project(project_id)
        print("Project deleted (if it existed).")

    def _list_tasks_for_project(self) -> None:
        project_id_str = input("Project ID: ").strip()
        if not project_id_str.isdigit():
            print("Invalid ID.")
            return

        project_id = int(project_id_str)
        tasks = self.task_service.list_tasks_for_project(project_id)
        if not tasks:
            print("No tasks for this project.")
            return

        for t in tasks:
            status = t.status
            print(
                f"{t.id}: [{status}] {t.title} | deadline={t.deadline} | closed_at={t.closed_at}"
            )

    def _create_task(self) -> None:
        project_id_str = input("Project ID: ").strip()
        if not project_id_str.isdigit():
            print("Invalid project ID.")
            return

        project_id = int(project_id_str)
        title = input("Task title: ").strip()
        deadline_str = input("Deadline (YYYY-MM-DD): ").strip()

        try:
            yyyy, mm, dd = deadline_str.split("-")
            deadline = date(int(yyyy), int(mm), int(dd))
        except Exception:
            print("Invalid date format.")
            return

        try:
            task = self.task_service.create_task(
                title=title,
                project_id=project_id,
                deadline=deadline,
            )
            print(f"Task created with ID {task.id}")
        except ValueError as e:
            print(f"Error: {e}")
