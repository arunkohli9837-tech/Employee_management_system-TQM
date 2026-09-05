from database.database import get_connection


def _employee_row_to_dict(row):
    if row is None:
        return None

    return {
        "id": row[0],
        "employee_code": row[1],
        "full_name": row[2],
        "email": row[3],
        "phone": row[4],
        "department": row[5],
        "designation": row[6],
        "salary": row[7],
        "joining_date": row[8],
        "status": row[9],
        "created_at": row[10],
        "updated_at": row[11],
    }


def get_employee_by_id(employee_id: int):
    """Return an employee by database ID."""

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                id,
                employee_code,
                full_name,
                email,
                phone,
                department,
                designation,
                salary,
                joining_date,
                status,
                created_at,
                updated_at
            FROM employees
            WHERE id = ?
            """,
            (employee_id,),
        ).fetchone()

        return _employee_row_to_dict(row)

    finally:
        connection.close()