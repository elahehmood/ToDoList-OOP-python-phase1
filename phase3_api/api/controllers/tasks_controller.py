from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_tasks_stub():
    """
    Temporary stub endpoint for listing tasks.
    Will be replaced with real implementation using services & DB.
    """
    return []
