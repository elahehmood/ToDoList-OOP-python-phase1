# 📋 ToDoList-OOP-python-phase1

This is an advanced, Command Line Interface (CLI)-based ToDo List management system implemented in Python using an Object-Oriented Programming (OOP) approach. It provides organized capabilities for managing projects and their associated tasks.

## 🚀 Installation and Setup

This project uses **Poetry** to manage dependencies and virtual environments, ensuring clean and reproducible installations.

### 1\. Prerequisites

  * Python 3.10+
  * Poetry (Install via: `pip install poetry`)

### 2\. Dependency Installation

Navigate to the project's root directory (`todolist-oop-v2`):

```bash
# Install all required packages (dotenv, etc.)
poetry install

# Activate the virtual environment shell
poetry shell
```

### 3\. Running the Application

Once the Poetry shell is active, execute the main module:

```bash
python -m todolist_oop.main
```

## 📝 Usage Instructions

Upon execution, the main menu will appear. All interactions are driven by selecting the corresponding number for the desired option.

| Menu | Options | Capability (User Story) |
| :--- | :--- | :--- |
| **Project Management** | `1. Create a new project` | US-1 |
| | `3. Edit a project` | US-2 |
| | `4. Delete a project` | US-3 |
| **Task Management** | `1. Add a task to a project` | US-4 |
| | `3. Change a task's status` | US-5 |
| | `4. Edit a task's details` | US-6 |
| | `5. Delete a task` | US-7 |
| | `2. List tasks in a project` | US-9 |

-----

## ✅ Comprehensive Test Cases (QA)

These tests are designed to ensure the project's correct functionality and robust error handling across all scenarios (including input validation and invalid IDs).

### 1\. Project Management Tests

| Step | Menu/Operation | Required Input | Expected Outcome | Status |
| :--- | :--- | :--- | :--- | :--- |
| **1.1** | Main: **1** $\rightarrow$ Project: **1** | Name: `Alpha_Project` $\rightarrow$ Description: `Initial deployment` | **Success**: Note the project ID (`P_ID_1`). | US-1 |
| **1.2** | Main: **1** $\rightarrow$ Project: **1** | Name: **(Empty)** | **❌ Error**: `Error: Project name cannot be empty.` | **AC (Empty Name)** |
| **1.3** | Main: **1** $\rightarrow$ Project: **3** | Project ID: `99999999` (Invalid) | **❌ Error**: `Error: Project with ID '99999999' not found.` Returns to menu. | **AC (Invalid ID)** |
| **1.4** | Main: **1** $\rightarrow$ Project: **3** | Project ID: `P_ID_1` $\rightarrow$ New Name: `Beta Project` | **Success**: `Project 'Beta Project' updated successfully.` | US-2 |

### 2\. Task Management and Validation Tests

Use the noted project ID (`P_ID_1`) for the tasks in this section.

| Step | Menu/Operation | Required Input | Expected Outcome | Status |
| :--- | :--- | :--- | :--- | :--- |
| **2.1** | Main: **2** $\rightarrow$ Task: **1** | Project ID: `P_ID_1` $\rightarrow$ Title: `T1` $\rightarrow$ Deadline: `2025-01-30` | **Success**: Note the task ID (`T_ID_1`). | US-4 |
| **2.2** | Main: **2** $\rightarrow$ Task: **1** | Project ID: `P_ID_1` $\rightarrow$ Title: `T2` $\rightarrow$ Deadline: `30-01-2025` | **❌ Error**: `Error: Invalid deadline format. Please use YYYY-MM-DD.` | **AC (Date Format)** |
| **2.3** | Main: **2** $\rightarrow$ Task: **2** | Project ID: `P_ID_1` | **Success**: Displays `T1` with status `todo`. | US-9 |
| **2.4** | Main: **2** $\rightarrow$ Task: **3** (Change Status) | Project ID: `P_ID_1` $\rightarrow$ Task ID: `99999999` | **❌ Error**: `Error: Task with ID '99999999' not found...` **(Immediately returns to menu without asking for new status)**. | **AC (Invalid Task ID - UX Fix)** |
| **2.5** | Main: **2** $\rightarrow$ Task: **3** | Project ID: `P_ID_1` $\rightarrow$ Task ID: `T_ID_1` $\rightarrow$ New Status: `doing` | **Success**: `Task 'T1' status updated to 'doing'.` | US-5 |
| **2.6** | Main: **2** $\rightarrow$ Task: **4** (Edit Task) | Project ID: `P_ID_1` $\rightarrow$ Task ID: `T_ID_1` $\rightarrow$ New Deadline: `2025-10-17` $\rightarrow$ New Status: `done` | **Success**: `Task 'T1' updated successfully.` | US-6 |

### 3\. UX and Final Deletion Scenarios

| Step | Menu/Operation | Required Input | Expected Outcome | Status |
| :--- | :--- | :--- | :--- | :--- |
| **3.1** | Main: **1** $\rightarrow$ Project: **1** | Name: `Empty_P` (For empty project test) | **Success**: Note the project ID (`P_ID_E`). | US-1 |
| **3.2** | Main: **2** $\rightarrow$ Task: **4** (Edit Task) | Project ID: `P_ID_E` | `Project 'Empty_P' has no tasks.` **(Immediately returns to menu without asking for Task ID or details)**. | **AC (Empty Project UX)** |
| **3.3** | Main: **2** $\rightarrow$ Task: **5** | Project ID: `P_ID_1` $\rightarrow$ Task ID: `T_ID_1` | **Success**: `Task 'T1' was successfully deleted...` | US-7 |
| **3.4** | Main: **1** $\rightarrow$ Project: **4** | Project ID: `P_ID_E` | **Success**: `Project 'Empty_P' and all its tasks were deleted successfully.` | US-3 |
| **3.5** | Main: **0** | - | `Goodbye!` | (Exit) |

-----

## ⚠️ Final Reminder

Ensure that you execute the application within the **Poetry virtual environment** (after running `poetry shell`) to avoid `ModuleNotFoundError` issues.
