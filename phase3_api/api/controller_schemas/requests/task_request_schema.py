from datetime import date
from pydantic import BaseModel, Field


class TaskCreateRequest(BaseModel):
    """Request payload for creating a new task within a project."""
    project_id: int
    title: str = Field(min_length=1, max_length=30)
    description: str | None = Field(default=None, max_length=150)
    deadline: date | None = None


class TaskUpdateRequest(BaseModel):
    """Request payload for partially updating an existing task."""
    title: str | None = Field(default=None, min_length=1, max_length=30)
    description: str | None = Field(default=None, max_length=150)
    deadline: date | None = None
    status: str | None = Field(
        default=None,
        description="Valid values: 'todo', 'doing', 'done'.",
    )
