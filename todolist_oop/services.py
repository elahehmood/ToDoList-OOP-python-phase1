# todolist_oop/services.py
import os
from dotenv import load_dotenv
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
