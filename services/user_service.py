from database.database import get_connection


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
            SELECT
                id,
                username,
                role,
                is_active
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
            SELECT
                id,
                username,
                role,
                is_active
            FROM users
            ORDER BY id
            """
        ).fetchall()

        return [_user_row_to_dict(row) for row in rows]

    finally:
        connection.close()

def deactivate_user(user_id: int):
    """Deactivate an active user account."""

    connection = get_connection()

    try:
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
            connection.rollback()
            return False

        connection.commit()
        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def activate_user(user_id: int):
    """Activate an inactive user account."""

    connection = get_connection()

    try:
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
            connection.rollback()
            return False

        connection.commit()
        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()