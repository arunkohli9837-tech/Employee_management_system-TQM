import re


EMAIL_PATTERN = re.compile(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)

PHONE_PATTERN = re.compile(
    r"^[0-9+\-\s()]{7,20}$"
)


def validate_required(value: str, field_name: str) -> str:
    """Validate that a required text field is not empty."""

    value = value.strip()

    if not value:
        raise ValueError(f"{field_name} must not be empty.")

    return value


def validate_email(email: str) -> str:
    """Validate and return a normalized email address."""

    email = validate_required(email, "Email")

    if not EMAIL_PATTERN.fullmatch(email):
        raise ValueError("Invalid email format.")

    return email


def validate_phone(phone: str) -> str:
    """Validate and return a normalized phone number."""

    phone = validate_required(phone, "Phone")

    if not PHONE_PATTERN.fullmatch(phone):
        raise ValueError("Invalid phone format.")

    return phone


def validate_salary(salary) -> float:
    """Validate that salary is numeric and non-negative."""

    try:
        salary = float(salary)
    except (TypeError, ValueError):
        raise ValueError("Salary must be a valid number.")

    if salary < 0:
        raise ValueError("Salary must not be negative.")

    return salary


def validate_employee_fields(
    employee_code: str,
    full_name: str,
    email: str,
    phone: str,
    department: str,
    designation: str,
    salary,
    joining_date: str,
):
    """Validate all required employee fields."""

    return {
        "employee_code": validate_required(
            employee_code, "Employee code"
        ),
        "full_name": validate_required(
            full_name, "Full name"
        ),
        "email": validate_email(email),
        "phone": validate_phone(phone),
        "department": validate_required(
            department, "Department"
        ),
        "designation": validate_required(
            designation, "Designation"
        ),
        "salary": validate_salary(salary),
        "joining_date": validate_required(
            joining_date, "Joining date"
        ),
    }