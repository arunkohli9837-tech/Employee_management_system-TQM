from database.database import transaction, get_connection
from services.audit_service import insert_audit_log
from services.password_service import hash_password


ALLOWED_ROLES = {"Admin", "HR", "Employee"}


def _user_row_to_dict(row):
    if row is None:
        return None

    return {
        "id": row[0],
        "username": row[1],
        "role": row[2],
        "is_active": row[3],
    }


def get_user_by_id(user_id: int):
    """Return a user by database ID without exposing the password hash."""

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT id, username, role, is_active
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

        return _user_row_to_dict(row)

    finally:
        connection.close()


def get_all_users():
    """Return all users without exposing password hashes."""

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT id, username, role, is_active
            FROM users
            ORDER BY id
            """
        ).fetchall()

        return [_user_row_to_dict(row) for row in rows]

    finally:
        connection.close()


def update_user(
    user_id: int,
    username: str,
    role: str,
    password: str = "",
    performed_by=None,
):
    """Update username, role and optionally password."""

    username = username.strip()
    role = role.strip()

    if not username:
        raise ValueError("Username must not be empty.")

    if role not in ALLOWED_ROLES:
        raise ValueError("Invalid user role.")

    with transaction() as connection:
        existing = connection.execute(
            """
            SELECT username
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

        if existing is None:
            return False

        old_username = existing[0]

        if password.strip():
            password_hash = hash_password(password)

            connection.execute(
                """
                UPDATE users
                SET username = ?,
                    role = ?,
                    password_hash = ?
                WHERE id = ?
                """,
                (
                    username,
                    role,
                    password_hash,
                    user_id,
                ),
            )
        else:
            connection.execute(
                """
                UPDATE users
                SET username = ?,
                    role = ?
                WHERE id = ?
                """,
                (
                    username,
                    role,
                    user_id,
                ),
            )

        if performed_by:
            insert_audit_log(
                connection=connection,
                user_id=performed_by["id"],
                username=performed_by["username"],
                action="UPDATE_USER",
                target_type="User",
                target_id=user_id,
                description=f"User {old_username} updated successfully",
                status="Success",
            )

        return True


def deactivate_user(user_id: int, performed_by=None):
    """Deactivate an active user account."""

    with transaction() as connection:
        row = connection.execute(
            """
            SELECT username
            FROM users
            WHERE id = ?
              AND is_active = 1
            """,
            (user_id,),
        ).fetchone()

        if row is None:
            return False

        target_username = row[0]

        cursor = connection.execute(
            """
            UPDATE users
            SET is_active = 0
            WHERE id = ?
              AND is_active = 1
            """,
            (user_id,),
        )

        if cursor.rowcount == 0:
            return False

        if performed_by:
            insert_audit_log(
                connection=connection,
                user_id=performed_by["id"],
                username=performed_by["username"],
                action="DEACTIVATE_USER",
                target_type="User",
                target_id=user_id,
                description=f"User {target_username} deactivated successfully",
                status="Success",
            )

        return True


def activate_user(user_id: int, performed_by=None):
    """Activate an inactive user account."""

    with transaction() as connection:
        row = connection.execute(
            """
            SELECT username
            FROM users
            WHERE id = ?
              AND is_active = 0
            """,
            (user_id,),
        ).fetchone()

        if row is None:
            return False

        target_username = row[0]

        cursor = connection.execute(
            """
            UPDATE users
            SET is_active = 1
            WHERE id = ?
              AND is_active = 0
            """,
            (user_id,),
        )

        if cursor.rowcount == 0:
            return False

        if performed_by:
            insert_audit_log(
                connection=connection,
                user_id=performed_by["id"],
                username=performed_by["username"],
                action="ACTIVATE_USER",
                target_type="User",
                target_id=user_id,
                description=f"User {target_username} activated successfully",
                status="Success",
            )

        return True