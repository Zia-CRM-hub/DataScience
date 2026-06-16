"""
SQLite database creation and schema for Employee Events system
"""

import sqlite3
from pathlib import Path

def create_database():
    """Create the employee_events.db database with all required tables"""
    db_path = Path(__file__).parent / "employee_events.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create team table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team (
            team_id INTEGER PRIMARY KEY,
            team_name TEXT NOT NULL,
            shift TEXT,
            manager_name TEXT
        )
    """)
    
    # Create employee table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee (
            employee_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            team_id INTEGER NOT NULL,
            FOREIGN KEY (team_id) REFERENCES team(team_id)
        )
    """)
    
    # Create employee_events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee_events (
            event_date TEXT NOT NULL,
            employee_id INTEGER NOT NULL,
            team_id INTEGER NOT NULL,
            positive_events INTEGER DEFAULT 0,
            negative_events INTEGER DEFAULT 0,
            PRIMARY KEY (event_date, employee_id, team_id),
            FOREIGN KEY (employee_id) REFERENCES employee(employee_id),
            FOREIGN KEY (team_id) REFERENCES team(team_id)
        )
    """)
    
    # Create notes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            employee_id INTEGER NOT NULL,
            team_id INTEGER NOT NULL,
            note TEXT,
            note_date TEXT NOT NULL,
            PRIMARY KEY (employee_id, team_id, note_date),
            FOREIGN KEY (employee_id) REFERENCES employee(employee_id),
            FOREIGN KEY (team_id) REFERENCES team(team_id)
        )
    """)
    
    # Insert sample data
    cursor.execute("INSERT OR IGNORE INTO team VALUES (1, 'Engineering', 'Day', 'Alice Johnson')")
    cursor.execute("INSERT OR IGNORE INTO team VALUES (2, 'Sales', 'Day', 'Bob Smith')")
    cursor.execute("INSERT OR IGNORE INTO team VALUES (3, 'HR', 'Day', 'Carol White')")
    
    cursor.execute("INSERT OR IGNORE INTO employee VALUES (1, 'John', 'Doe', 1)")
    cursor.execute("INSERT OR IGNORE INTO employee VALUES (2, 'Jane', 'Smith', 1)")
    cursor.execute("INSERT OR IGNORE INTO employee VALUES (3, 'Mike', 'Johnson', 2)")
    
    cursor.execute("INSERT OR IGNORE INTO employee_events VALUES ('2024-01-01', 1, 1, 3, 0)")
    cursor.execute("INSERT OR IGNORE INTO employee_events VALUES ('2024-01-02', 2, 1, 2, 1)")
    cursor.execute("INSERT OR IGNORE INTO employee_events VALUES ('2024-01-03', 3, 2, 4, 0)")
    
    cursor.execute("INSERT OR IGNORE INTO notes VALUES (1, 1, 'Great performance on project', '2024-01-01')")
    cursor.execute("INSERT OR IGNORE INTO notes VALUES (2, 1, 'Completed training', '2024-01-02')")
    
    conn.commit()
    conn.close()
    
    return db_path

if __name__ == "__main__":
    db_path = create_database()
    print(f"Database created at: {db_path}")
