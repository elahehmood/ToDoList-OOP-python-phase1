from datetime import datetime

from app.services.project_service import ProjectService
from app.services.task_service import TaskService


class Console:
    def __init__(self, project_service: ProjectService, task_service: TaskService) -> None:
        self.project_service = project_service
        self.task_service = task_service

    # ---------- Main Loop ----------
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

    def _print_main_menu(self) -> None:
        print("\n===== ToDoList - Main Menu =====")
        print("1. Project Management")
        print("2. Task Management")
        print("0. Exit")

    # ---------- Project Management ----------
    def _print_project_menu(self) -> None:
        print("\n--- Project Management ---")
        print("1. Create a new project")
        print("2. List all projects")
        print("3. Delete a project")
        print("9. Back to Main Menu")

    def _handle_project_management(self) -> None:
        while True:
            self._print_project_menu()
            choice = input("Your choice: ").strip()

            if choice == "1":
                self._create_project()
            elif choice == "2":
                self._list_projects()
            elif choice == "3":
                self._delete_project()
            elif choice == "9":
                break
            else:
                print("Invalid choice!")

    def _create_project(self) -> None:
        print("\n--- Create Project ---")
        name = input("Project name: ").strip()
        description = input("Project description (optional): ").strip() or None

        try:
            project = self.project_service.create_project(name, description)
            print(f"Project '{project.name}' created successfully (ID: {project.id})")
        except ValueError as e:
            print(f"Error: {e}")

    def _list_projects(self) -> None:
        projects = self.project_service.list_projects()
        if not projects:
            print("No projects found.")
            return

        print("\n--- Projects ---")
        for p in projects:
            print(f"{p.id}: {p.name} - {p.description or ''}")

    def _delete_project(self) -> None:
        self._list_projects()
        project_id_raw = input("Enter the ID of the project to delete: ").strip()
        if not project_id_raw.isdigit():
            print("Invalid ID.")
            return

        project_id = int(project_id_raw)
        ok = self.project_service.delete_project(project_id)
        if ok:
            print("Project deleted.")
        else:
            print("Project not found.")

    # ---------- Task Management ----------
    def _print_task_menu(self) -> None:
        print("\n--- Task Management ---")
        print("1. Add a task to a project")
        print("2. List tasks in a project")
        print("3. Change a task's status")
        print("4. Edit a task's details")
        print("5. Delete a task")
        print("9. Back to Main Menu")

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
            elif choice == "9":
                break
            else:
                print("Invalid choice!")

    def _add_task(self) -> None:
        print("\n--- Add Task ---")
        self._list_projects()
        project_id_raw = input("Enter the project ID to add a task to: ").strip()
        if not project_id_raw.isdigit():
            print("Invalid project ID.")
            return

        project_id = int(project_id_raw)
        title = input("Task title: ").strip()
        deadline_raw = input("Deadline (optional, YYYY-MM-DD): ").strip()
        deadline = None
        if deadline_raw:
            try:
                deadline = datetime.strptime(deadline_raw, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format, ignoring deadline.")

        task = self.task_service.create_task_for_project(
            project_id=project_id,
            title=title,
            deadline=deadline,
        )
        print(f"Task '{task.title}' created with ID: {task.id}")

    def _list_tasks(self) -> None:
        print("\n--- List Tasks ---")
        self._list_projects()
        project_id_raw = input("Enter the project ID to list its tasks: ").strip()
        if not project_id_raw.isdigit():
            print("Invalid project ID.")
            return
        project_id = int(project_id_raw)

        tasks = self.task_service.list_tasks_for_project(project_id)
        if not tasks:
            print("No tasks for this project.")
            return

        print(f"\nTasks for project {project_id}:")
        for t in tasks:
            deadline = t.deadline.isoformat() if t.deadline else "-"
            closed = t.closed_at.isoformat() if t.closed_at else "-"
            print(f"{t.id}: {t.title} [{t.status}] deadline={deadline}, closed_at={closed}")

    def _change_task_status(self) -> None:
        print("\n--- Change Task Status ---")
        self._list_projects()
        project_id_raw = input("Project ID containing the task: ").strip()
        if not project_id_raw.isdigit():
            print("Invalid project ID.")
            return

        project_id = int(project_id_raw)
        tasks = self.task_service.list_tasks_for_project(project_id)
        if not tasks:
            print("No tasks for this project.")
            return

        for t in tasks:
            deadline = t.deadline.isoformat() if t.deadline else "-"
            print(f"{t.id}: {t.title} [{t.status}] deadline={deadline}")

        task_id_raw = input("Task ID to update: ").strip()
        if not task_id_raw.isdigit():
            print("Invalid task ID.")
            return
        task_id = int(task_id_raw)

        new_status = input("New status (todo, doing, done): ").strip().lower()
        try:
            task = self.task_service.update_task_status(task_id, new_status)
        except ValueError as e:
            print(f"Error: {e}")
            return

        if not task:
            print("Task not found.")
        else:
            print(f"Task '{task.title}' updated to status '{task.status}'.")

    def _edit_task(self) -> None:
        print("\n--- Edit Task ---")
        self._list_projects()
        project_id_raw = input("Project ID containing the task: ").strip()
        if not project_id_raw.isdigit():
            print("Invalid project ID.")
            return
        project_id = int(project_id_raw)

        tasks = self.task_service.list_tasks_for_project(project_id)
        if not tasks:
            print("No tasks for this project.")
            return

        for t in tasks:
            print(f"{t.id}: {t.title} [{t.status}]")

        task_id_raw = input("Task ID to edit: ").strip()
        if not task_id_raw.isdigit():
            print("Invalid task ID.")
            return
        task_id = int(task_id_raw)

        print("Leave fields blank to keep current value.")
        new_title = input("New title: ").strip()
        new_deadline_raw = input("New deadline (YYYY-MM-DD): ").strip()
        new_status = input("New status (todo, doing, done): ").strip().lower()

        deadline = None
        if new_deadline_raw:
            try:
                deadline = datetime.strptime(new_deadline_raw, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format, ignoring new deadline.")

        try:
            task = self.task_service.edit_task(
                task_id=task_id,
                title=new_title or None,
                deadline=deadline,
                status=new_status or None,
            )
        except ValueError as e:
            print(f"Error: {e}")
            return

        if not task:
            print("Task not found.")
        else:
            print("Task updated.")

    def _delete_task(self) -> None:
        print("\n--- Delete Task ---")
        self._list_projects()
        project_id_raw = input("Project ID containing the task: ").strip()
        if not project_id_raw.isdigit():
            print("Invalid project ID.")
            return
        project_id = int(project_id_raw)

        tasks = self.task_service.list_tasks_for_project(project_id)
        if not tasks:
            print("No tasks for this project.")
            return

        for t in tasks:
            print(f"{t.id}: {t.title} [{t.status}]")

        task_id_raw = input("Task ID to delete: ").strip()
        if not task_id_raw.isdigit():
            print("Invalid task ID.")
            return
        task_id = int(task_id_raw)

        ok = self.task_service.delete_task(task_id)
        if ok:
            print("Task deleted.")
        else:
            print("Task not found.")
