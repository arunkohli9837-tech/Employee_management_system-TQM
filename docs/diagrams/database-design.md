# Employee Management System — Database Design

## 1. Purpose

This document defines the initial database design for the Employee Management System.

The application will use SQLite as its primary local database.

The design is based on the current project requirements and architecture and may be refined during actual implementation when a genuine requirement or technical constraint is identified.

---

## 2. Database Technology

| Item | Decision |
|---|---|
| Database | SQLite |
| Python Library | sqlite3 |
| Database Type | Local relational database |
| Primary Usage | Employee and system data storage |
| Integrity | Constraints and transactions |
| Backup | SQLite database backup/recovery mechanisms |

---

## 3. Planned Tables

The initial database design contains the following tables:

1. `users`
2. `employees`
3. `audit_logs`
4. `error_logs`
5. `backup_history`

Additional tables may be introduced if an actual implementation requirement justifies them.

---

# 4. Users Table

The `users` table will store application account information.

## Purpose

It will support:

- Authentication
- Role management
- Account status
- Current-user identification
- User administration

## Planned Fields

| Field | Type | Constraints / Purpose |
|---|---|---|
| id | INTEGER | Primary Key |
| username | TEXT | Required, Unique |
| password_hash | TEXT | Required |
| role | TEXT | Required, Valid Role |
| is_active | INTEGER | Required, Account status |
| created_at | TEXT | Required |
| updated_at | TEXT | Required |

### Role Values

The planned roles are:

- Admin
- HR
- Employee

The implementation may use an appropriate database representation for these values.

### Reliability Considerations

- Username uniqueness should be enforced.
- Required account fields should not accept NULL values.
- Invalid roles should be prevented.
- Account status should be controlled by the application and database rules where appropriate.

---

# 5. Employees Table

The `employees` table will store employee information.

## Purpose

It will support:

- Employee creation
- Employee viewing
- Employee search
- Employee updates
- Employee deactivation

## Planned Fields

| Field | Type | Constraints / Purpose |
|---|---|---|
| id | INTEGER | Primary Key |
| employee_code | TEXT | Required, Unique |
| full_name | TEXT | Required |
| email | TEXT | Required, Unique |
| phone | TEXT | Required/Validated |
| department | TEXT | Required |
| designation | TEXT | Required |
| salary | REAL | Required, Non-negative |
| joining_date | TEXT | Required |
| status | TEXT | Required |
| created_at | TEXT | Required |
| updated_at | TEXT | Required |

### Employee Status

The application is expected to support an active/inactive state rather than permanently deleting historical employee information.

### Reliability Considerations

- Employee code should be unique.
- Employee email should be unique.
- Required fields should be protected against NULL values.
- Salary should not be negative.
- Employee deactivation should preserve historical information.
- Appropriate database constraints should provide a second layer of protection in addition to UI validation.

---

# 6. Audit Logs Table

The `audit_logs` table will provide traceability for important operations.

## Purpose

It will help with:

- Accountability
- Traceability
- Reliability analysis
- Reviewing important operations

## Planned Fields

| Field | Type | Constraints / Purpose |
|---|---|---|
| id | INTEGER | Primary Key |
| user_id | INTEGER | Foreign Key to users |
| username | TEXT | Recorded username where useful |
| action | TEXT | Operation performed |
| target_type | TEXT | Object affected |
| target_id | INTEGER | Affected record ID where applicable |
| description | TEXT | Operation details |
| status | TEXT | Operation result |
| created_at | TEXT | Timestamp |

### Relationship

A log entry may reference the user who performed the operation.

Conceptually:

```text
users
  |
  | 1
  |
  | many
  v
audit_logs