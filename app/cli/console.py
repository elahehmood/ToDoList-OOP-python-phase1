from __future__ import annotations

from datetime import date
from typing import Optional

from app.services.project_service import ProjectService
from app.services.task_service import TaskService


class Console:
    """CLI layer: handles user interaction and delegates to services."""

    def __init__(self, project_service: ProjectService, task_service: TaskService) -> None:
        self.project_service = project_service
        self.task_service = task_service
        
    # ---------- Main loop ----------

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

    # ---------- Menus ----------

    @staticmethod
    def _print_main_menu() -> None:
        print("\n===== ToDoList - Main Menu =====")
        print("1. Project Management")
        print("2. Task Management")
        print("0. Exit")

    @staticmethod
    def _print_project_menu() -> None:
        print("\n--- Project Management ---")
        print("1. Create a new project")
        print("2. List all projects")
        print("3. Edit a project")
        print("4. Delete a project")
        print("9. Back to Main Menu")

    @staticmethod
    def _print_task_menu() -> None:
        print("\n--- Task Management ---")
        print("1. Add a task to a project")
        print("2. List tasks in a project")
        print("3. Change a task's status")
        print("4. Edit a task's details")
        print("5. Delete a task")
        print("6. Close overdue tasks")
        print("9. Back to Main Menu")

    # ---------- Project flow ----------

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

    def _print_projects(self) -> None:
        projects = self.project_service.list_projects()
        if not projects:
            print("No projects to display.")
            return

        print("\n--- Projects ---")
        for p in projects:
            desc = p.description or ""
            print(f"{p.id}: {p.name} - {desc}")

    def _create_project(self) -> None:
        print("\n--- Create Project ---")
        name = input("Project name: ")
        description = input("Project description (optional): ")

        project = self.project_service.create_project(name, description)
        if project is None:
            # Service already printed an error message
            return

        print(f"Project '{project.name}' created successfully (ID: {project.id})")

    def _list_projects(self) -> None:
        self._print_projects()

    def _edit_project(self) -> None:
        print("\n--- Edit Project ---")
        self._print_projects()
        projects = self.project_service.list_projects()
        if not projects:
            return

        raw_id = input("Enter the ID of the project to edit: ").strip()
        try:
            project_id = int(raw_id)
        except ValueError:
            print("Error: Project ID must be a number.")
            return

        project = self.project_service.get_project(project_id)
        if project is None:
            print(f"Error: Project with ID '{project_id}' not found.")
            return

        print(
            f"\nEditing project '{project.name}' "
            f"(current description: {project.description or ''})"
        )
        print("Leave blank to keep current value.")

        new_name = input(f"New name (current: {project.name}): ")
        new_description = input(
            f"New description (current: {project.description or ''}): "
        )

        self.project_service.edit_project(project_id, new_name, new_description)
        # Service prints the appropriate message

    def _delete_project(self) -> None:
        print("\n--- Delete Project ---")
        self._print_projects()
        projects = self.project_service.list_projects()
        if not projects:
            return

        raw_id = input("Enter the ID of the project to delete: ").strip()
        try:
            project_id = int(raw_id)
        except ValueError:
            print("Error: Project ID must be a number.")
            return

        ok = self.project_service.delete_project(project_id)
        if ok:
            print(f"Project with ID '{project_id}' deleted successfully.")

    # ---------- Task flow ----------

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

    def _print_tasks_for_project(self, project_id: int) -> None:
        project = self.project_service.get_project(project_id)
        if project is None:
            print(f"Error: Project with ID '{project_id}' not found.")
            return

        tasks = self.task_service.list_tasks_for_project(project_id)
        if not tasks:
            print(f"Project '{project.name}' has no tasks.")
            return

        print(f"\nTasks for project {project.id} ({project.name}):")
        for t in tasks:
            deadline_str = t.deadline.isoformat() if t.deadline else "-"
            closed_str = (
                t.closed_at.replace(microsecond=0).isoformat()
                if t.closed_at
                else "-"
            )
            print(
                f"{t.id}: {t.title} [{t.status}] "
                f"deadline={deadline_str}, closed_at={closed_str}"
            )

    def _add_task(self) -> None:
        print("\n--- Add Task ---")
        self._print_projects()
        projects = self.project_service.list_projects()
        if not projects:
            return

        raw_pid = input("Enter the project ID to add a task to: ").strip()
        try:
            project_id = int(raw_pid)
        except ValueError:
            print("Error: Project ID must be a number.")
            return

        project = self.project_service.get_project(project_id)
        if project is None:
            print(f"Error: Project with ID '{project_id}' not found.")
            return

        title = input("Task title: ")
        description = input("Task description (optional): ")
        deadline_str = input("Deadline (optional, YYYY-MM-DD): ").strip()

        deadline_date: Optional[date] = None
        if deadline_str:
            try:
                deadline_date = date.fromisoformat(deadline_str)
            except ValueError:
                print("Invalid date format, ignoring deadline (expected YYYY-MM-DD).")
                deadline_date = None

        task = self.task_service.create_task_for_project(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline_date,
        )
        if task is None:
            return

        print(f"Task '{task.title}' created with ID {task.id}.")

    def _list_tasks(self) -> None:
        print("\n--- List Tasks ---")
        self._print_projects()
        projects = self.project_service.list_projects()
        if not projects:
            return

        raw_pid = input("Enter the project ID: ").strip()
        try:
            project_id = int(raw_pid)
        except ValueError:
            print("Error: Project ID must be a number.")
            return

        self._print_tasks_for_project(project_id)

    def _change_task_status(self) -> None:
        print("\n--- Change Task Status ---")
        self._print_projects()
        projects = self.project_service.list_projects()
        if not projects:
            return

        raw_pid = input("Enter the project ID containing the task: ").strip()
        try:
            project_id = int(raw_pid)
        except ValueError:
            print("Error: Project ID must be a number.")
            return

        # Show tasks for reference
        self._print_tasks_for_project(project_id)
        tasks = self.task_service.list_tasks_for_project(project_id)
        if not tasks:
            return

        raw_tid = input("Enter the task ID to update: ").strip()
        try:
            task_id = int(raw_tid)
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        new_status = input("New status (todo, doing, done): ").strip()
        task = self.task_service.update_task_status(task_id, new_status)
        if task is None:
            return

        print(f"Task '{task.title}' status updated to '{task.status}'.")

    def _edit_task(self) -> None:
        print("\n--- Edit Task ---")
        self._print_projects()
        projects = self.project_service.list_projects()
        if not projects:
            return

        raw_pid = input("Enter the project ID containing the task: ").strip()
        try:
            project_id = int(raw_pid)
        except ValueError:
            print("Error: Project ID must be a number.")
            return

        self._print_tasks_for_project(project_id)
        tasks = self.task_service.list_tasks_for_project(project_id)
        if not tasks:
            return

        raw_tid = input("Enter the task ID to edit: ").strip()
        try:
            task_id = int(raw_tid)
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        print("Leave fields blank to keep the current value.")
        new_title = input("New title (max 30): ")
        new_description = input("New description (max 150): ")
        new_deadline_str = input("New deadline (YYYY-MM-DD): ").strip()
        new_status = input("New status (todo, doing, done): ")

        deadline_date: Optional[date] = None
        if new_deadline_str:
            try:
                deadline_date = date.fromisoformat(new_deadline_str)
            except ValueError:
                print("Error: Invalid deadline format. Please use YYYY-MM-DD.")
                return

        task = self.task_service.edit_task(
            task_id=task_id,
            title=new_title if new_title.strip() else None,
            description=new_description if new_description.strip() else None,
            deadline=deadline_date,
            status=new_status if new_status.strip() else None,
        )
        if task is None:
            return

        print(f"Task '{task.title}' updated successfully.")

    def _delete_task(self) -> None:
        print("\n--- Delete Task ---")
        self._print_projects()
        projects = self.project_service.list_projects()
        if not projects:
            return

        raw_pid = input("Enter the project ID containing the task: ").strip()
        try:
            project_id = int(raw_pid)
        except ValueError:
            print("Error: Project ID must be a number.")
            return

        self._print_tasks_for_project(project_id)
        tasks = self.task_service.list_tasks_for_project(project_id)
        if not tasks:
            return

        raw_tid = input("Enter the task ID to delete: ").strip()
        try:
            task_id = int(raw_tid)
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        ok = self.task_service.delete_task(task_id)
        if ok:
            print(f"Task with ID '{task_id}' deleted successfully.")

    def _close_overdue_tasks(self) -> None:
        print("\n--- Close Overdue Tasks ---")
        closed_count = self.task_service.close_overdue_tasks()
        print(f"Closed {closed_count} overdue task(s).")
