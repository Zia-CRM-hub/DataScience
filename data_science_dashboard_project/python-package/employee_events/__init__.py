"""
Employee Events Package
"""

from .queries import QueryBase, Employee, Team
from .sql_execution import sql_query, SQLMixin
from .db_setup import create_database, get_db_path

__version__ = "1.0.0"
__all__ = [
    "QueryBase",
    "Employee", 
    "Team",
    "sql_query",
    "SQLMixin",
    "create_database",
    "get_db_path"
]
