from fastapi import APIRouter, FastAPI

from phase3_api.api.controllers import projects_controller, tasks_controller

# Root API router with /api prefix
api_router = APIRouter(prefix="/api")


# /api/projects/...
api_router.include_router(
    projects_controller.router,
    prefix="/projects",
    tags=["projects"],
)

# /api/tasks/...
api_router.include_router(
    tasks_controller.router,
    prefix="/tasks",
    tags=["tasks"],
)


def include_all_routers(app: FastAPI) -> None:
    """
    Attach the main API router to the FastAPI application.
    """
    app.include_router(api_router)
