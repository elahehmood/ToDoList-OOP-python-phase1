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

# todolist_oop/cli.py
# ... (all previous code)

def print_main_menu():
    print("\n===== ToDoList - Main Menu =====")
    print("1. Project Management")
    print("2. Task Management")
    print("0. Exit")

# Placeholder for Task Management (will be implemented later)
def handle_task_management(manager: TodoListManager):
    """Handles the task management submenu interactions."""
    print("Task management is not yet implemented.")

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

