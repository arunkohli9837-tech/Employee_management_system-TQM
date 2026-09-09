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