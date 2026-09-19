from pathlib import Path
import shutil
import sqlite3
from datetime import datetime

from database.database import DATABASE_PATH


BASE_DIR = Path(__file__).resolve().parent.parent
BACKUP_DIR = BASE_DIR / "backups"


def ensure_backup_directory() -> None:
    """Create the backup directory if it does not exist."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def create_backup() -> Path:
    """Create a timestamped copy of the current database."""
    ensure_backup_directory()

    if not DATABASE_PATH.exists():
        raise FileNotFoundError("Database file does not exist.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_path = BACKUP_DIR / (
        f"employee_management_backup_{timestamp}.db"
    )

    shutil.copy2(DATABASE_PATH, backup_path)

    return backup_path


def list_backups() -> list[Path]:
    """Return available database backup files."""
    ensure_backup_directory()

    return sorted(
        BACKUP_DIR.glob("employee_management_backup_*.db"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def validate_backup(backup_path: Path) -> bool:
    """Check whether a backup is a valid SQLite database."""
    if not backup_path.exists():
        return False

    try:
        connection = sqlite3.connect(backup_path)

        result = connection.execute(
            "PRAGMA integrity_check"
        ).fetchone()

        connection.close()

        return result is not None and result[0] == "ok"

    except sqlite3.Error:
        return False


def create_safety_backup() -> Path:
    """Create a safety backup of the current database before restore."""
    ensure_backup_directory()

    if not DATABASE_PATH.exists():
        raise FileNotFoundError("Database file does not exist.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    safety_backup_path = BACKUP_DIR / (
        f"employee_management_safety_{timestamp}.db"
    )

    shutil.copy2(DATABASE_PATH, safety_backup_path)

    return safety_backup_path


def restore_backup(backup_path: Path) -> Path:
    """Restore a valid backup after creating a safety backup."""
    backup_path = Path(backup_path)

    if not backup_path.exists():
        raise FileNotFoundError("Selected backup does not exist.")

    if not validate_backup(backup_path):
        raise ValueError("Selected backup is not a valid SQLite database.")

    safety_backup_path = create_safety_backup()

    try:
        shutil.copy2(backup_path, DATABASE_PATH)
    except Exception:
        # Restore the original database if the restore operation fails.
        shutil.copy2(safety_backup_path, DATABASE_PATH)
        raise

    return safety_backup_path