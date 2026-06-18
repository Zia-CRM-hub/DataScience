"""
SQLite database creation and schema for Employee Events system
"""

import csv
import sqlite3
from pathlib import Path


def get_db_path():
    """Return the canonical SQLite database path for this package."""
    return Path(__file__).parent / "employee_events.db"


def get_project_root():
    """Return the data_science_dashboard_project root directory."""
    return Path(__file__).resolve().parent.parent.parent


def get_sample_data_dir():
    """Return the project sample data directory."""
    return get_project_root() / "sample_data"


def _seed_from_csv(cursor):
    """Seed database tables from CSV files in sample_data directory."""
    sample_dir = get_sample_data_dir()
    if not sample_dir.exists():
        return False

    team_file = sample_dir / "team.csv"
    employee_file = sample_dir / "employee.csv"
    events_file = sample_dir / "employee_events.csv"
    notes_file = sample_dir / "notes.csv"

    required_files = [team_file, employee_file, events_file, notes_file]
    if not all(path.exists() for path in required_files):
        return False

    with team_file.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        cursor.executemany(
            """
            INSERT OR IGNORE INTO team (team_id, team_name, shift, manager_name)
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    int(row["team_id"]),
                    row["team_name"],
                    row["shift"],
                    row["manager_name"],
                )
                for row in rows
            ],
        )

    with employee_file.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        cursor.executemany(
            """
            INSERT OR IGNORE INTO employee (employee_id, first_name, last_name, team_id)
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    int(row["employee_id"]),
                    row["first_name"],
                    row["last_name"],
                    int(row["team_id"]),
                )
                for row in rows
            ],
        )

    with events_file.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        cursor.executemany(
            """
            INSERT OR IGNORE INTO employee_events
            (event_date, employee_id, team_id, positive_events, negative_events)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (
                    row["event_date"],
                    int(row["employee_id"]),
                    int(row["team_id"]),
                    int(row["positive_events"]),
                    int(row["negative_events"]),
                )
                for row in rows
            ],
        )

    with notes_file.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        cursor.executemany(
            """
            INSERT OR IGNORE INTO notes (employee_id, team_id, note, note_date)
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    int(row["employee_id"]),
                    int(row["team_id"]),
                    row["note"],
                    row["note_date"],
                )
                for row in rows
            ],
        )

    return True

def create_database():
    """Create the employee_events.db database with all required tables"""
    db_path = get_db_path()
    
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
    
    # Seed sample data from CSV files. If files are missing, fallback to minimal seed.
    seeded = _seed_from_csv(cursor)
    if not seeded:
        cursor.execute("INSERT OR IGNORE INTO team VALUES (1, 'Engineering', 'Day', 'Alice Johnson')")
        cursor.execute("INSERT OR IGNORE INTO employee VALUES (1, 'John', 'Doe', 1)")
        cursor.execute("INSERT OR IGNORE INTO employee_events VALUES ('2024-01-01', 1, 1, 3, 0)")
        cursor.execute("INSERT OR IGNORE INTO notes VALUES (1, 1, 'Great performance on project', '2024-01-01')")
    
    conn.commit()
    conn.close()
    
    return db_path

if __name__ == "__main__":
    db_path = create_database()
    print(f"Database created at: {db_path}")
