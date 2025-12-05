from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_projects_stub():
    """
    Temporary stub endpoint for listing projects.
    Will be replaced with real implementation using services & DB.
    """
    return []
