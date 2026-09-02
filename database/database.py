from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "employee_management.db"


def get_connection() -> sqlite3.Connection:
    """Create and configure a connection to the SQLite database."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=10,
    )

    connection.execute("PRAGMA foreign_keys = ON")

    return connection