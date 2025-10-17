from .services import TodoListManager
from .models import Project

def print_main_menu():
    print("\n===== ToDoList - Main Menu =====")
    print("1. Project Management")
    print("2. Task Management")
    print("0. Exit")


def print_project_menu():
    print("\n--- Project Management ---")
    print("1. Create a new project")
    print("2. List all projects")
    print("3. Edit a project")   
    print("4. Delete a project") 
    print("9. Back to Main Menu")

def handle_project_management(manager: TodoListManager):
    """Handles the project management submenu interactions."""
    while True:
        print_project_menu()
        choice = input("Your choice: ")
        
        if choice == '1':
            create_project_cli(manager)
        elif choice == '2':
            manager.list_projects() # <-- Use manager.list_projects directly if list_projects_cli is not defined
        elif choice == '3':
            edit_project_cli(manager) # <-- CORRECTED ROUTE
        elif choice == '4': 
            manager.list_projects() # addition for better UX
            project_id = input("Enter the ID of the project to delete: ")
            manager.delete_project(project_id) # <-- CORRECTED ROUTE
        elif choice == '9':
            break
        else:
            print("Invalid choice!")


def create_project_cli(manager: TodoListManager):
    """Handles user input for creating a project."""
    print("\n--- Create Project ---")
    name = input("Project name (max 30): ")
    desc = input("Project description (max 150): ")
    
    project: Project | None = manager.create_project(name, desc)
    
    if project:
        print(f"Project '{project.name}' created successfully with ID: {project.id}")
    else:
        # Error message is printed by the service layer
        pass


def edit_project_cli(manager: TodoListManager):
    """Handles the user interaction for editing a project."""
    manager.list_projects()
    print("\n--- Edit Project ---")
    project_id = input("Enter the ID of the project to edit: ").strip()

    project = manager.find_project(project_id)
    if not project:
        return

    print(f"\n--- Editing Project: '{project.name}' (Current Name/Description) ---")
    print("Note: Leave fields blank to keep the current value (max 30/150 chars).")

    new_name = input(f"New Name (Current: {project.name}): ")
    new_description = input(f"New Description (Current: {project.description}): ")

    manager.edit_project(project_id, new_name, new_description)


def print_task_menu():
    print("\n--- Task Management ---")
    print("1. Add a task to a project")
    print("2. List tasks in a project")
    print("3. Change a task's status")
    print("4. Edit a task's details")   
    print("5. Delete a task")          
    print("9. Back to Main Menu")
    

def add_task_cli(manager: TodoListManager):
    """Handles user input for adding a task to a project."""
    print("\n--- Add Task ---")
    manager.list_projects() # Optional: Show projects for user reference
    project_id = input("Enter the project ID to add a task to: ").strip()
    
    # Check if project exists before prompting for task details (better UX)
    if not manager.find_project(project_id):
        # find_project prints the error message
        return
        
    title = input("Task title (max 30): ")
    desc = input("Task description (max 150): ")
    deadline = input("Deadline (optional, format YYYY-MM-DD): ")
    
    manager.add_task_to_project(project_id, title, desc, deadline)


def list_tasks_cli(manager: TodoListManager):
    """Handles the user interaction for listing tasks in a project (US-9)."""
    print("\n--- List Tasks ---")
    manager.list_projects()
    project_id = input("Enter the project ID to list its tasks: ").strip()
    manager.list_tasks_in_project(project_id)


def update_task_status_cli(manager: TodoListManager):
    """Handles the user interaction for changing a task's status (US-5)."""
    print("\n--- Change Task Status ---")
    manager.list_projects()
    project_id = input("Project ID containing the task: ").strip()
    
    # Optional: List tasks in project for user reference
    project = manager.find_project(project_id)
    if project:
        manager.list_tasks_in_project(project_id)
    
    task_id = input("Task ID to update: ").strip()
    status = input("New status (todo, doing, done): ").strip().lower()
    
    manager.update_task_status(project_id, task_id, status)

def edit_task_cli(manager: TodoListManager):
    """Handles the user interaction for editing a task (US-6)."""
    print("\n--- Edit Task ---")
    manager.list_projects()
    project_id = input("Project ID containing the task: ").strip()
    
    # Show tasks for better UX
    project = manager.find_project(project_id)
    if project:
        manager.list_tasks_in_project(project_id)
    
    task_id = input("Task ID to edit: ").strip()

    print("\nNote: Leave fields blank to keep current value.")
    new_title = input("New Title (max 30): ")
    new_description = input("New Description (max 150): ")
    new_deadline = input("New Deadline (YYYY-MM-DD): ")
    new_status = input("New Status (todo, doing, done): ")
    
    manager.edit_task(project_id, task_id, new_title, new_description, new_deadline, new_status)


def delete_task_cli(manager: TodoListManager):
    """Handles the user interaction for deleting a task (US-7)."""
    print("\n--- Delete Task ---")
    project_id = input("Project ID containing the task: ").strip()
    manager.list_tasks_in_project(project_id) # Show tasks for user reference
    task_id = input("Task ID to delete: ").strip()
    manager.delete_task(project_id, task_id)


def handle_task_management(manager: TodoListManager):
    """Handles the task management submenu interactions."""
    while True:
        print_task_menu()
        choice = input("Your choice: ")
        
        if choice == '1':
            add_task_cli(manager) 
        elif choice == '2':
            list_tasks_cli(manager) 
        elif choice == '3':
            update_task_status_cli(manager) 
        elif choice == '4':
            edit_task_cli(manager) # <-- NEW ROUTE
        elif choice == '5':
            delete_task_cli(manager) # <-- NEW ROUTE
        elif choice == '9':
            break
        else:
            print("Invalid choice!")


def run_cli():
    """The main application loop."""
    manager = TodoListManager()
    while True:
        print_main_menu()
        choice = input("Your choice: ")

        if choice == '1':
            handle_project_management(manager)
        elif choice == '2':
            handle_task_management(manager)
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

