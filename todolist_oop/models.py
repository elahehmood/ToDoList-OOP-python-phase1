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

