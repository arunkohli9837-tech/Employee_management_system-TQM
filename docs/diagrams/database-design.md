# Employee Management System — Database Design

## 1. Purpose

This document describes the SQLite database structure currently defined by the project schema and the reliability controls associated with it.

The database is accessed from Python through the `sqlite3` library and is kept separate from the GUI layer.

---

## 2. Database Technology

| Item | Decision |
|---|---|
| Database | SQLite |
| Python Library | `sqlite3` |
| Database Type | Local relational database |
| Primary Usage | Employee and system data storage |
| Integrity | Primary keys, foreign keys, UNIQUE, NOT NULL, CHECK constraints, and transactions |
| Backup | Database backup/recovery mechanisms planned for later implementation |

---

## 3. Current Schema

The current `database/schema.sql` defines five tables:

1. `users`
2. `employees`
3. `audit_logs`
4. `error_logs`
5. `backup_history`

These tables form the database foundation for authentication, employee management, auditability, error logging, and backup/recovery functionality.

---

# 4. Users Table

The `users` table stores application account information.

| Field | Type | Constraints / Purpose |
|---|---|---|
| id | INTEGER | Primary Key |
| username | TEXT | NOT NULL, UNIQUE, case-insensitive |
| password_hash | TEXT | NOT NULL |
| role | TEXT | NOT NULL, CHECK: Admin / HR / Employee |
| is_active | INTEGER | NOT NULL, CHECK: 0 / 1 |
| created_at | TEXT | NOT NULL, timestamp |
| updated_at | TEXT | NOT NULL, timestamp |

### Roles

- Admin
- HR
- Employee

### Reliability Considerations

- Username uniqueness is enforced by the database.
- Invalid roles are prevented by a `CHECK` constraint.
- Account status is restricted to active/inactive values.
- Password hashes are stored instead of plain-text passwords.

---

# 5. Employees Table

The `employees` table stores employee information.

| Field | Type | Constraints / Purpose |
|---|---|---|
| id | INTEGER | Primary Key |
| employee_code | TEXT | NOT NULL, UNIQUE, case-insensitive |
| full_name | TEXT | NOT NULL |
| email | TEXT | NOT NULL, UNIQUE, case-insensitive |
| phone | TEXT | NOT NULL; application validated |
| department | TEXT | NOT NULL |
| designation | TEXT | NOT NULL |
| salary | REAL | NOT NULL, CHECK salary >= 0 |
| joining_date | TEXT | NOT NULL; application validated as `DD-MM-YYYY` |
| status | TEXT | NOT NULL, CHECK: Active / Inactive |
| created_at | TEXT | NOT NULL, timestamp |
| updated_at | TEXT | NOT NULL, timestamp |

### Employee Status

Employees are deactivated by changing their status to `Inactive` instead of permanently deleting the database record.

### Reliability Considerations

- Employee code and email uniqueness are enforced by the database.
- Required fields use `NOT NULL`.
- Salary cannot be negative because of a database `CHECK` constraint.
- Joining date format is validated by the application before insertion/update.
- Soft deactivation preserves historical employee information.
- Application validation provides an additional protection layer before database constraints.

---

# 6. Audit Logs Table

The `audit_logs` table provides traceability for important operations.

| Field | Type | Constraints / Purpose |
|---|---|---|
| id | INTEGER | Primary Key |
| user_id | INTEGER | Foreign Key to `users`, `ON DELETE SET NULL` |
| username | TEXT | Recorded username where applicable |
| action | TEXT | Operation performed |
| target_type | TEXT | Object affected |
| target_id | INTEGER | Affected record ID where applicable |
| description | TEXT | Operation details |
| status | TEXT | Operation result |
| created_at | TEXT | NOT NULL, timestamp |

### Relationship

```text
users
  |
  | 1
  |
  | many
  v
audit_logs
```

Successful authentication is currently integrated with audit logging. Additional auditable operations can be connected as those features are implemented.

---

# 7. Error Logs Table

The `error_logs` table provides a database location for technical application error records.

| Field | Type | Constraints / Purpose |
|---|---|---|
| id | INTEGER | Primary Key |
| user_id | INTEGER | Foreign Key to `users`, `ON DELETE SET NULL` |
| error_type | TEXT | NOT NULL |
| message | TEXT | NOT NULL |
| module | TEXT | Module where the error occurred |
| created_at | TEXT | NOT NULL, timestamp |

This table exists in the current schema. Application-level error logging is planned for a later reliability milestone.

---

# 8. Backup History Table

The `backup_history` table is defined for recording backup and restore operations.

| Field | Type | Constraints / Purpose |
|---|---|---|
| id | INTEGER | Primary Key |
| operation | TEXT | NOT NULL, CHECK: Backup / Restore |
| file_path | TEXT | NOT NULL |
| status | TEXT | Operation result |
| initiated_by | INTEGER | Foreign Key to `users`, `ON DELETE SET NULL` |
| created_at | TEXT | NOT NULL, timestamp |
| description | TEXT | Additional operation information |

Backup and recovery service/GUI functionality is planned for a later milestone.

---

# 9. Database Relationships

```text
                 +----------------+
                 |     users      |
                 +----------------+
                  |      |      |
                  |      |      +--------------------+
                  |      |                           |
                  v      v                           v
            audit_logs  backup_history          error_logs

                 employees
            (independent master data)
```

The foreign-key relationships connect system activity and operational history to the user account that initiated an operation where applicable.

---

# 10. Reliability Controls

The database design supports reliability through:

- Primary keys for record identity.
- UNIQUE constraints for usernames, employee codes, and employee emails.
- NOT NULL constraints for required data.
- CHECK constraints for roles, account status, employee status, salary, and backup operation type.
- Foreign keys for traceability relationships.
- Parameterized SQL in implemented service operations.
- Transaction commit/rollback handling in implemented write operations.
- Application-level validation before employee database operations.

---

# 11. Implementation Status

### Implemented

- SQLite connection layer.
- Current database schema.
- User authentication data.
- Employee CRUD/deactivation service operations.
- Employee search service.
- Audit-log creation, retrieval, and search service.
- Employee input validation.

### Planned

- Backup creation and restore workflow.
- Backup history service integration.
- Application-level error-log integration.
- GUI screens for User Management, Audit Logs, and Backup & Recovery.
