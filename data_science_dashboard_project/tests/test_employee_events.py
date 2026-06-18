"""
Pytest test functions for Employee Events System
"""

import pytest
from pathlib import Path
import sys
import sqlite3

# Add python-package to path
sys.path.insert(0, str(Path(__file__).parent.parent / "python-package"))

from employee_events.db_setup import get_db_path, create_database

# Path variable for interacting with the SQLite database
DB_PATH = get_db_path()


@pytest.fixture
def db_path():
    """Fixture that provides the database path and ensures it exists"""
    if not DB_PATH.exists():
        create_database()
    return DB_PATH


def test_db_path(db_path):
    """Test that we can get the database path"""
    assert db_path is not None
    assert isinstance(db_path, Path)
    print(f"Database path: {db_path}")


def test_db_exists(db_path):
    """Test that the database file exists"""
    assert db_path.exists(), f"Database file does not exist at {db_path}"


def test_employee_table_exists(db_path):
    """Test that the employee table exists in the database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='employee'
    """)
    result = cursor.fetchone()
    conn.close()
    
    assert result is not None, "Employee table does not exist"


def test_team_table_exists(db_path):
    """Test that the team table exists in the database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='team'
    """)
    result = cursor.fetchone()
    conn.close()
    
    assert result is not None, "Team table does not exist"


def test_employee_events_table_exists(db_path):
    """Test that the employee_events table exists in the database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='employee_events'
    """)
    result = cursor.fetchone()
    conn.close()
    
    assert result is not None, "Employee_events table does not exist"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
