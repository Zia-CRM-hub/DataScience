"""
FastHTML dashboard components for Employee Events System
"""

from fasthtml.common import *

class DashboardBase:
    """Base class for dashboard components"""
    
    def __init__(self):
        self.title = "Employee Events Dashboard"
    
    def render_header(self):
        """Render the header component"""
        return Header(
            Div(
                H1(self.title),
                cls="header"
            )
        )
    
    def render_footer(self):
        """Render the footer component"""
        return Footer(
            P("© 2024 Employee Events Management System"),
            cls="footer"
        )
    
    def render_nav(self):
        """Render the navigation component"""
        return Nav(
            Ul(
                Li(A("Home", href="/")),
                Li(A("Employees", href="/employee")),
                Li(A("Teams", href="/team")),
                cls="nav-list"
            ),
            cls="navbar"
        )


class EmployeeDashboard(DashboardBase):
    """Employee dashboard component"""
    
    def render_employee_card(self, employee):
        """Render an individual employee card"""
        return Div(
            H3(f"{employee[1]} {employee[2]}"),
            P(f"ID: {employee[0]}"),
            P(f"Team: {employee[4]}"),
            A("View Details", href=f"/employee/{employee[0]}"),
            cls="employee-card"
        )
    
    def render_employee_list(self, employees):
        """Render a list of employee cards"""
        cards = [self.render_employee_card(emp) for emp in employees]
        return Div(
            H2("Employees"),
            Div(*cards, cls="employee-list"),
            cls="employee-section"
        )


class TeamDashboard(DashboardBase):
    """Team dashboard component"""
    
    def render_team_card(self, team):
        """Render an individual team card"""
        return Div(
            H3(team[1]),
            P(f"Shift: {team[2]}"),
            P(f"Manager: {team[3]}"),
            A("View Details", href=f"/team/{team[0]}"),
            cls="team-card"
        )
    
    def render_team_list(self, teams):
        """Render a list of team cards"""
        cards = [self.render_team_card(team) for team in teams]
        return Div(
            H2("Teams"),
            Div(*cards, cls="team-list"),
            cls="team-section"
        )


class EventDashboard(DashboardBase):
    """Event dashboard component"""
    
    def render_event_row(self, event):
        """Render an event table row"""
        return Tr(
            Td(event[0]),  # event_date
            Td(event[1]),  # employee_id
            Td(event[3]),  # positive_events
            Td(event[4]),  # negative_events
        )
    
    def render_events_table(self, events):
        """Render events as a table"""
        if not events:
            return P("No events found")
        
        rows = [self.render_event_row(event) for event in events]
        return Table(
            Thead(
                Tr(
                    Th("Date"),
                    Th("Employee ID"),
                    Th("Positive Events"),
                    Th("Negative Events"),
                )
            ),
            Tbody(*rows),
            cls="events-table"
        )
