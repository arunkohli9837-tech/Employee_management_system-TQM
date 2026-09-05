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
    if not user:
        return False

    role = user.get("role")

    if role not in ROLE_PERMISSIONS:
        return False

    return permission in ROLE_PERMISSIONS[role]


def has_role(user, role):
    if not user:
        return False

    return user.get("role") == role


def has_any_role(user, roles):
    if not user:
        return False

    return user.get("role") in roles