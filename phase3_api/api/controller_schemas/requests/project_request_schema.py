from pydantic import BaseModel, Field


class ProjectCreateRequest(BaseModel):
    """Request payload for creating a new project."""
    name: str = Field(min_length=1, max_length=30)
    description: str | None = Field(default=None, max_length=150)


class ProjectUpdateRequest(BaseModel):
    """Request payload for partially updating an existing project."""
    name: str | None = Field(default=None, min_length=1, max_length=30)
    description: str | None = Field(default=None, max_length=150)
