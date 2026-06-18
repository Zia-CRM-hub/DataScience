# Employee Events Dashboard

## Business Scenario

- You are supporting a manufacturing company that wants to reduce loss of top employees to competitors.
- Managers capture positive and negative performance events through a data-entry form.
- A machine learning model predicts employee recruitment risk.
- The dashboard must let managers monitor both productivity and recruitment likelihood for one employee or a team.

## Technical Scenario

The project implements the required technical architecture:

1. SQL queries for business-critical datasets via the Employee and Team query APIs.
2. A reusable Python package so users do not write raw SQL manually.
3. A FastHTML dashboard built from the existing component framework.
4. OOP subclassing in both the query layer and dashboard layer.

## Features

- SQLite database for team, employee, events, and notes data.
- Python package API in python-package/employee_events.
- SQL decorator and mixin support in sql_execution.py.
- FastHTML dashboard with employee and team routes.
- Recruitment likelihood display for employee and team views.
- CSV-based sample data seeding for reproducible demos.
- Pytest and GitHub Actions test workflow.

## Project Structure

data_science_dashboard_project/
- python-package/
    - employee_events/
        - __init__.py
        - db_setup.py
        - sql_execution.py
        - queries.py
        - employee_events.db
    - setup.py
- report/
    - src/dashboard_components.py
    - utils.py
    - dashboard.py
- sample_data/
    - team.csv
    - employee.csv
    - employee_events.csv
    - notes.csv
- tests/test_employee_events.py
- docs/business_scenario_validation.md
- requirements.txt
- README.md

## Installation

1. Install dependencies.

```bash
python -m pip install -r requirements.txt
```

2. Install the package.

```bash
python -m pip install -e python-package
```

3. Initialize database from sample data.

```bash
python -c "from employee_events import create_database; create_database()"
```

## Run Dashboard

```bash
python report/dashboard.py
```

Dashboard URL: http://127.0.0.1:8000

## Run Tests

```bash
python -m pytest tests -v
```

## Business Requirement Verification

Employee-level requirement:
- Route /employee/{employee_id} shows positive and negative event totals and predicted recruitment likelihood.

Team-level requirement:
- Route /team/{team_id} shows aggregate event totals and average recruitment likelihood.

Detailed validation mapping is documented in docs/business_scenario_validation.md.
