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

def create_employee(
    employee_code: str,
    full_name: str,
    email: str,
    phone: str,
    department: str,
    designation: str,
    salary: float,
    joining_date: str,
):
    """Create a new employee record and return its database ID."""

    employee_code = employee_code.strip()
    full_name = full_name.strip()
    email = email.strip()
    phone = phone.strip()
    department = department.strip()
    designation = designation.strip()
    joining_date = joining_date.strip()

    if not employee_code:
        raise ValueError("Employee code must not be empty.")

    if not full_name:
        raise ValueError("Full name must not be empty.")

    if not email:
        raise ValueError("Email must not be empty.")

    if not phone:
        raise ValueError("Phone must not be empty.")

    if not department:
        raise ValueError("Department must not be empty.")

    if not designation:
        raise ValueError("Designation must not be empty.")

    if not joining_date:
        raise ValueError("Joining date must not be empty.")

    if salary < 0:
        raise ValueError("Salary must not be negative.")

    connection = get_connection()

    try:
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
                joining_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
            ),
        )

        connection.commit()
        return cursor.lastrowid

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close() 

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
):
    """Update an existing employee record."""

    employee_code = employee_code.strip()
    full_name = full_name.strip()
    email = email.strip()
    phone = phone.strip()
    department = department.strip()
    designation = designation.strip()
    joining_date = joining_date.strip()

    if not employee_code:
        raise ValueError("Employee code must not be empty.")

    if not full_name:
        raise ValueError("Full name must not be empty.")

    if not email:
        raise ValueError("Email must not be empty.")

    if not phone:
        raise ValueError("Phone must not be empty.")

    if not department:
        raise ValueError("Department must not be empty.")

    if not designation:
        raise ValueError("Designation must not be empty.")

    if not joining_date:
        raise ValueError("Joining date must not be empty.")

    if salary < 0:
        raise ValueError("Salary must not be negative.")

    connection = get_connection()

    try:
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
            connection.rollback()
            return False

        connection.commit()
        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

def deactivate_employee(employee_id: int):
    """Deactivate an employee without permanently deleting the record."""

    connection = get_connection()

    try:
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
            connection.rollback()
            return False

        connection.commit()
        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()