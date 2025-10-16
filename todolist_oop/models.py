# todolist_oop/models.py
import uuid
from datetime import datetime

class Task:
    """Represents a single task in a project."""
    def __init__(self, title: str, description: str, deadline: str = None):
        self.id: str = str(uuid.uuid4())[:8]  # Short, unique ID
        self.title: str = title
        self.description: str = description
        self.deadline: str | None = deadline
        self.status: str = "todo"  # Default status is 'todo'
        self.created_at: datetime = datetime.now()

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"


class Project:
    """Represents a project that contains multiple tasks."""
    def __init__(self, name: str, description: str):
        self.id: str = str(uuid.uuid4())[:8] # Unique ID
        self.name: str = name
        self.description: str = description
        self.tasks: list['Task'] = []  # A list to hold tasks
        self.created_at: datetime = datetime.now()

    def __repr__(self):
        return f"Project(id={self.id}, name='{self.name}', tasks_count={len(self.tasks)})"