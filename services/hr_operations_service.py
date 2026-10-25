"""Basic monthly payroll and employee performance-log workflows."""
from datetime import datetime

from database.database import get_connection, transaction
from services.audit_service import insert_audit_log

ALLOWED_HR_ROLES = {"Admin", "HR"}


def _require_hr(user):
    if not user or user.get("role") not in ALLOWED_HR_ROLES:
        raise PermissionError("Only Admin or HR users can manage HR operations.")


def _validate_period(pay_period):
    value = str(pay_period).strip()
    try:
        datetime.strptime(value, "%Y-%m")
    except ValueError as exc:
        raise ValueError("Pay period must use YYYY-MM format.") from exc
    return value


def _validate_review_date(review_date):
    value = str(review_date).strip()
    try:
        datetime.strptime(value, "%d-%m-%Y")
    except ValueError as exc:
        raise ValueError("Review date must use DD-MM-YYYY format.") from exc
    return value


def list_active_employees(user):
    _require_hr(user)
    connection = get_connection()
    try:
        return connection.execute(
            "SELECT id, employee_code, full_name FROM employees WHERE status = 'Active' ORDER BY full_name"
        ).fetchall()
    finally:
        connection.close()


def create_payroll_record(employee_id, pay_period, deductions, bonus, performed_by):
    _require_hr(performed_by)
    pay_period = _validate_period(pay_period)
    try:
        deductions = float(deductions)
        bonus = float(bonus)
    except (TypeError, ValueError) as exc:
        raise ValueError("Deductions and bonus must be valid numbers.") from exc
    if deductions < 0 or bonus < 0:
        raise ValueError("Deductions and bonus cannot be negative.")

    with transaction() as connection:
        employee = connection.execute(
            "SELECT employee_code, salary FROM employees WHERE id = ? AND status = 'Active'",
            (employee_id,),
        ).fetchone()
        if employee is None:
            raise ValueError("Select an active employee.")
        basic_salary = float(employee[1])
        if deductions > basic_salary + bonus:
            raise ValueError("Deductions cannot exceed basic salary plus bonus.")
        net_salary = round(basic_salary - deductions + bonus, 2)
        cursor = connection.execute(
            """INSERT INTO payroll_records
               (employee_id, pay_period, basic_salary, deductions, bonus, net_salary, created_by)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (employee_id, pay_period, basic_salary, deductions, bonus, net_salary, performed_by["id"]),
        )
        insert_audit_log(
            connection, performed_by["id"], performed_by["username"],
            "CREATE_PAYROLL", "Payroll", cursor.lastrowid,
            f"Payroll created for {employee[0]} for {pay_period}", "Success",
        )
        return cursor.lastrowid


def get_payroll_records(user):
    _require_hr(user)
    connection = get_connection()
    try:
        return connection.execute(
            """SELECT p.id, e.employee_code, e.full_name, p.pay_period,
                      p.basic_salary, p.deductions, p.bonus, p.net_salary, p.created_at
               FROM payroll_records p JOIN employees e ON e.id = p.employee_id
               ORDER BY p.pay_period DESC, e.full_name"""
        ).fetchall()
    finally:
        connection.close()


def create_performance_log(employee_id, review_date, rating, comments, performed_by):
    _require_hr(performed_by)
    review_date = _validate_review_date(review_date)
    comments = str(comments).strip()
    try:
        rating = int(rating)
    except (TypeError, ValueError) as exc:
        raise ValueError("Rating must be an integer from 1 to 5.") from exc
    if rating < 1 or rating > 5:
        raise ValueError("Rating must be from 1 to 5.")
    if not comments:
        raise ValueError("Performance comments are required.")

    with transaction() as connection:
        employee = connection.execute(
            "SELECT employee_code FROM employees WHERE id = ?",
            (employee_id,),
        ).fetchone()
        if employee is None:
            raise ValueError("Employee record was not found.")
        cursor = connection.execute(
            """INSERT INTO performance_logs
               (employee_id, review_date, rating, comments, created_by)
               VALUES (?, ?, ?, ?, ?)""",
            (employee_id, review_date, rating, comments, performed_by["id"]),
        )
        insert_audit_log(
            connection, performed_by["id"], performed_by["username"],
            "CREATE_PERFORMANCE_LOG", "PerformanceLog", cursor.lastrowid,
            f"Performance review recorded for {employee[0]}", "Success",
        )
        return cursor.lastrowid


def get_performance_logs(user):
    _require_hr(user)
    connection = get_connection()
    try:
        return connection.execute(
            """SELECT p.id, e.employee_code, e.full_name, p.review_date,
                      p.rating, p.comments, p.created_at
               FROM performance_logs p JOIN employees e ON e.id = p.employee_id
               ORDER BY p.review_date DESC, p.id DESC"""
        ).fetchall()
    finally:
        connection.close()
