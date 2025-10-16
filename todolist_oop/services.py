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
