from database.database import get_connection, transaction
from services.validation_service import validate_employee_fields
from services.audit_service import insert_audit_log


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


def create_employee(
    employee_code: str,
    full_name: str,
    email: str,
    phone: str,
    department: str,
    designation: str,
    salary: float,
    joining_date: str,
    performed_by=None,
):
    """Create a new employee record and return its database ID."""

    validated = validate_employee_fields(
        employee_code,
        full_name,
        email,
        phone,
        department,
        designation,
        salary,
        joining_date,
    )

    employee_code = validated["employee_code"]
    full_name = validated["full_name"]
    email = validated["email"]
    phone = validated["phone"]
    department = validated["department"]
    designation = validated["designation"]
    salary = validated["salary"]
    joining_date = validated["joining_date"]

    with transaction() as connection:
        cursor = connection.execute(
            """
            INSERT INTO employees (
                employee_code,
                full_name,
                email,
                phone,
                department,
                designation,
                salary,
                joining_date,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                employee_code,
                full_name,
                email,
                phone,
                department,
                designation,
                salary,
                joining_date,
                "Active",
            ),
        )

        employee_id = cursor.lastrowid

        if performed_by:
            insert_audit_log(
                connection=connection,
                user_id=performed_by["id"],
                username=performed_by["username"],
                action="CREATE_EMPLOYEE",
                target_type="Employee",
                target_id=employee_id,
                description=f"Employee {employee_code} created successfully",
                status="Success",
            )

    return employee_id


def get_all_employees():
    """Return all employee records ordered by database ID."""

    connection = get_connection()

    try:
        rows = connection.execute(
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
            ORDER BY id
            """
        ).fetchall()

        return [_employee_row_to_dict(row) for row in rows]

    finally:
        connection.close()


def search_employees(search_term: str):
    """Search employees by code, name, email, or department."""

    search_term = search_term.strip()

    if not search_term:
        return []

    connection = get_connection()

    try:
        pattern = f"%{search_term}%"

        rows = connection.execute(
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
            WHERE employee_code LIKE ?
               OR full_name LIKE ?
               OR email LIKE ?
               OR department LIKE ?
            ORDER BY id
            """,
            (pattern, pattern, pattern, pattern),
        ).fetchall()

        return [_employee_row_to_dict(row) for row in rows]

    finally:
        connection.close()


def update_employee(
    employee_id: int,
    employee_code: str,
    full_name: str,
    email: str,
    phone: str,
    department: str,
    designation: str,
    salary: float,
    joining_date: str,
    performed_by=None,
):
    """Update an existing employee record."""

    validated = validate_employee_fields(
        employee_code,
        full_name,
        email,
        phone,
        department,
        designation,
        salary,
        joining_date,
    )

    employee_code = validated["employee_code"]
    full_name = validated["full_name"]
    email = validated["email"]
    phone = validated["phone"]
    department = validated["department"]
    designation = validated["designation"]
    salary = validated["salary"]
    joining_date = validated["joining_date"]

    with transaction() as connection:
        cursor = connection.execute(
            """
            UPDATE employees
            SET
                employee_code = ?,
                full_name = ?,
                email = ?,
                phone = ?,
                department = ?,
                designation = ?,
                salary = ?,
                joining_date = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                employee_code,
                full_name,
                email,
                phone,
                department,
                designation,
                salary,
                joining_date,
                employee_id,
            ),
        )

        if cursor.rowcount == 0:
            return False

        if performed_by:
            insert_audit_log(
                connection=connection,
                user_id=performed_by["id"],
                username=performed_by["username"],
                action="UPDATE_EMPLOYEE",
                target_type="Employee",
                target_id=employee_id,
                description=f"Employee {employee_code} updated successfully",
                status="Success",
            )

        return True


def deactivate_employee(employee_id: int, performed_by=None):
    """Deactivate an employee without permanently deleting the record."""

    with transaction() as connection:
        cursor = connection.execute(
            """
            UPDATE employees
            SET
                status = 'Inactive',
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
              AND status = 'Active'
            """,
            (employee_id,),
        )

        if cursor.rowcount == 0:
            return False

        if performed_by:
            insert_audit_log(
                connection=connection,
                user_id=performed_by["id"],
                username=performed_by["username"],
                action="DEACTIVATE_EMPLOYEE",
                target_type="Employee",
                target_id=employee_id,
                description=f"Employee ID {employee_id} deactivated successfully",
                status="Success",
            )

        return True