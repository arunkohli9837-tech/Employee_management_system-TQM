# Employee Management System
## Application Architecture

---

## 1. Purpose

This document describes the application architecture used by the Employee Management System and distinguishes currently implemented components from functionality planned for later milestones.

The architecture keeps the user interface, service/business logic, validation, and database responsibilities separated so the system can be developed, tested, and improved incrementally.

---

## 2. Architecture Style

The application uses a simple layered architecture suitable for a Python desktop application.

### Layers

1. **Presentation Layer** — CustomTkinter screens and user interaction.
2. **Service / Business Logic Layer** — authentication, authorization, validation, employee/user/audit operations, and later backup/recovery operations.
3. **Database Layer** — SQLite connection management, schema initialization, queries, transactions, and database constraints.

Cross-cutting reliability and security controls are implemented within the appropriate layer rather than being placed only in the GUI.

---

## 3. Current Project Structure

```text
Employee Management System
│
├── main.py
│   └── Application entry point and top-level screen navigation
│
├── ui/
│   ├── login.py
│   ├── dashboard.py
│   ├── employees.py
│   ├── users.py
│   ├── audit_logs.py
│   └── backup.py
│
├── services/
│   ├── auth_service.py
│   ├── access_control.py
│   ├── session.py
│   ├── validation_service.py
│   ├── employee_service.py
│   ├── user_service.py
│   ├── audit_service.py
│   └── backup_service.py
│
├── database/
│   ├── database.py
│   └── schema.sql
│
├── docs/
│   ├── requirements.md
│   ├── architecture.md
│   ├── development-log.md
│   ├── error-log.md
│   └── diagrams/
│
├── data/
├── backups/
└── logs/
```

The exact project contents may grow as later milestones are implemented.

---

## 4. High-Level Architecture

```text
+-----------------------------------------------------------+
|                  PRESENTATION LAYER                      |
|                   CustomTkinter GUI                      |
|                                                          |
| Login → Dashboard → Feature screens                      |
|                                                          |
| Users | Audit Logs | Backup & Recovery                   |
+------------------------------+----------------------------+
                               |
                               v
+-----------------------------------------------------------+
|              SERVICE / BUSINESS LOGIC LAYER              |
|                                                          |
| Authentication | Session | Authorization | Validation    |
| Employee Operations | User Operations | Audit Operations |
| Backup / Recovery Operations                             |
+------------------------------+----------------------------+
                               |
                               v
+-----------------------------------------------------------+
|                    DATABASE LAYER                        |
|                                                          |
| database.py | SQLite / sqlite3 | Schema Initialization   |
| Queries | Parameterized SQL | Transactions | Constraints |
+------------------------------+----------------------------+
                               |
                               v
+-----------------------------------------------------------+
|                     SQLite DATABASE                      |
| Users | Employees | Audit Logs | Error Logs              |
| Backup History                                           |
+-----------------------------------------------------------+
```

---

## 5. Responsibility of Each Layer

### 5.1 Presentation Layer

The GUI is responsible for: 

- Collecting user input.
- Displaying application information and results.
- Showing validation feedback.
- Triggering service-layer operations.
- Handling top-level screen navigation through callbacks managed by `main.py`.

The GUI is **not** responsible for direct SQL database operations.

### 5.2 Service / Business Logic Layer

The service layer is responsible for: 

- Authentication and password verification.
- Session state.
- Role and permission enforcement.
- Employee CRUD/deactivation operations.
- Reusable input validation.
- User account operations.
- Audit logging and audit retrieval/search.
- Transaction commit/rollback handling in implemented database operations.

Backup and recovery operations are implemented through `services/backup_service.py` and exposed through the Backup & Recovery GUI.

### 5.3 Database Layer

The database layer is responsible for: 

- SQLite connection creation.
- Schema initialization.
- Database access through `sqlite3`.
- Database constraints.
- Supporting transactions used by service operations.

---

## 6. Navigation Responsibility

Top-level screen navigation is handled by `main.py`.

Current flow:

```text
LoginFrame
    ↓ successful login
EmployeeManagementApp
    ↓
DashboardFrame
    ├── Employee Management
    ├── User Management
    ├── Audit Logs
    └── Backup & Recovery
```

Top-level navigation is coordinated by `main.py`, while the Dashboard keeps the sidebar fixed and displays the selected feature in the content area. The feature screens no longer require a visible Back to Dashboard button because the fixed sidebar provides navigation.

This avoids making individual GUI frames responsible for recreating other top-level screens.

---

## 7. Reliability and Security Placement

Reliability is supported through multiple layers:

- GUI input validation and understandable feedback.
- Reusable validation in the service layer.
- Parameterized SQL.
- SQLite `NOT NULL`, `UNIQUE`, `CHECK`, and foreign-key constraints where defined by the schema.
- Transaction commit/rollback handling in implemented write operations.
- Soft deactivation instead of permanent deletion for employees and users.
- Audit logging for implemented auditable operations.
- Backup creation, SQLite integrity validation, safety backup before restore, and restore recovery handling.

Security is supported through:

- Password hashing.
- Current-user session handling.
- Role-based permissions.
- Service-level `require_permission()` enforcement.
- Inactive-account authentication restrictions.

Backup/recovery and broader application error logging are planned reliability milestones and should not be treated as completed until recorded as such in the development log.

---

## 8. Planned Architectural Evolution

The architecture will remain layered as new features are added. Future milestones are expected to extend the existing structure rather than introduce unnecessary technologies.

Remaining planned additions include:

- Stronger centralized error handling and recovery.
- Application-level error logging.
- TQM reliability analysis documentation based on actual project data.

Any architectural change will be documented when it is actually implemented.
