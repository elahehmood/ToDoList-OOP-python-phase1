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
            return False  # find_project prints the error message

        # 1. Prepare inputs
        new_name = new_name.strip()
        new_description = new_description.strip()
        
        updated = False

        # 2. Check and update Name 
        if new_name and new_name != project.name:
            if len(new_name) > 30:
                print("Error: New project name exceeds 30 characters.")
                return False
            
            # Check uniqueness for the new name against all OTHER projects
            if any(p.name == new_name and p.id != project_id for p in self.projects):
                print("Error: A project with this new name already exists.")
                return False
                
            project.name = new_name
            updated = True

        # 3. Check and update Description 
        if new_description and new_description != project.description:
            if len(new_description) > 150:
                print("Error: New project description exceeds 150 characters.")
                return False
            
            project.description = new_description
            updated = True
            
        if updated:
            print(f"Project '{project.name}' updated successfully.")
            return True
        else:
            print("Info: No changes were made (input fields were empty or identical to current values).")
            return True # Still return True as the operation was succesful