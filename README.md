
# 📋 ToDoList-OOP – Phase 1 → Phase 3

A multi-phase ToDo List management system implemented in Python using an Object-Oriented Programming (OOP) approach, evolving from a simple CLI to a fully RESTful Web API.

- **Phase 1:** In-Memory OOP CLI
- **Phase 2:** RDB + Scheduling (PostgreSQL, SQLAlchemy, layered architecture)
- **Phase 3:** FastAPI Web API (CLI deprecated, RESTful API)

---

## Phase 1 – ToDoList-OOP-python-phase1 (In-Memory CLI)

This is an advanced, Command Line Interface (CLI) ToDo List system implemented in Python using OOP. It provides organized capabilities for managing **projects** and their associated **tasks** in memory.

### 🚀 Installation and Setup

This phase uses **Poetry** to manage dependencies and virtual environments.

#### 1. Prerequisites

- Python 3.10+
- Poetry (install via):

```bash
pip install poetry
````

#### 2. Dependency Installation

Navigate to the project's root directory (e.g. `todolist-oop-v2`):

```bash
# Install all required packages (dotenv, etc.)
poetry install

# Activate the virtual environment shell
poetry shell
```

#### 3. Running the Application

Once the Poetry shell is active, execute the Phase 1 main module:

```bash
python -m todolist_oop.main
```

---

### 📝 Usage Instructions (Phase 1 CLI)

Upon execution, the main menu will appear. All interactions are driven by selecting the corresponding number for the desired option.

#### Project & Task Menu Overview

| Menu Section           | Option Text                  | Capability (User Story) |
| ---------------------- | ---------------------------- | ----------------------- |
| **Project Management** | `1. Create a new project`    | US-1                    |
|                        | `3. Edit a project`          | US-2                    |
|                        | `4. Delete a project`        | US-3                    |
| **Task Management**    | `1. Add a task to a project` | US-4                    |
|                        | `2. List tasks in a project` | US-9                    |
|                        | `3. Change a task's status`  | US-5                    |
|                        | `4. Edit a task's details`   | US-6                    |
|                        | `5. Delete a task`           | US-7                    |

---

### ✅ Comprehensive Test Cases (QA – Phase 1)

These tests ensure correct functionality and robust error handling across project and task operations (including input validation and invalid IDs).

#### 1. Project Management Tests

Use the main menu → **Project Management** to perform these scenarios.

| Step    | Menu / Operation                | Required Input                                            | Expected Outcome                                                             | Status / Notes      |
| ------- | ------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------- |
| **1.1** | Main: `1` → Project: `1`        | Name: `Alpha_Project` → Description: `Initial deployment` | **Success**: Project created. Note the project ID (`P_ID_1`).                | US-1                |
| **1.2** | Main: `1` → Project: `1`        | Name: **(Empty)**                                         | **❌ Error**: `Error: Project name cannot be empty.`                          | **AC (Empty Name)** |
| **1.3** | Main: `1` → Project: `3` (Edit) | Project ID: `99999999` (invalid)                          | **❌ Error**: `Error: Project with ID '99999999' not found.` Returns to menu. | **AC (Invalid ID)** |
| **1.4** | Main: `1` → Project: `3` (Edit) | Project ID: `P_ID_1` → New name: `Beta Project`           | **Success**: `Project 'Beta Project' updated successfully.`                  | US-2                |

---

#### 2. Task Management and Validation Tests

Use the noted project ID (`P_ID_1`) from step **1.1** for these tests.

