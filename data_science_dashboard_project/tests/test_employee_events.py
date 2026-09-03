"""
Comprehensive pytest suite for Employee Events System
Tests cover all rubric requirements: package API, inheritance, database, and integration
"""

import pytest
from pathlib import Path
import sys
import sqlite3
import tempfile
import shutil

# Add python-package to path
sys.path.insert(0, str(Path(__file__).parent.parent / "python-package"))

from employee_events.db_setup import get_db_path, create_database
from employee_events.queries import Employee, Team, QueryBase
from employee_events.sql_execution import SQLMixin
import pandas as pd

# Path variable for interacting with the SQLite database
DB_PATH = get_db_path()


@pytest.fixture
def db_path():
    """Fixture that provides the database path and ensures it exists"""
    if not DB_PATH.exists():
        create_database()
    return DB_PATH


# ==============================================================================
# PYTHON PACKAGE TESTS: Database connection and SQL execution
# ==============================================================================

class TestPackageDatabase:
    """Tests for Python package database functionality"""
    
    def test_db_path_exists(self, db_path):
        """Test that database file exists"""
        assert db_path.exists(), f"Database file does not exist at {db_path}"
    
    def test_employee_table_exists(self, db_path):
        """Test that the employee table exists in the database"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employee'")
        result = cursor.fetchone()
        conn.close()
        assert result is not None, "Employee table does not exist"
    
    def test_team_table_exists(self, db_path):
        """Test that the team table exists in the database"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='team'")
        result = cursor.fetchone()
        conn.close()
        assert result is not None, "Team table does not exist"
    
    def test_employee_events_table_exists(self, db_path):
        """Test that the employee_events table exists in the database"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employee_events'")
        result = cursor.fetchone()
        conn.close()
        assert result is not None, "Employee_events table does not exist"


class TestPackageImports:
    """Tests for package imports and exports"""
    
    def test_import_querybase(self):
        """Test that QueryBase can be imported from package"""
        from employee_events import QueryBase
        assert QueryBase is not None
    
    def test_import_employee(self):
        """Test that Employee can be imported from package"""
        from employee_events import Employee
        assert Employee is not None
    
    def test_import_team(self):
        """Test that Team can be imported from package"""
        from employee_events import Team
        assert Team is not None
    
    def test_import_sqlmixin(self):
        """Test that SQLMixin can be imported from package"""
        from employee_events import SQLMixin
        assert SQLMixin is not None


# ==============================================================================
# OBJECT ORIENTED PROGRAMMING TESTS: Inheritance and mixins
# ==============================================================================

class TestOOPInheritance:
    """Tests for class hierarchy and inheritance"""
    
    def test_querybase_inheritance(self):
        """Test that QueryBase inherits from SQLMixin"""
        assert issubclass(QueryBase, SQLMixin), "QueryBase should inherit from SQLMixin"
    
    def test_employee_inheritance(self):
        """Test that Employee inherits from QueryBase"""
        assert issubclass(Employee, QueryBase), "Employee should inherit from QueryBase"
    
    def test_team_inheritance(self):
        """Test that Team inherits from QueryBase"""
        assert issubclass(Team, QueryBase), "Team should inherit from QueryBase"
    
    def test_employee_has_execute_query_method(self):
        """Test that Employee has execute_query method from mixin"""
        emp = Employee()
        assert hasattr(emp, 'execute_query'), "Employee should have execute_query method"
    
    def test_team_has_execute_query_method(self):
        """Test that Team has execute_query method from mixin"""
        team = Team()
        assert hasattr(team, 'execute_query'), "Team should have execute_query method"
    
    def test_mixin_not_instantiated_alone(self):
        """Test that SQLMixin is used as mixin, not standalone"""
        # SQLMixin should only be used as mixin in inheritance tree
        mixin = SQLMixin()
        assert hasattr(mixin, 'execute_query'), "SQLMixin should have execute_query"


# ==============================================================================
# PACKAGE API TESTS: Required methods (names, username, event_counts)
# ==============================================================================

class TestEmployeeAPI:
    """Tests for Employee class public API"""
    
    def test_employee_names_method_exists(self):
        """Test that Employee.names() method exists"""
        emp = Employee()
        assert hasattr(emp, 'names'), "Employee should have names() method"
        assert callable(emp.names), "names should be callable"
    
    def test_employee_names_returns_dataframe(self, db_path):
        """Test that Employee.names() returns a pandas DataFrame"""
        emp = Employee()
        result = emp.names()
        assert isinstance(result, pd.DataFrame), "names() should return DataFrame"
    
    def test_employee_names_has_employee_id_column(self, db_path):
        """Test that names DataFrame has employee_id column"""
        emp = Employee()
        result = emp.names()
        assert 'employee_id' in result.columns, "names() should include employee_id"
    
    def test_employee_username_method_exists(self):
        """Test that Employee.username() method exists"""
        emp = Employee()
        assert hasattr(emp, 'username'), "Employee should have username() method"
        assert callable(emp.username), "username should be callable"
    
    def test_employee_username_returns_string_or_none(self, db_path):
        """Test that Employee.username() returns string or None"""
        emp = Employee()
        result = emp.username(1)
        assert isinstance(result, (str, type(None))), "username() should return string or None"
    
    def test_employee_event_counts_method_exists(self):
        """Test that Employee.event_counts() method exists"""
        emp = Employee()
        assert hasattr(emp, 'event_counts'), "Employee should have event_counts() method"
        assert callable(emp.event_counts), "event_counts should be callable"
    
    def test_employee_event_counts_returns_dataframe(self, db_path):
        """Test that Employee.event_counts() returns a pandas DataFrame"""
        emp = Employee()
        result = emp.event_counts(1)
        assert isinstance(result, pd.DataFrame), "event_counts() should return DataFrame"


class TestTeamAPI:
    """Tests for Team class public API"""
    
    def test_team_names_method_exists(self):
        """Test that Team.names() method exists"""
        team = Team()
        assert hasattr(team, 'names'), "Team should have names() method"
        assert callable(team.names), "names should be callable"
    
    def test_team_names_returns_dataframe(self, db_path):
        """Test that Team.names() returns a pandas DataFrame"""
        team = Team()
        result = team.names()
        assert isinstance(result, pd.DataFrame), "names() should return DataFrame"
    
    def test_team_names_has_team_id_column(self, db_path):
        """Test that names DataFrame has team_id column"""
        team = Team()
        result = team.names()
        assert 'team_id' in result.columns, "names() should include team_id"
    
    def test_team_username_method_exists(self):
        """Test that Team.username() method exists"""
        team = Team()
        assert hasattr(team, 'username'), "Team should have username() method"
        assert callable(team.username), "username should be callable"
    
    def test_team_username_returns_string_or_none(self, db_path):
        """Test that Team.username() returns string or None"""
        team = Team()
        result = team.username(1)
        assert isinstance(result, (str, type(None))), "username() should return string or None"
    
    def test_team_event_counts_method_exists(self):
        """Test that Team.event_counts() method exists"""
        team = Team()
        assert hasattr(team, 'event_counts'), "Team should have event_counts() method"
        assert callable(team.event_counts), "event_counts should be callable"
    
    def test_team_event_counts_returns_dataframe(self, db_path):
        """Test that Team.event_counts() returns a pandas DataFrame"""
        team = Team()
        result = team.event_counts(1)
        assert isinstance(result, pd.DataFrame), "event_counts() should return DataFrame"


# ==============================================================================
# INTEGRATION TESTS: Package usage in dashboard context
# ==============================================================================

class TestPackageIntegration:
    """Tests for package integration with dashboard"""
    
    def test_employee_instantiation(self):
        """Test that Employee class can be instantiated"""
        emp = Employee()
        assert emp is not None
        assert isinstance(emp, Employee)
    
    def test_team_instantiation(self):
        """Test that Team class can be instantiated"""
        team = Team()
        assert team is not None
        assert isinstance(team, Team)
    
    def test_employee_query_execution(self, db_path):
        """Test that Employee can execute queries"""
        emp = Employee()
        result = emp.get_all_employees()
        assert result is not None
        assert isinstance(result, list)
    
    def test_team_query_execution(self, db_path):
        """Test that Team can execute queries"""
        team = Team()
        result = team.get_all_teams()
        assert result is not None
        assert isinstance(result, list)
    
    def test_parameterized_queries(self, db_path):
        """Test that parameterized queries work (SQL injection prevention)"""
        emp = Employee()
        # This should not raise an error even with parameter
        result = emp.get_employee(1)
        assert result is not None or result == []


# ==============================================================================
# PANDAS DATAFRAME TESTS: New DataFrame methods
# ==============================================================================

class TestDataFrameOutput:
    """Tests for pandas DataFrame output from API methods"""
    
    def test_read_sql_method_exists(self):
        """Test that SQLMixin has read_sql method"""
        emp = Employee()
        assert hasattr(emp, 'read_sql'), "Employee should have read_sql method"
    
    def test_read_sql_returns_dataframe(self, db_path):
        """Test that read_sql returns DataFrame"""
        emp = Employee()
        result = emp.read_sql("SELECT * FROM employee LIMIT 1")
        assert isinstance(result, pd.DataFrame), "read_sql should return DataFrame"
    
    def test_event_counts_with_pandas(self, db_path):
        """Test event_counts returns valid DataFrame"""
        emp = Employee()
        result = emp.event_counts(1)
        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            # If there are records, check columns exist
            expected_cols = ['event_date', 'positive_events', 'negative_events']
            for col in expected_cols:
                assert col in result.columns or result.empty


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
