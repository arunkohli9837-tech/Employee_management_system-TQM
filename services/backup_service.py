"""SQLite-safe database backup, validation, and recovery operations."""
from datetime import datetime
import os
from pathlib import Path
import sqlite3

from database.database import DATABASE_PATH

BASE_DIR = Path(__file__).resolve().parent.parent
BACKUP_DIR = BASE_DIR / "backups"


def ensure_backup_directory() -> None:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]


def _sqlite_backup(source_path: Path, destination_path: Path) -> Path:
    """Use SQLite's online backup API rather than copying a live DB file."""
    source_path = Path(source_path)
    destination_path = Path(destination_path)
    if not source_path.exists():
        raise FileNotFoundError("Database file does not exist.")
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    source = destination = None
    try:
        source = sqlite3.connect(str(source_path), timeout=10)
        destination = sqlite3.connect(str(destination_path), timeout=10)
        source.backup(destination)
        result = destination.execute("PRAGMA integrity_check").fetchone()
        if result is None or result[0] != "ok":
            raise sqlite3.DatabaseError("Backup integrity check failed.")
    except Exception:
        try:
            destination_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise
    finally:
        if destination is not None:
            destination.close()
        if source is not None:
            source.close()
    return destination_path


def create_backup() -> Path:
    """Create a timestamped manual database backup."""
    ensure_backup_directory()
    return _sqlite_backup(
        DATABASE_PATH,
        BACKUP_DIR / f"employee_management_backup_{_timestamp()}.db",
    )


def create_automatic_backup() -> Path:
    """Create a timestamped automatic database backup."""
    ensure_backup_directory()
    return _sqlite_backup(
        DATABASE_PATH,
        BACKUP_DIR / f"employee_management_auto_{_timestamp()}.db",
    )


def list_backups() -> list[Path]:
    ensure_backup_directory()
    return sorted(
        BACKUP_DIR.glob("employee_management_*.db"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def validate_backup(backup_path: Path) -> bool:
    """Return True only when a file is an integrity-valid SQLite database."""
    backup_path = Path(backup_path)
    if not backup_path.is_file() or backup_path.stat().st_size == 0:
        return False
    connection = None
    try:
        connection = sqlite3.connect(f"file:{backup_path.resolve().as_posix()}?mode=ro", uri=True)
        result = connection.execute("PRAGMA integrity_check").fetchone()
        return result is not None and result[0] == "ok"
    except (sqlite3.Error, OSError, ValueError):
        return False
    finally:
        if connection is not None:
            connection.close()


def create_safety_backup() -> Path:
    """Create a verified safety backup before attempting a restore."""
    ensure_backup_directory()
    return _sqlite_backup(
        DATABASE_PATH,
        BACKUP_DIR / f"employee_management_safety_{_timestamp()}.db",
    )


def restore_backup(backup_path: Path) -> Path:
    """Restore a valid backup, preserving a safety copy and verifying the result."""
    backup_path = Path(backup_path).resolve()
    database_path = Path(DATABASE_PATH).resolve()
    if not backup_path.exists():
        raise FileNotFoundError("Selected backup does not exist.")
    if backup_path == database_path:
        raise ValueError("The active database cannot be selected as its own backup.")
    if not validate_backup(backup_path):
        raise ValueError("Selected backup is not a valid SQLite database.")

    safety_backup_path = create_safety_backup()
    database_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = database_path.with_name(
        f"{database_path.stem}.restore_{_timestamp()}.tmp.db"
    )
    try:
        _sqlite_backup(backup_path, temporary_path)
        if not validate_backup(temporary_path):
            raise sqlite3.DatabaseError("Restored database failed integrity validation.")
        os.replace(temporary_path, database_path)
    except Exception:
        try:
            if safety_backup_path.exists():
                recovery_path = database_path.with_name(
                    f"{database_path.stem}.recovery_{_timestamp()}.tmp.db"
                )
                _sqlite_backup(safety_backup_path, recovery_path)
                os.replace(recovery_path, database_path)
        except Exception:
            # Preserve the original failure; the safety backup remains available.
            pass
        raise
    finally:
        try:
            temporary_path.unlink(missing_ok=True)
        except OSError:
            pass
    return safety_backup_path