| Step    | Menu / Operation                      | Required Input                                                                             | Expected Outcome                                                                                | Status / Notes                    |
| ------- | ------------------------------------- | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- | --------------------------------- |
| **2.1** | Main: `2` → Task: `1` (Add Task)      | Project ID: `P_ID_1` → Title: `T1` → Deadline: `2025-01-30`                                | **Success**: Task created. Note the task ID (`T_ID_1`).                                         | US-4                              |
| **2.2** | Main: `2` → Task: `1` (Add Task)      | Project ID: `P_ID_1` → Title: `T2` → Deadline: `30-01-2025`                                | **❌ Error**: `Error: Invalid deadline format. Please use YYYY-MM-DD.`                           | **AC (Date Format)**              |
| **2.3** | Main: `2` → Task: `2` (List Tasks)    | Project ID: `P_ID_1`                                                                       | **Success**: Displays `T1` with status `todo`.                                                  | US-9                              |
| **2.4** | Main: `2` → Task: `3` (Change Status) | Project ID: `P_ID_1` → Task ID: `99999999`                                                 | **❌ Error**: `Error: Task with ID '99999999' not found...` and returns to menu (no status ask). | **AC (Invalid Task ID - UX Fix)** |
| **2.5** | Main: `2` → Task: `3` (Change Status) | Project ID: `P_ID_1` → Task ID: `T_ID_1` → New status: `doing`                             | **Success**: `Task 'T1' status updated to 'doing'.`                                             | US-5                              |
| **2.6** | Main: `2` → Task: `4` (Edit Task)     | Project ID: `P_ID_1` → Task ID: `T_ID_1` → New deadline: `2025-10-17` → New status: `done` | **Success**: `Task 'T1' updated successfully.`                                                  | US-6                              |

---

#### 3. UX and Final Deletion Scenarios

| Step    | Menu / Operation                          | Required Input                                 | Expected Outcome                                                                    | Status / Notes            |
| ------- | ----------------------------------------- | ---------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------- |
| **3.1** | Main: `1` → Project: `1` (Create Project) | Name: `Empty_P` (for testing an empty project) | **Success**: Project created. Note project ID (`P_ID_E`).                           | US-1                      |
| **3.2** | Main: `2` → Task: `4` (Edit Task)         | Project ID: `P_ID_E`                           | Shows `Project 'Empty_P' has no tasks.` and returns to menu (no Task ID requested). | **AC (Empty Project UX)** |
| **3.3** | Main: `2` → Task: `5` (Delete Task)       | Project ID: `P_ID_1` → Task ID: `T_ID_1`       | **Success**: `Task 'T1' was successfully deleted...`                                | US-7                      |
| **3.4** | Main: `1` → Project: `4` (Delete Project) | Project ID: `P_ID_E`                           | **Success**: `Project 'Empty_P' and all its tasks were deleted successfully.`       | US-3                      |
| **3.5** | Main: `0` (Exit)                          | –                                              | `Goodbye!`                                                                          | Application exit          |

---

## Phase 2 – RDB + Scheduling

This phase is a continuation of **ToDoList-OOP-python-phase1**.

All user stories and validation rules from Phase 1 are preserved, but the app now:

* Persists data in **PostgreSQL** instead of in-memory lists
* Uses **SQLAlchemy** and **Alembic** for ORM and migrations
* Follows a layered architecture (**models → repositories → services → CLI**)
* Adds **automatic closing of overdue tasks** via:

  * A one-shot CLI command
  * A long-running scheduler (for development)
  * A real **cron job** (for production-like scheduling)

### 🧱 Architecture Overview (Phase 2)

**Package layout (Phase 2):**

* `app/db/`

  * `session.py` – creates the SQLAlchemy engine and `SessionLocal` from `DATABASE_URL` (via `python-dotenv`)
  * `base.py` – `Base` declarative class
* `app/models/`

  * `project.py` – `Project` SQLAlchemy model
  * `task.py` – `Task` SQLAlchemy model

    * `deadline` (optional `DATE`)
    * `closed_at` (`DATETIME`, set when task becomes `done`)
    * `is_overdue` property (deadline vs today / `closed_at`)
* `app/repositories/`

  * `project_repository.py` – `ProjectRepository` / `SqlAlchemyProjectRepository`
  * `task_repository.py` – `TaskRepository` / `SqlAlchemyTaskRepository`
* `app/services/`

  * `project_service.py` – business rules for projects (names, limits, uniqueness)
  * `task_service.py` – business rules for tasks (limits, validation, overdue handling)
* `app/cli/console.py` – main interactive CLI (menus, input parsing, printing)
* `app/main.py` – CLI entry point (`python -m app.main`)
* `app/commands/`

  * `autoclose_overdue.py` – one-shot command to close all overdue tasks
  * `schedule_autoclose.py` – development scheduler using the `schedule` library
* `alembic/` – migrations and configuration for DB schema

---

## Phase 3 – FastAPI Web API (CLI Deprecation & RESTful API)

