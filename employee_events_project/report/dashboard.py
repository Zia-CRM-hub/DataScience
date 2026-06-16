"""
FastHTML Dashboard Application for Employee Events System
"""

from fasthtml.common import *
from pathlib import Path
import sys

# Add python-package to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "python-package"))

# Import classes from the employee_events package
from employee_events import Employee, Team, create_database
from employee_events.db_setup import get_db_path

# Import dashboard components
from src.dashboard_components import DashboardBase, EmployeeDashboard, TeamDashboard, EventDashboard

# Initialize the database
db_path = get_db_path()
if not db_path.exists():
    create_database()

# Initialize FastHTML app
app, rt = fast_app(
    title="Employee Events Dashboard",
    css="style.css"
)

# Initialize dashboard components
base_dashboard = DashboardBase()
employee_dashboard = EmployeeDashboard()
team_dashboard = TeamDashboard()
event_dashboard = EventDashboard()

# Instantiate query classes
employee_queries = Employee()
team_queries = Team()


@rt("/")
def index():
    """Index route - Main dashboard"""
    return Html(
        Head(
            Title("Employee Events Dashboard"),
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
        ),
        Body(
            base_dashboard.render_header(),
            base_dashboard.render_nav(),
            Main(
                Div(
                    H2("Welcome to Employee Events Dashboard"),
                    P("Select an option from the navigation menu to get started."),
                    cls="welcome-section"
                ),
                cls="main-content"
            ),
            base_dashboard.render_footer(),
        )
    )


@rt("/employee")
def employee():
    """Employee list route"""
    employees = employee_queries.get_all_employees()
    
    return Html(
        Head(
            Title("Employees - Employee Events Dashboard"),
            Meta(charset="utf-8"),
        ),
        Body(
            base_dashboard.render_header(),
            base_dashboard.render_nav(),
            Main(
                employee_dashboard.render_employee_list(employees or []),
                cls="main-content"
            ),
            base_dashboard.render_footer(),
        )
    )


@rt("/employee/{employee_id}")
def employee_detail(employee_id: int):
    """Employee detail route"""
    employee = employee_queries.get_employee(employee_id)
    events = employee_queries.get_employee_events(employee_id)
    notes = employee_queries.get_employee_notes(employee_id)
    summary = employee_queries.get_employee_event_summary(employee_id)
    
    if not employee:
        return Html(
            Head(Title("Employee Not Found")),
            Body(
                base_dashboard.render_header(),
                base_dashboard.render_nav(),
                Main(P(f"Employee {employee_id} not found"), cls="main-content"),
                base_dashboard.render_footer(),
            )
        )
    
    emp = employee[0]
    total_positive = summary[0][0] if summary and summary[0][0] else 0
    total_negative = summary[0][1] if summary and summary[0][1] else 0
    
    return Html(
        Head(Title(f"{emp[1]} {emp[2]} - Employee Details")),
        Body(
            base_dashboard.render_header(),
            base_dashboard.render_nav(),
            Main(
                Div(
                    H2(f"{emp[1]} {emp[2]}"),
                    P(f"Employee ID: {emp[0]}"),
                    P(f"Team: {emp[4]}"),
                    Div(
                        H3("Summary"),
                        P(f"Total Positive Events: {total_positive}"),
                        P(f"Total Negative Events: {total_negative}"),
                        cls="summary-section"
                    ),
                    Div(
                        H3("Recent Events"),
                        event_dashboard.render_events_table(events or []),
                        cls="events-section"
                    ),
                    cls="employee-detail"
                ),
                cls="main-content"
            ),
            base_dashboard.render_footer(),
        )
    )


@rt("/team")
def team():
    """Team list route"""
    teams = team_queries.get_all_teams()
    
    return Html(
        Head(
            Title("Teams - Employee Events Dashboard"),
            Meta(charset="utf-8"),
        ),
        Body(
            base_dashboard.render_header(),
            base_dashboard.render_nav(),
            Main(
                team_dashboard.render_team_list(teams or []),
                cls="main-content"
            ),
            base_dashboard.render_footer(),
        )
    )


@rt("/team/{team_id}")
def team_detail(team_id: int):
    """Team detail route"""
    team = team_queries.get_team(team_id)
    employees = team_queries.get_team_size(team_id)
    events = team_queries.get_team_events(team_id)
    summary = team_queries.get_team_summary(team_id)
    
    if not team:
        return Html(
            Head(Title("Team Not Found")),
            Body(
                base_dashboard.render_header(),
                base_dashboard.render_nav(),
                Main(P(f"Team {team_id} not found"), cls="main-content"),
                base_dashboard.render_footer(),
            )
        )
    
    tm = team[0]
    summary_data = summary[0] if summary else None
    
    return Html(
        Head(Title(f"{tm[1]} - Team Details")),
        Body(
            base_dashboard.render_header(),
            base_dashboard.render_nav(),
            Main(
                Div(
                    H2(tm[1]),
                    P(f"Team ID: {tm[0]}"),
                    P(f"Shift: {tm[2]}"),
                    P(f"Manager: {tm[3]}"),
                    Div(
                        H3("Summary"),
                        P(f"Employees: {summary_data[2] if summary_data else 0}"),
                        P(f"Total Positive Events: {summary_data[3] if summary_data else 0}"),
                        P(f"Total Negative Events: {summary_data[4] if summary_data else 0}"),
                        cls="summary-section"
                    ),
                    Div(
                        H3("Recent Events"),
                        event_dashboard.render_events_table(events or []),
                        cls="events-section"
                    ),
                    cls="team-detail"
                ),
                cls="main-content"
            ),
            base_dashboard.render_footer(),
        )
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
