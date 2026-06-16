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

# Get the database path
db_path = get_db_path()


@pytest.fixture
def db():
    """Fixture that provides the database path and ensures it exists"""
    if not db_path.exists():
        create_database()
    return db_path


def test_db_path(db):
    """Test that we can get the database path"""
    assert db is not None
    assert isinstance(db, Path)
    print(f"Database path: {db}")


def test_db_exists(db):
    """Test that the database file exists"""
    assert db.exists(), f"Database file does not exist at {db}"


def test_employee_table_exists(db):
    """Test that the employee table exists in the database"""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='employee'
    """)
    result = cursor.fetchone()
    conn.close()
    
    assert result is not None, "Employee table does not exist"


def test_team_table_exists(db):
    """Test that the team table exists in the database"""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='team'
    """)
    result = cursor.fetchone()
    conn.close()
    
    assert result is not None, "Team table does not exist"


def test_employee_events_table_exists(db):
    """Test that the employee_events table exists in the database"""
    conn = sqlite3.connect(db)
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