Phase 3 replaces the CLI as the **primary interface** with a **FastAPI-based Web API**, while reusing the existing **Service/Repository** domain logic from Phase 2.

The legacy CLI is still available but **deprecated**. All new features and integrations should go through the Web API.

### 1. How to Run the Web API

```bash
# From the project root
poetry install
poetry run uvicorn phase3_api.api_main:app --reload
```

* Base URL: `http://127.0.0.1:8000`
* API base path (versioned): `http://127.0.0.1:8000/api/v1`
* Interactive API docs (Swagger): `http://127.0.0.1:8000/docs`
* Alternative docs (ReDoc): `http://127.0.0.1:8000/redoc`

---

### 2. CLI Deprecation (Deprecation Notice)

The original CLI from Phase 1–2 is still present for backward compatibility, but it is **officially deprecated**:

* Deprecation is *not* an immediate removal.
* The CLI still runs and works, but it is **no longer the primary interface**.
* All new capabilities are exposed only via the FastAPI Web API.
* The CLI may be completely removed in a future phase/version.

**CLI entry point (Phase 2 style):**

```bash
poetry run python -m app.main
```

When executed, the CLI prints a deprecation warning and directs the user to the Web API:

* “The CLI interface is deprecated and will be removed in a future version.”
* “Use the FastAPI-based Web API instead.”

This matches the required **Deprecation Notice** and **Migration Phase** from the course specification.

---

### 3. Architecture & Layered Design (Controller → Service → Repository)

The Web API is implemented in a layered, testable architecture:

* **Controllers (FastAPI routers)** – HTTP layer only:

  * Located in `phase3_api/api/controllers/`
  * Responsible for:

    * Request/response mapping (Pydantic models)
    * Status codes and HTTP errors (`HTTPException`)
    * Dependency injection of `Service` objects

* **Services (Domain / Business Logic)**:

  * Located in `phase3_api/services/`
  * Implement all rules and constraints from Phase 1–2:

    * Task and project validation
    * Maximum tasks per project
    * Status transitions (`todo → doing → done`)
    * Handling overdue tasks
  * Services call repositories; they never touch CLI / HTTP directly.

* **Repositories (Data Access Layer)**:

  * Located in `phase3_api/repositories/`
  * Wrap SQLAlchemy operations:

    * `SqlAlchemyProjectRepository`
    * `SqlAlchemyTaskRepository`
  * Responsible only for persistence, not business rules.

Controllers depend on **Services**, which depend on **Repositories**.
There is no direct Controller → DB coupling.

---

### 4. API Versioning & Routing Structure

All API endpoints are grouped under a **versioned prefix**:

```python
# phase3_api/api/routers.py
api_router = APIRouter(prefix="/api/v1")

api_router.include_router(
    projects_controller.router,
    prefix="/projects",
    tags=["projects"],
)

api_router.include_router(
    tasks_controller.router,
    prefix="/tasks",
    tags=["tasks"],
)
```

Resulting URLs:

* Projects: `/api/v1/projects/...`
* Tasks: `/api/v1/tasks/...`

This provides:

* Clear separation of concerns (projects vs tasks)
* A stable contract for clients
* Room for future versions (e.g., `/api/v2`) without breaking existing clients

---

### 5. Endpoints Overview

#### 5.1 Projects

**Base path:** `/api/v1/projects`

| Method | Path                    | Description                |
| ------ | ----------------------- | -------------------------- |
| GET    | `/api/v1/projects/`     | List all projects          |
| POST   | `/api/v1/projects/`     | Create a new project       |
| GET    | `/api/v1/projects/{id}` | Get a single project by ID |
| PATCH  | `/api/v1/projects/{id}` | Partially update a project |
| DELETE | `/api/v1/projects/{id}` | Delete a project by ID     |

**Project creation request:**

```json
{
  "name": "My Project",
  "description": "Optional description (<= 150 chars)"
}
```

**Constraints:**

* `name`: required, `1–30` characters
* `description`: optional, `<= 150` characters

**Project PATCH (partial update) example:**

```json
{
  "name": "Renamed Project"
}
```

All fields in `ProjectUpdateRequest` are **optional**.
If a field is omitted, its existing value is preserved. This matches the semantics of HTTP **PATCH** (partial update), not a full replace (**PUT**).

---

#### 5.2 Tasks

**Base path:** `/api/v1/tasks`

