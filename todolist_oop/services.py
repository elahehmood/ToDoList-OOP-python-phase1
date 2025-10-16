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