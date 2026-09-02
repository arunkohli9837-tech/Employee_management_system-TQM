import base64
import hashlib
import hmac
import secrets
import sqlite3

from database.database import get_connection


ALLOWED_ROLES = {"Admin", "HR", "Employee"}

HASH_ALGORITHM = "sha256"
PBKDF2_ITERATIONS = 600_000
SALT_LENGTH = 16


def _hash_password(password: str) -> str:
    """Create a salted PBKDF2 password hash."""
    if not isinstance(password, str) or not password:
        raise ValueError("Password must not be empty.")

    salt = secrets.token_bytes(SALT_LENGTH)

    password_hash = hashlib.pbkdf2_hmac(
        HASH_ALGORITHM,
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )

    encoded_salt = base64.b64encode(salt).decode("ascii")
    encoded_hash = base64.b64encode(password_hash).decode("ascii")

    return (
        f"pbkdf2_{HASH_ALGORITHM}$"
        f"{PBKDF2_ITERATIONS}$"
        f"{encoded_salt}$"
        f"{encoded_hash}"
    )


def _verify_password(password: str, stored_hash: str) -> bool:
    """Verify a password against a stored PBKDF2 hash."""
    try:
        algorithm, iterations, encoded_salt, encoded_hash = stored_hash.split(
            "$",
            maxsplit=3,
        )

        if algorithm != f"pbkdf2_{HASH_ALGORITHM}":
            return False

        iterations = int(iterations)

        salt = base64.b64decode(encoded_salt)
        expected_hash = base64.b64decode(encoded_hash)

        actual_hash = hashlib.pbkdf2_hmac(
            HASH_ALGORITHM,
            password.encode("utf-8"),
            salt,
            iterations,
        )

        return hmac.compare_digest(actual_hash, expected_hash)

    except (ValueError, TypeError, UnicodeError):
        return False


def create_user(username: str, password: str, role: str) -> None:
    """Create a new application user."""
    username = username.strip()

    if not username:
        raise ValueError("Username must not be empty.")

    if not password:
        raise ValueError("Password must not be empty.")

    password_hash = _hash_password(password)

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

        if not _verify_password(password, stored_hash):
            return None

        return {
            "id": user_id,
            "username": stored_username,
            "role": role,
        }

    finally:
        connection.close()