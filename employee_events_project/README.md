# Employee Events Dashboard

## Project Overview
A full-stack web application for managing and analyzing employee events using Python, SQLite, and FastHTML.

## Features
- **SQL Database**: SQLite database with employee, team, events, and notes tables
- **Python Package**: Reusable `employee_events` package with database query classes
- **Decorator/Mixin Pattern**: Custom SQL execution decorator and mixin for database operations
- **FastHTML Dashboard**: Interactive web dashboard with employee and team views
- **Test Suite**: Comprehensive pytest tests for database validation
- **CI/CD**: GitHub Actions for automated testing on commits

## Project Structure

```
employee_events_project/
├── python-package/
│   ├── employee_events/
│   │   ├── __init__.py              # Package initialization
│   │   ├── db_setup.py              # Database creation and schema
│   │   ├── sql_execution.py         # Decorator and SQLMixin for database operations
│   │   ├── queries.py               # QueryBase, Employee, and Team classes
│   │   └── employee_events.db       # SQLite database
│   └── setup.py                     # Package setup configuration
├── report/
│   ├── src/
│   │   └── dashboard_components.py  # FastHTML dashboard components
│   ├── utils.py                     # Utility functions with pathlib paths
│   └── dashboard.py                 # Main FastHTML application
├── tests/
│   └── test_employee_events.py      # Pytest test functions
├── .github/
│   └── workflows/
│       └── tests.yml                # GitHub Actions workflow
├── requirements.txt                 # Project dependencies
└── README.md                        # This file
```

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install the Python Package
```bash
cd python-package
pip install -e .
```

### 3. Initialize the Database
```bash
python -c "from employee_events import create_database; create_database()"
```

## Usage

### Running the Dashboard
```bash
python report/dashboard.py
```

The dashboard will be available at `http://127.0.0.1:8000`

### Using the Query Classes

```python
from employee_events import Employee, Team

# Employee queries
emp = Employee()
all_employees = emp.get_all_employees()
employee = emp.get_employee(1)
events = emp.get_employee_events(1)

# Team queries
team = Team()
all_teams = team.get_all_teams()
team_data = team.get_team(1)
team_summary = team.get_team_summary(1)
```

### Using the SQL Decorator

```python
from employee_events import sql_query

@sql_query
def get_employees():
    return "SELECT * FROM employee"

employees = get_employees()
```

## Database Schema

### Team Table
- `team_id` (INTEGER, Primary Key)
- `team_name` (TEXT)
- `shift` (TEXT)
- `manager_name` (TEXT)

### Employee Table
- `employee_id` (INTEGER, Primary Key)
- `first_name` (TEXT)
- `last_name` (TEXT)
- `team_id` (INTEGER, Foreign Key)

### Employee Events Table
- `event_date` (TEXT)
- `employee_id` (INTEGER, Foreign Key)
- `team_id` (INTEGER, Foreign Key)
- `positive_events` (INTEGER)
- `negative_events` (INTEGER)

### Notes Table
- `employee_id` (INTEGER, Foreign Key, Part of Composite PK)
- `team_id` (INTEGER, Foreign Key, Part of Composite PK)
- `note_date` (TEXT, Part of Composite PK)
- `note` (TEXT)

## Running Tests

```bash
pytest tests/ -v
```

## Architecture Highlights

### SQL Execution Pattern
The project implements **both** decorator and mixin patterns:
- **Decorator**: `@sql_query` decorator for simple functions returning SQL strings
- **Mixin**: `SQLMixin` class for classes that need database operations

### Query Class Hierarchy
- `QueryBase`: Common queries for both employees and teams
- `Employee(QueryBase)`: Employee-specific queries
- `Team(QueryBase)`: Team-specific queries

### Dashboard Components
- `DashboardBase`: Base class with common rendering methods
- `EmployeeDashboard(DashboardBase)`: Employee-specific UI components
- `TeamDashboard(DashboardBase)`: Team-specific UI components
- `EventDashboard(DashboardBase)`: Event table rendering

## GitHub Actions
Tests run automatically on commits to the `main` branch using the GitHub Actions workflow defined in `.github/workflows/tests.yml`.

## Future Enhancements
- Add data visualization and charts
- Implement authentication
- Add employee event creation/editing features
- Deploy to cloud platform
- Add API endpoints for external integrations
