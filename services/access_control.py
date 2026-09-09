ROLE_PERMISSIONS = {
    "Admin": {
        "manage_users",
        "manage_employees",
        "view_employees",
        "view_audit_logs",
        "manage_backups",
    },
    "HR": {
        "manage_employees",
        "view_employees",
    },
    "Employee": {
        "view_employees",
    },
}


def has_permission(user, permission):
    """Return True when the logged-in user has the requested permission."""

    if not user:
        return False

    role = user.get("role")

    if role not in ROLE_PERMISSIONS:
        return False

    return permission in ROLE_PERMISSIONS[role]


def require_permission(user, permission):
    """Raise PermissionError when the user lacks a required permission."""

    if not has_permission(user, permission):
        raise PermissionError(
            f"User does not have permission: {permission}"
        )

    return True


def has_role(user, role):
    """Return True when the user has the specified role."""

    if not user:
        return False

    return user.get("role") == role


def has_any_role(user, roles):
    """Return True when the user has any role from the supplied roles."""

    if not user:
        return False

    return user.get("role") in roles