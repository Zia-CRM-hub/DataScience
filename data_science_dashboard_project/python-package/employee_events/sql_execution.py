"""
Decorator for handling SQLite database connections and SQL query execution
"""

import sqlite3
from pathlib import Path
from functools import wraps

def get_db_path():
    """Get the path to the employee_events.db database"""
    return Path(__file__).parent / "employee_events.db"

def sql_query(func):
    """
    Decorator that handles SQLite database connection lifecycle for SQL queries.
    
    The decorated function should return a SQL query string.
    The decorator handles:
    1. Opening a connection to the database
    2. Executing the SQL query
    3. Closing the connection
    4. Returning the data as a list of tuples
    
    Usage:
        @sql_query
        def get_employees():
            return "SELECT * FROM employee"
        
        data = get_employees()
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        db_path = get_db_path()
        
        # Get the SQL query from the decorated function
        query = func(*args, **kwargs)
        
        try:
            # Step 1: Open connection
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Step 2: Execute query
            cursor.execute(query)
            
            # Step 3: Fetch results
            results = cursor.fetchall()
            
            # Step 4: Close connection and return data
            conn.close()
            return results
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    return wrapper


class SQLMixin:
    """
    Mixin class that provides database connection handling for SQL queries.
    
    Methods in subclasses can use self.execute_query() to run SQL queries
    with automatic connection management.
    """
    
    def _get_db_path(self):
        """Get the path to the employee_events.db database"""
        return get_db_path()
    
    def execute_query(self, query):
        """
        Execute a SQL query with automatic connection handling.
        
        Args:
            query (str): SQL query string
            
        Returns:
            list: List of tuples containing query results
        """
        db_path = self._get_db_path()
        
        try:
            # Step 1: Open connection
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Step 2: Execute query
            cursor.execute(query)
            
            # Step 3: Fetch results
            results = cursor.fetchall()
            
            # Step 4: Close connection and return data
            conn.close()
            return results
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
