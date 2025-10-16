from .services import TodoListManager
from .models import Project

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
            list_projects_cli(manager)
        elif choice == '3':
            manager.list_projects() # addition for better UX
            project_id = input("Enter the ID of the project to delete: ")
            manager.delete_project(project_id)   
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

def print_main_menu():
    print("\n===== ToDoList - Main Menu =====")
    print("1. Project Management")
    print("2. Task Management")
    print("0. Exit")

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

def handle_task_management(manager: TodoListManager):
    """Handles the task management submenu interactions."""
    while True:
        print_task_menu()
        choice = input("Your choice: ")
        
        if choice == '1':
            add_task_cli(manager) # <--- NEW HANDLER
        elif choice == '2':
            list_tasks_cli(manager) # <--- NEW HANDLER
        elif choice == '3':
            update_task_status_cli(manager) # <--- NEW HANDLER
        # Options 4, 5 will be added later
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