| Method | Path                              | Description                                 |
| ------ | --------------------------------- | ------------------------------------------- |
| GET    | `/api/v1/tasks/?project_id={pid}` | List tasks for a given project              |
| POST   | `/api/v1/tasks/`                  | Create a new task in a project              |
| POST   | `/api/v1/tasks/close-overdue`     | Close overdue tasks (global or per project) |
| GET    | `/api/v1/tasks/{id}`              | Get a single task by ID                     |
| PATCH  | `/api/v1/tasks/{id}`              | Partially update a task                     |
| DELETE | `/api/v1/tasks/{id}`              | Delete a task by ID                         |

**List tasks for a project:**

```http
GET /api/v1/tasks/?project_id=1
```

* If the project exists but has no tasks → `200 OK` + `[]`
* If the project does not exist → `404 Not Found`

**Create new task:**

```json
{
  "project_id": 1,
  "title": "Implement Phase 3",
  "description": "FastAPI Web API",
  "deadline": "2025-12-31"
}
```

**Constraints:**

* `title`: required, `1–30` characters
* `description`: optional, `<= 150` characters
* `deadline`: optional ISO date
* `status`: must be one of `"todo"`, `"doing"`, `"done"` (handled in Service)

**Task PATCH (partial update) examples:**

* Change only the title:

  ```json
  {
    "title": "Renamed Task"
  }
  ```

* Mark as done:

  ```json
  {
    "status": "done"
  }
  ```

All fields in `TaskUpdateRequest` are optional.
The service updates only those fields that are provided (non-`None`).

---

### 6. Overdue Tasks (Auto-Close Behavior)

The domain rule “close overdue tasks” from Phase 2 is preserved and implemented in the **TaskService**.

* A task is considered **overdue** based on the `Task.is_overdue` flag / property (derived from `deadline` and current time).
* Only tasks that are **not already `"done"`** are affected.

The Web API exposes this behavior explicitly via a POST endpoint:

```http
POST /api/v1/tasks/close-overdue
POST /api/v1/tasks/close-overdue?project_id={pid}
```

* If `project_id` is provided:

  * Overdue tasks only for that project are closed.
* If `project_id` is omitted:

  * Overdue tasks for **all projects** are closed.

**Response example:**

```json
{
  "closed_count": 3,
  "scope": "project",
  "project_id": 1
}
```

This is a **state-changing** operation and is therefore implemented as `POST`.
In contrast, `GET /api/v1/tasks` remains a **pure read-only** operation with no side effects.

---

### 7. Validation & Pydantic Models

All input and output payloads are defined via **Pydantic models**:

* Requests:

  * `ProjectCreateRequest`, `ProjectUpdateRequest`
  * `TaskCreateRequest`, `TaskUpdateRequest`
* Responses:

  * `ProjectResponse`
  * `TaskResponse`

Validation is enforced automatically by FastAPI:

* Empty or too-long titles/descriptions → `422 Unprocessable Entity`
* Invalid enum values for status → rejected in the Service layer with a `400` API error
* Missing required fields → `422` with detailed error messages

Response models are configured with `from_attributes=True` so that SQLAlchemy ORM objects are safely converted to clean JSON responses.

---

### 8. Sync vs Async

* The project uses **synchronous** SQLAlchemy sessions.
* All FastAPI endpoints are implemented as **regular `def` functions**, not `async def`.
* This avoids mixing sync DB access with async endpoints and respects best practices:

  * `FastAPI (sync) → Service (sync) → Repository (sync) → DB`

If the data layer is migrated to an async driver in the future, the endpoints can be migrated to `async def` consistently.

---

## Final Summary

This repository demonstrates a full evolution:

* From **simple OOP CLI** → **DB-backed layered architecture** → **RESTful Web API**
* Reuse of domain logic across multiple interfaces (CLI & Web API)
* Clean separation of concerns:

  * Controller → Service → Repository
* Proper usage of:

  * Pydantic for validation
  * FastAPI for Web APIs
  * SQLAlchemy + Alembic for persistence and migrations

In **Phase 3**, the recommended way to interact with the system is through the **FastAPI Web API** (`/api/v1/...`).
The CLI remains available but is officially **deprecated**.

```
::contentReference[oaicite:0]{index=0}
```
