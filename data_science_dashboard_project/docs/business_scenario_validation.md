# Business Scenario Validation

## Scenario Summary

The dashboard is designed for manufacturing managers who need to:
- Monitor productivity signals at employee and team levels.
- View likelihood of recruitment risk for employees and teams.

## Requirement-to-Implementation Mapping

1. Single employee productivity visualization
- Implemented in report/dashboard.py route /employee/{employee_id}
- Displays total positive and negative events plus event history table

2. Team productivity visualization
- Implemented in report/dashboard.py route /team/{team_id}
- Displays team-level totals and event history table

3. Employee likelihood of recruitment
- Implemented in report/dashboard.py using report/utils.py function predict_recruitment_likelihood
- Uses model.pkl if available; otherwise uses deterministic fallback logic

4. Team average likelihood of recruitment
- Implemented in report/dashboard.py using report/utils.py function average_team_recruitment_likelihood

## Technical Scenario Validation

1. SQL queries for critical datasets
- Implemented in python-package/employee_events/queries.py in QueryBase, Employee, and Team classes

2. Python package API
- Package implemented under python-package/employee_events
- Importable classes and functions are exported in python-package/employee_events/__init__.py

3. FastHTML dashboard extension
- Existing FastHTML components are extended from report/src/dashboard_components.py
- App and routes are defined in report/dashboard.py

4. OOP extension and customization
- Dashboard classes use inheritance: EmployeeDashboard, TeamDashboard, EventDashboard subclass DashboardBase
- Query classes use inheritance: Employee and Team subclass QueryBase

## Sample Data Coverage

The sample_data folder includes:
- team.csv
- employee.csv
- employee_events.csv
- notes.csv

Database seeding logic reads these files in python-package/employee_events/db_setup.py.

## Verification Steps

1. Install dependencies and package.
2. Initialize database with create_database().
3. Run pytest on tests/test_employee_events.py.
4. Launch dashboard and confirm:
- /employee/{employee_id} shows productivity and recruitment likelihood.
- /team/{team_id} shows aggregate productivity and average recruitment likelihood.
