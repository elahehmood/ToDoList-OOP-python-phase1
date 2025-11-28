from __future__ import annotations

from datetime import datetime
from typing import Optional

from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.models.project import Project
from app.models.task import Task


class Console:
    def __init__(
        self,
        project_service: ProjectService,
        task_service: TaskService,
    ) -> None:
        self.project_service = project_service
        self.task_service = task_service

    # ===========================
    # Main loop
    # ===========================
    def run(self) -> None:
        while True:
            self._print_main_menu()
            choice = input("Your choice: ").strip()

            if choice == "1":
                self._handle_project_management()
            elif choice == "2":
                self._handle_task_management()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    # ===========================
    # Menus
    # ===========================
    def _print_main_menu(self) -> None:
        print("\n===== ToDoList - Main Menu =====")
        print("1. Project Management")
        print("2. Task Management")
        print("0. Exit")

    def _print_project_menu(self) -> None:
        print("\n--- Project Management ---")
        print("1. Create a new project")
        print("2. List all projects")
        print("3. Edit a project")
        print("4. Delete a project")
        print("9. Back to Main Menu")

    def _print_task_menu(self) -> None:
        print("\n--- Task Management ---")
        print("1. Add a task to a project")
        print("2. List tasks in a project")
        print("3. Change a task's status")
        print("4. Edit a task's details")
        print("5. Delete a task")
        print("6. Close overdue tasks")
        print("9. Back to Main Menu")

    # ===========================
    # Helpers
    # ===========================
    def _read_int(self, prompt: str) -> Optional[int]:
        raw = input(prompt).strip()
        if not raw:
            print("Empty input.")
            return None
        try:
            return int(raw)
        except ValueError:
            print("Invalid number.")
            return None

    def _parse_date_input(self, raw: str) -> Optional["datetime.date"]:
        raw = raw.strip()
        if not raw:
            return None
        try:
            return datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format, ignoring deadline. (Expected YYYY-MM-DD)")
            return None

    def _print_projects(self) -> None:
        projects = self.project_service.list_projects()
        if not projects:
            print("No projects found.")
            return

        print("\n--- Projects ---")
        for p in projects:
            desc = p.description or ""
            print(f"{p.id}: {p.name} - {desc}")

    def _print_tasks_for_project(self, project: Project) -> None:
        tasks = self.task_service.list_tasks_for_project(project.id)
        if not tasks:
            print(f"No tasks for project {project.id} ({project.name}).")
            return

        print(f"\nTasks for project {project.id} ({project.name}):")
        for t in tasks:
            deadline_str = t.deadline.isoformat() if t.deadline else "-"
            closed_str = (
                t.closed_at.isoformat(timespec="seconds") if t.closed_at else "-"
            )
            print(
                f"{t.id}: {t.title} "
                f"[{t.status}] deadline={deadline_str}, closed_at={closed_str}"
            )

    # ===========================
    # Project management
    # ===========================
    def _handle_project_management(self) -> None:
        while True:
            self._print_project_menu()
            choice = input("Your choice: ").strip()

            if choice == "1":
                self._create_project()
            elif choice == "2":
                self._list_projects()
            elif choice == "3":
                self._edit_project()
            elif choice == "4":
                self._delete_project()
            elif choice == "9":
                break
            else:
                print("Invalid choice!")

    def _create_project(self) -> None:
        print("\n--- Create Project ---")
        name = input("Project name: ").strip()
        description = input("Project description (optional): ").strip()

        project = self.project_service.create_project(name, description)

        if project is None:
            return  # error already printed by service

        print(f"Project '{project.name}' created successfully (ID: {project.id})")

    def _list_projects(self) -> None:
        self._print_projects()

    def _edit_project(self) -> None:
        print("\n--- Edit Project ---")
        self._print_projects()

        pid_raw = input("Enter the ID of the project to edit: ").strip()
        if not pid_raw.isdigit():
            print("Invalid project ID.")
            return

        project_id = int(pid_raw)
        project = self.project_service.get_project(project_id)
        if project is None:
            print("Project not found.")
            return

        print(f"\nEditing project '{project.name}' (current description: {project.description or ''})")
        print("Leave blank to keep current value.")

        new_name = input(f"New name (current: {project.name}): ").strip()
        new_description = input(f"New description (current: {project.description or ''}): ").strip()

        if not new_name:
            new_name = project.name
        if new_description == "":
            new_description = project.description

        updated = self.project_service.edit_project(project_id, new_name, new_description)

        if updated is not None:
            print("Project updated successfully.")

    def _delete_project(self) -> None:
        self._print_projects()
        print("\n--- Delete Project ---")

        project_id = self._read_int("Enter the ID of the project to delete: ")
        if project_id is None:
            return

        ok = self.project_service.delete_project(project_id)
        if not ok:
            print("Project not found.")
            return

        print("Project deleted successfully.")

    # ===========================
    # Task management
    # ===========================
    def _handle_task_management(self) -> None:
        while True:
            self._print_task_menu()
            choice = input("Your choice: ").strip()

            if choice == "1":
                self._add_task()
            elif choice == "2":
                self._list_tasks()
            elif choice == "3":
                self._change_task_status()
            elif choice == "4":
                self._edit_task()
            elif choice == "5":
                self._delete_task()
            elif choice == "6":
                self._close_overdue_tasks()                
            elif choice == "9":
                break
            else:
                print("Invalid choice!")

    def _select_project(self) -> Optional[Project]:
        self._print_projects()
        project_id = self._read_int("Enter the project ID: ")
        if project_id is None:
            return None

        project = self.project_service.get_project(project_id)
        if not project:
            print("Project not found.")
            return None
        return project


    def _add_task(self) -> None:
        print("\n--- Add Task ---")
        self._print_projects()

        project_id_str = input("Enter the project ID to add a task to: ").strip()
        if not project_id_str.isdigit():
            print("Invalid project ID.")
            return

        project_id = int(project_id_str)

        # Check that the project exists before creating a task
        project = self.project_service.get_project(project_id)
        if project is None:
            print(f"Project with ID {project_id} not found.")
            return

        title = input("Task title: ").strip()
        description = input("Task description (optional): ").strip()

        deadline_input = input("Deadline (optional, YYYY-MM-DD): ").strip()
        deadline_date: date | None = None
        if deadline_input:
            try:
                year, month, day = map(int, deadline_input.split("-"))
                deadline_date = date(year, month, day)
            except ValueError:
                print("Invalid date format, ignoring deadline (expected YYYY-MM-DD).")

        task = self.task_service.create_task_for_project(
            project_id=project_id,
            title=title,
            description=description or None,
            deadline=deadline_date,
        )

        print(f"Task '{task.title}' created with ID {task.id}.")

    def _list_tasks(self) -> None:
        """List all tasks for a chosen project."""
        print("\n--- List Tasks ---")
        self._print_projects()

        project_id_str = input("Enter the project ID: ").strip()
        if not project_id_str.isdigit():
            print("Invalid project ID.")
            return

        project_id = int(project_id_str)

        project = self.project_service.get_project(project_id)
        if project is None:
            print(f"Project with ID {project_id} not found.")
            return

        tasks = self.task_service.list_tasks_for_project(project_id)
        if not tasks:
            print(f"No tasks found for project {project_id} ({project.name}).")
            return

        print(f"\nTasks for project {project_id} ({project.name}):")
        for t in tasks:
            deadline_str = t.deadline.isoformat() if t.deadline else "-"
            closed_at_str = t.closed_at.isoformat() if t.closed_at else "-"
            print(f"{t.id}: {t.title} [{t.status}] deadline={deadline_str}, closed_at={closed_at_str}")

    def _list_tasks(self) -> None:
        """List all tasks for a chosen project."""
        print("\n--- List Tasks ---")
        self._print_projects()

        project_id_str = input("Enter the project ID: ").strip()
        if not project_id_str.isdigit():
            print("Invalid project ID.")
            return

        project_id = int(project_id_str)

        project = self.project_service.get_project(project_id)
        if project is None:
            print(f"Project with ID {project_id} not found.")
            return

        tasks = self.task_service.list_tasks_for_project(project_id)
        if not tasks:
            print(f"No tasks found for project {project_id} ({project.name}).")
            return

        print(f"\nTasks for project {project_id} ({project.name}):")
        for t in tasks:
            deadline_str = t.deadline.isoformat() if t.deadline else "-"
            closed_at_str = t.closed_at.isoformat() if t.closed_at else "-"
            print(f"{t.id}: {t.title} [{t.status}] deadline={deadline_str}, closed_at={closed_at_str}")


    def _change_task_status(self) -> None:
        print("\n--- Change Task Status ---")
        project = self._select_project()
        if not project:
            return

        self._print_tasks_for_project(project)

        task_id = self._read_int("Task ID to update: ")
        if task_id is None:
            return

        new_status = input("New status (todo, doing, done): ").strip().lower()

        try:
            updated = self.task_service.update_task_status(task_id, new_status)
        except ValueError as e:
            print(f"Error: {e}")
            return

        if not updated:
            print("Task not found.")
            return

        print("Task status updated successfully.")

    def _edit_task(self) -> None:
        print("\n--- Edit Task ---")
        self._print_projects()
        project_id_str = input("Enter the project ID: ").strip()

        if not project_id_str.isdigit():
            print("Invalid project ID.")
            return

        project_id = int(project_id_str)
        self._print_tasks_for_project(project_id)

        task_id_str = input("Enter the task ID to edit: ").strip()
        if not task_id_str.isdigit():
            print("Invalid task ID.")
            return

        task_id = int(task_id_str)

        print("Leave fields blank to keep current values.")
        new_title = input("New title (optional): ")
        new_description = input("New description (optional): ")
        new_deadline_str = input("New deadline (optional, YYYY-MM-DD): ")
        new_status = input("New status (todo/doing/done, optional): ")

        from datetime import datetime, date

        new_deadline: date | None = None
        if new_deadline_str:
            try:
                new_deadline = datetime.strptime(new_deadline_str, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format, ignoring deadline (expected YYYY-MM-DD).")

        # normalize blanks → None
        title_arg = new_title if new_title.strip() else None
        description_arg = new_description if new_description.strip() else None
        status_arg = new_status if new_status.strip() else None

        try:
            updated = self.task_service.edit_task(
                task_id=task_id,
                title=title_arg,
                description=description_arg,
                deadline=new_deadline,
                status=status_arg,
            )
        except ValueError as exc:
            print(f"Error: {exc}")
            return

        if updated is None:
            print("Task not found.")
        else:
            print(f"Task {updated.id} updated.")

    def _delete_task(self) -> None:
        print("\n--- Delete Task ---")
        project = self._select_project()
        if not project:
            return

        self._print_tasks_for_project(project)

        task_id = self._read_int("Task ID to delete: ")
        if task_id is None:
            return

        ok = self.task_service.delete_task(task_id)
        if not ok:
            print("Task not found.")
            return

        print("Task deleted successfully.")

    def _close_overdue_tasks(self) -> None:
        print("\n--- Close Overdue Tasks ---")
        count = self.task_service.close_overdue_tasks()

        if count == 0:
            print("No overdue tasks were found.")
        else:
            print(f"Automatically closed {count} overdue task(s).")
