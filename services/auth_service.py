import sqlite3

from database.database import get_connection
from services.password_service import hash_password, verify_password


ALLOWED_ROLES = {"Admin", "HR", "Employee"}


def create_user(username: str, password: str, role: str) -> None:
    """Create a new application user."""
    username = username.strip()

    if not username:
        raise ValueError("Username must not be empty.")

    if not password:
        raise ValueError("Password must not be empty.")

    if role not in ALLOWED_ROLES:
        raise ValueError("Invalid user role.")

    password_hash = hash_password(password)

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO users (
                username,
                password_hash,
                role,
                is_active
            )
            VALUES (?, ?, ?, ?)
            """,
            (username, password_hash, role, 1),
        )

        connection.commit()

    except sqlite3.IntegrityError:
        connection.rollback()
        raise

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


def authenticate_user(username: str, password: str):
    """
    Authenticate a user.

    Returns a dictionary containing safe user information when
    authentication succeeds.

    Returns None when authentication fails.
    """
    username = username.strip()

    if not username or not password:
        return None

    connection = get_connection()

    try:
        user = connection.execute(
            """
            SELECT
                id,
                username,
                password_hash,
                role,
                is_active
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

        if user is None:
            return None

        user_id, stored_username, stored_hash, role, is_active = user

        if not is_active:
            return None

        if not verify_password(password, stored_hash):
            return None

        return {
            "id": user_id,
            "username": stored_username,
            "role": role,
        }

    finally:
        connection.close()