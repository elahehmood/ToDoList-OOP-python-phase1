from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class TaskResponse(BaseModel):
    """Response model for task data."""
    id: int
    project_id: int
    title: str
    description: str | None = None
    status: str
    deadline: date | None = None
    closed_at: datetime | None = None
    is_overdue: bool

    model_config = ConfigDict(from_attributes=True)
