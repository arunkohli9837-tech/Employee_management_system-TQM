from database.database import get_connection


def create_audit_log(
    user_id,
    username,
    action,
    target_type,
    target_id=None,
    description="",
    status="Success",
):
    """Create an audit log entry for a system action."""

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO audit_logs (
                user_id,
                username,
                action,
                target_type,
                target_id,
                description,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                username,
                action,
                target_type,
                target_id,
                description,
                status,
            ),
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
def _audit_row_to_dict(row):
    """Convert an audit-log database row into a dictionary."""

    if row is None:
        return None

    return {
        "id": row[0],
        "user_id": row[1],
        "username": row[2],
        "action": row[3],
        "target_type": row[4],
        "target_id": row[5],
        "description": row[6],
        "status": row[7],
        "created_at": row[8],
    }


def get_all_audit_logs():
    """Return all audit logs ordered from newest to oldest."""

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                id,
                user_id,
                username,
                action,
                target_type,
                target_id,
                description,
                status,
                created_at
            FROM audit_logs
            ORDER BY id DESC
            """
        ).fetchall()

        return [_audit_row_to_dict(row) for row in rows]

    finally:
        connection.close()


def search_audit_logs(search_term: str):
    """Search audit logs by username, action, target type, or description."""

    search_term = search_term.strip()

    if not search_term:
        return []

    pattern = f"%{search_term}%"

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                id,
                user_id,
                username,
                action,
                target_type,
                target_id,
                description,
                status,
                created_at
            FROM audit_logs
            WHERE username LIKE ?
               OR action LIKE ?
               OR target_type LIKE ?
               OR description LIKE ?
            ORDER BY id DESC
            """,
            (
                pattern,
                pattern,
                pattern,
                pattern,
            ),
        ).fetchall()

        return [_audit_row_to_dict(row) for row in rows]

    finally:
        connection.close()