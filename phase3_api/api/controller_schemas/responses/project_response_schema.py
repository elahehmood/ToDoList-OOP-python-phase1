from pydantic import BaseModel, ConfigDict


class ProjectResponse(BaseModel):
    """Response model for project data."""
    id: int
    name: str
    description: str | None = None

    # Equivalent of orm_mode = True in Pydantic v1
    model_config = ConfigDict(from_attributes=True)
