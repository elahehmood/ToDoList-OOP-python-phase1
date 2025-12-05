from fastapi import FastAPI
from phase3_api.api.routers import include_all_routers

# FastAPI application instance
app = FastAPI(
    title="ToDoList Phase 3 API",
    version="0.1.0",
    description="Phase 3 - RESTful Web API for the ToDoList project.",
)


@app.get("/", tags=["health"])
def health_check():
    """
    Simple health-check endpoint.
    """
    return {"status": "ok"}


# attach all routers (projects, tasks, ...)
include_all_routers(app)
