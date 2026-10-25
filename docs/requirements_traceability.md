# Requirements Traceability Matrix

| ID | Requirement | Implementation location | Verification method | Status |
|---|---|---|---|---|
| FR-AUTH-01 | Registered users can log in | `services/auth_service.py`, `ui/login.py` | Valid/invalid login test and live demo | Implemented; live demo pending |
| FR-AUTH-03 | Passwords are not stored as plain text | `services/password_service.py`, `services/auth_service.py` | Inspect stored hash and verify login | Implemented; test evidence should be captured |
| FR-USER-01 | Admin can create user accounts | `services/user_service.py`, `ui/users.py` | Create user as Admin | Implemented; live demo pending |
| FR-RBAC-01 | Roles are Admin, HR and Employee | `services/access_control.py`, `database/schema.sql` | Role tests and restricted-role demo | Implemented |
| FR-EMP-01 | Create employee | `services/employee_service.py`, `ui/employees.py` | REL test and GUI demo | Implemented |
| FR-EMP-02 | Read/search employee | `services/employee_service.py`, `ui/employees.py` | Search and retrieve test | Implemented |
| FR-EMP-03 | Update employee | `services/employee_service.py`, `ui/employees.py` | Update test | Implemented |
| FR-EMP-04 | Deactivate employee without hard deletion | `services/employee_service.py`, `ui/employees.py` | Verify status becomes Inactive | Implemented |
| FR-VAL-01 | Validate required fields/email/phone/salary/date | `services/validation_service.py` | Invalid-input tests | Implemented |
| FR-DB-01 | Roll back failed write transactions | `database/database.py` | Intentional exception test | Implemented and tested |
| FR-AUD-01 | Store and retrieve audit events | `services/audit_service.py`, `ui/audit_logs.py` | Audit persistence test and GUI demo | Implemented; test included |
| FR-BKP-01 | Create/validate database backups | `services/backup_service.py`, `ui/backup.py` | Backup integrity test | Implemented; tests included |
| FR-BKP-02 | Recover from a valid backup | `services/backup_service.py` | Restore test in temporary database | Implemented; tests included |
| FR-ERR-01 | Log unexpected exceptions without exposing technical detail in UI | `services/error_handler.py` | Simulated logging failure test | Implemented; tests included |

| FR-PAY-01/02 | Create monthly payroll record and calculate net pay | `services/hr_operations_service.py`, `ui/hr_operations.py`, `database/schema.sql` | Payroll service tests and GUI demo | Implemented; live GUI demo pending |
| FR-PAY-03 | Prevent duplicate employee/pay-period payroll | `database/schema.sql` | Duplicate payroll test | Implemented; test included |
| FR-PERF-01/02 | Record dated performance rating/comments with validation | `services/hr_operations_service.py`, `ui/hr_operations.py`, `database/schema.sql` | Performance-log tests and GUI demo | Implemented; test included |
| FR-PERF-03 | Audit payroll/performance operations | `services/hr_operations_service.py` | Inspect audit log after creating records | Implemented; live demo pending |

## Scope note

Payroll is a simplified academic calculation (basic salary − deductions + bonus). Statutory tax, PF, ESI, attendance deductions and advanced appraisal workflows are outside the current scope.
