"""
Query classes for Employee Events database
"""

import pandas as pd
from .sql_execution import SQLMixin

class QueryBase(SQLMixin):
    """
    Base class for database queries that can be used by both employees and teams.
    Uses SQLMixin for automatic database connection handling.
    """
    
    def get_all_records(self, table_name):
        """Get all records from a specific table"""
        query = f"SELECT * FROM {table_name}"
        return self.execute_query(query)
    
    def get_record_by_id(self, table_name, id_column, id_value):
        """Get a specific record by ID"""
        query = f"SELECT * FROM {table_name} WHERE {id_column} = ?"
        return self.execute_query(query, (id_value,))
    
    def get_count(self, table_name):
        """Get the count of records in a table"""
        query = f"SELECT COUNT(*) FROM {table_name}"
        result = self.execute_query(query)
        return result[0][0] if result else 0
    
    def get_records_by_team(self, table_name, team_id):
        """Get records from a table for a specific team"""
        query = f"SELECT * FROM {table_name} WHERE team_id = ?"
        return self.execute_query(query, (team_id,))


class Employee(QueryBase):
    """
    Query class for employee-specific database queries.
    Inherits common queries from QueryBase.
    """
    
    def names(self):
        """Get all employee names as a DataFrame"""
        query = "SELECT employee_id, first_name || ' ' || last_name AS full_name FROM employee"
        return self.read_sql(query)
    
    def username(self, employee_id):
        """Get employee name by ID"""
        query = "SELECT first_name || ' ' || last_name AS full_name FROM employee WHERE employee_id = ?"
        result = self.execute_query(query, (employee_id,))
        return result[0][0] if result else None
    
    def event_counts(self, employee_id):
        """Get event counts by date for an employee"""
        query = """
            SELECT event_date, positive_events, negative_events 
            FROM employee_events 
            WHERE employee_id = ?
            ORDER BY event_date DESC
        """
        return self.read_sql(query, (employee_id,))
    
    def get_employee(self, employee_id):
        """Get employee details by ID"""
        query = """
            SELECT e.employee_id, e.first_name, e.last_name, e.team_id, t.team_name
            FROM employee e
            JOIN team t ON e.team_id = t.team_id
            WHERE e.employee_id = ?
        """
        return self.execute_query(query, (employee_id,))
    
    def get_all_employees(self):
        """Get all employees with their team information"""
        query = """
            SELECT e.employee_id, e.first_name, e.last_name, e.team_id, t.team_name
            FROM employee e
            JOIN team t ON e.team_id = t.team_id
            ORDER BY e.last_name, e.first_name
        """
        return self.execute_query(query)
    
    def get_employee_events(self, employee_id):
        """Get all events for a specific employee"""
        query = """
            SELECT event_date, employee_id, team_id, positive_events, negative_events
            FROM employee_events
            WHERE employee_id = ?
            ORDER BY event_date DESC
        """
        return self.execute_query(query, (employee_id,))
    
    def get_employee_notes(self, employee_id):
        """Get all notes for a specific employee"""
        query = """
            SELECT note_date, note
            FROM notes
            WHERE employee_id = ?
            ORDER BY note_date DESC
        """
        return self.execute_query(query, (employee_id,))
    
    def get_employee_by_team(self, team_id):
        """Get all employees in a specific team"""
        query = """
            SELECT e.employee_id, e.first_name, e.last_name, e.team_id, t.team_name
            FROM employee e
            JOIN team t ON e.team_id = t.team_id
            WHERE e.team_id = ?
            ORDER BY e.last_name, e.first_name
        """
        return self.execute_query(query, (team_id,))
    
    def get_employee_event_summary(self, employee_id):
        """Get summary of positive and negative events for an employee"""
        query = """
            SELECT 
                SUM(positive_events) as total_positive,
                SUM(negative_events) as total_negative,
                COUNT(*) as total_events
            FROM employee_events
            WHERE employee_id = ?
        """
        return self.execute_query(query, (employee_id,))


class Team(QueryBase):
    """
    Query class for team-specific database queries.
    Inherits common queries from QueryBase.
    """
    
    def names(self):
        """Get all team names as a DataFrame"""
        query = "SELECT team_id, team_name FROM team"
        return self.read_sql(query)
    
    def username(self, team_id):
        """Get team name by ID"""
        query = "SELECT team_name FROM team WHERE team_id = ?"
        result = self.execute_query(query, (team_id,))
        return result[0][0] if result else None
    
    def event_counts(self, team_id):
        """Get aggregated event counts for a team"""
        query = """
            SELECT 
                ee.event_date,
                SUM(ee.positive_events) as total_positive,
                SUM(ee.negative_events) as total_negative
            FROM employee_events ee
            WHERE ee.team_id = ?
            GROUP BY ee.event_date
            ORDER BY ee.event_date DESC
        """
        return self.read_sql(query, (team_id,))
    
    def get_team(self, team_id):
        """Get team details by ID"""
        query = """
            SELECT team_id, team_name, shift, manager_name
            FROM team
            WHERE team_id = ?
        """
        return self.execute_query(query, (team_id,))
    
    def get_all_teams(self):
        """Get all teams"""
        query = """
            SELECT team_id, team_name, shift, manager_name
            FROM team
            ORDER BY team_name
        """
        return self.execute_query(query)
    
    def get_team_size(self, team_id):
        """Get the number of employees in a team"""
        query = """
            SELECT COUNT(*) FROM employee WHERE team_id = ?
        """
        result = self.execute_query(query, (team_id,))
        return result[0][0] if result else 0
    
    def get_team_events(self, team_id):
        """Get all events for a specific team"""
        query = """
            SELECT event_date, employee_id, team_id, positive_events, negative_events
            FROM employee_events
            WHERE team_id = ?
            ORDER BY event_date DESC
        """
        return self.execute_query(query, (team_id,))
    
    def get_team_summary(self, team_id):
        """Get summary statistics for a team"""
        query = """
            SELECT 
                t.team_id,
                t.team_name,
                COUNT(DISTINCT e.employee_id) as employee_count,
                SUM(ee.positive_events) as total_positive_events,
                SUM(ee.negative_events) as total_negative_events
            FROM team t
            LEFT JOIN employee e ON t.team_id = e.team_id
            LEFT JOIN employee_events ee ON e.employee_id = ee.employee_id
            WHERE t.team_id = ?
            GROUP BY t.team_id, t.team_name
        """
        return self.execute_query(query, (team_id,))
    
    def get_team_notes(self, team_id):
        """Get all notes for a team"""
        query = """
            SELECT n.employee_id, e.first_name, e.last_name, n.note_date, n.note
            FROM notes n
            JOIN employee e ON n.employee_id = e.employee_id
            WHERE n.team_id = ?
            ORDER BY n.note_date DESC
        """
        return self.execute_query(query, (team_id,))
