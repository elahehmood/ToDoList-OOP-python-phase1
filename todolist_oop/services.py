import os
from dotenv import load_dotenv
from datetime import datetime
from .models import Project, Task 

# Load environment variables from .env file
load_dotenv()

class TodoListManager:
    """Manages all projects and tasks (The main service layer)."""
    def __init__(self):
        self.projects: list[Project] = []
        # Read configurations from .env
        self.max_projects: int = int(os.getenv("MAX_PROJECTS", 10))
        self.max_tasks: int = int(os.getenv("MAX_TASKS_PER_PROJECT", 20))
    
    def find_project(self, project_id: str) -> Project | None:
        """Finds a project by its ID."""
        for project in self.projects:
            if project.id == project_id:
                return project
            print(f"Error: Project with ID '{project_id}' not found.")
        return None
        
    
    def create_project(self, name: str, description: str) -> Project | None:
        """Creates a new project (AC: limit checks, unique name)."""
        name = name.strip()
        description = description.strip()

        # 1. Check MAX_NUMBER_OF_PROJECT limit
        if len(self.projects) >= self.max_projects:
            print(f"Error: You have reached the maximum limit of {self.max_projects} projects.")
            return None
        
        # 2. Check for uniqueness and length
        if len(name) > 30:
            print("Error: Project name exceeds 30 characters.")
            return None
        if len(description) > 150:
            print("Error: Project description exceeds 150 characters.")
            return None
        if any(p.name == name for p in self.projects):
            print("Error: A project with this name already exists.")
            return None

        project = Project(name, description)
        self.projects.append(project)
        return project
    
    def list_projects(self):
        """Displays a list of all projects (AC: sorted by creation time)."""
        if not self.projects:
            print("No projects to display.")
            return

        # Sort by creation time (ascending)
        sorted_projects = sorted(self.projects, key=lambda p: p.created_at)
        
        print("\n--- Project List ---")
        for p in sorted_projects:
            print(f"ID: {p.id} | Name: {p.name} | Description: {p.description}")
    
    def delete_project(self, project_id: str) -> bool:
        """Deletes a project and all its tasks (Cascade Delete)."""
        project = self.find_project(project_id)
        if project:
            self.projects.remove(project)
            print(f"Project '{project.name}' and all its tasks were deleted successfully.")
            return True
        # NOTE: find_project already prints "Error: Project with this ID not found."
        return False

    def edit_project(self, project_id: str, new_name: str, new_description: str) -> bool:
        """
        Finds a project by ID and updates its name and description (US-2).
        AC: Observes length limits, checks for name uniqueness, and updates only non-empty fields.
        """
        project = self.find_project(project_id)
        if not project:
            return False

        new_name = new_name.strip()
        new_description = new_description.strip()
        updated = False

        # Update Name
        if new_name and new_name != project.name:
            if len(new_name) > 30:
                print("Error: New project name exceeds 30 characters.")
                return False
            if any(p.name == new_name and p.id != project_id for p in self.projects):
                print("Error: A project with this new name already exists.")
                return False
            project.name = new_name
            updated = True

        # Update Description
        if new_description and new_description != project.description:
            if len(new_description) > 150:
                print("Error: New project description exceeds 150 characters.")
                return False
            project.description = new_description
            updated = True

        if updated:
            print(f" Project '{project.name}' updated successfully.")
            return True
        print("Info: No changes were made.")
        return True # Successful operation even if nothing changed
    
    def edit_task(self, project_id: str, task_id: str, 
                  new_title: str, new_description: str, 
                  new_deadline: str, new_status: str) -> bool:
        """
        Edits the details (title, description, deadline, status) of a specific task (US-6).
        AC: Checks length limits, valid date format, and valid status.
        Only updates non-empty fields.
        """
        task = self.find_task_in_project(project_id, task_id)
        if not task:
            # Error message printed by find_task_in_project
            return False

        updated = False
        valid_statuses = ["todo", "doing", "done"]

        # 1. Update Title (if provided)
        if new_title.strip():
            if len(new_title.strip()) > 30:
                print("Error: New task title exceeds 30 characters.")
                return False
            task.title = new_title.strip()
            updated = True

        # 2. Update Description (if provided)
        if new_description.strip():
            if len(new_description.strip()) > 150:
                print("Error: New task description exceeds 150 characters.")
                return False
            task.description = new_description.strip()
            updated = True

        # 3. Update Deadline (if provided)
        if new_deadline.strip():
            try:
                # Validate date format
                from datetime import datetime
                datetime.strptime(new_deadline.strip(), '%Y-%m-%d')
                task.deadline = new_deadline.strip()
                updated = True
            except ValueError:
                print("Error: Invalid deadline format. Please use YYYY-MM-DD.")
                return False
        
        # 4. Update Status (if provided)
        if new_status.strip():
            new_status_lower = new_status.strip().lower()
            if new_status_lower not in valid_statuses:
                print(f"Error: Invalid status. Allowed statuses are: {valid_statuses}")
                return False
            task.status = new_status_lower
            updated = True

        if updated:
            print(f" Task '{task.title}' updated successfully.")
            return True
        
        print("Info: No changes were made (input fields were empty).")
        return True

    def add_task_to_project(self, project_id: str, title: str, description: str, deadline: str = None) -> Task | None:
        """
        Adds a new task to a specific project (US-4).
        AC: Checks limits, string lengths (title<=30, desc<=150), valid deadline.
        """
        project = self.find_project(project_id)
        if not project:
            return None # find_project prints error

        # 1. Check MAX_NUMBER_OF_TASK limit
        if len(project.tasks) >= self.max_tasks:
            print(f"Error: This project has reached the maximum limit of {self.max_tasks} tasks.")
            return None

        # 2. Check Title and Description length (AC)
        if len(title.strip()) > 30:
            print("Error: Task title exceeds 30 characters.")
            return None
        if len(description.strip()) > 150:
            print("Error: Task description exceeds 150 characters.")
            return None

        # 3. Check Deadline validity (AC)
        if deadline:
            try:
                # Attempt to parse the date to validate it, then convert back to string if needed
                datetime.strptime(deadline, '%Y-%m-%d') 
            except ValueError:
                print("Error: Invalid deadline format. Please use YYYY-MM-DD.")
                return None

        # 4. Create and add Task
        task = Task(title.strip(), description.strip(), deadline)
        project.tasks.append(task)
        print(f"Task '{title.strip()}' was successfully added to project '{project.name}'.")
        return task

    def delete_task(self, project_id: str, task_id: str) -> bool:
        """Deletes a specific task from a project (US-7)."""
        project = self.find_project(project_id)
        if not project:
            # find_project prints the error
            return False

        for task in project.tasks:
            if task.id == task_id:
                project.tasks.remove(task)
                print(f"Task '{task.title}' was successfully deleted from project '{project.name}'.")
                return True
        
        print(f"Error: Task with ID '{task_id}' not found in this project.")
        return False
    
    def find_task_in_project(self, project_id: str, task_id: str) -> Task | None:
        """Finds a specific task within a specific project."""
        project = self.find_project(project_id)
        if project:
            for task in project.tasks:
                if task.id == task_id:
                    return task
            print(f"Error: Task with ID '{task_id}' not found in project '{project.name}'.")
            return None
        # find_project prints the error message if project is not found
        return None
    
    def update_task_status(self, project_id: str, task_id: str, status: str) -> bool:
        """Updates the status of a specific task (US-5)."""
        valid_statuses = ["todo", "doing", "done"]
        status = status.strip().lower()

        if status not in valid_statuses:
            print(f"Error: Invalid status. Allowed statuses are: {valid_statuses}")
            return False

        task = self.find_task_in_project(project_id, task_id)
        if task:
            task.status = status
            print(f"Task '{task.title}' status updated to '{status}'.")
            return True
        # find_task_in_project prints the error message if task is not found
        return False