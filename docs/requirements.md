# Employee Management System
## Software Requirements Specification

---

## 1. Project Overview

The Employee Management System is a desktop-based application intended to manage employee information and related administrative activities in a structured and reliable manner.

The application will be developed using Python with CustomTkinter for the desktop graphical user interface and SQLite for local data storage.

The system will provide controlled access to employee and user information through authentication and role-based permissions.

The project is being developed as an academic software project with a particular focus on software reliability and systematic development.

---

## 2. Problem Statement

Organizations need to maintain employee information accurately and make that information available to authorized users when required.

Managing employee records without a structured application can create difficulties such as:

- Inconsistent employee information
- Difficulty locating records
- Accidental data modification
- Duplicate records
- Unauthorized access
- Lack of traceability for important operations
- Risk of data loss
- Difficulty recovering from failures

The Employee Management System is intended to provide a structured desktop solution for managing employee information while improving data accuracy, access control, traceability, and reliability.

---

## 3. Project Objectives

The primary objectives of the project are:

1. To develop a desktop-based Employee Management System.
2. To maintain employee records in a structured database.
3. To provide secure user authentication.
4. To implement role-based access control.
5. To provide employee creation, viewing, searching, updating, and deactivation functionality.
6. To validate important user input before storing data.
7. To maintain audit information for important operations.
8. To handle application and database failures safely.
9. To provide database backup and recovery mechanisms.
10. To verify the system through structured testing.
11. To demonstrate software reliability as part of the TQM assignment.

---

## 4. Project Scope

### 4.1 In Scope

The planned system will cover:

- User authentication
- User and role management
- Employee management
- Employee search
- Employee information updates
- Employee deactivation
- Input validation
- Database constraints
- Role-based access control
- Audit logging
- Error handling
- Database backup and recovery
- Testing and reliability verification
- Project documentation

### 4.2 Out of Scope

The initial project scope does not include:

- Payroll processing
- Attendance tracking
- Leave management
- Recruitment management
- Performance appraisal
- Cloud-based multi-organization deployment
- Mobile application development
- Integration with external enterprise systems

These areas may be considered as future enhancements if required.

---

## 5. Target Users

The planned system will support the following user roles.

### 5.1 Administrator

The Administrator will manage system-level users, roles, access, and administrative operations.

Expected responsibilities include:

- Managing user accounts
- Assigning roles
- Activating or deactivating accounts
- Monitoring important system activity
- Accessing administrative functions

### 5.2 HR User

The HR user will primarily work with employee information.

Expected responsibilities include:

- Adding employees
- Viewing employee information
- Searching employee records
- Updating employee information
- Deactivating employee records where authorized

### 5.3 Employee

The Employee role will have restricted access appropriate to an individual employee account.

The exact accessible functionality will be finalized during authentication and authorization design.

---

# 6. Functional Requirements

## 6.1 Authentication Requirements

### FR-AUTH-01
The system shall provide a login mechanism for registered users.

### FR-AUTH-02
The system shall authenticate users using a username and password.

### FR-AUTH-03
User passwords shall not be stored as plain text.

### FR-AUTH-04
The system shall maintain an account status for users.

### FR-AUTH-05
The system shall provide logout functionality.

### FR-AUTH-06
The system shall maintain the identity of the currently authenticated user during an active session.

---

## 6.2 User Management Requirements

### FR-USER-01
An authorized administrator shall be able to create user accounts.

### FR-USER-02
An authorized administrator shall be able to update user account information.

### FR-USER-03
An authorized administrator shall be able to assign valid roles.

### FR-USER-04
An authorized administrator shall be able to activate or deactivate user accounts.

### FR-USER-05
The system shall allow authorized users to search or view user information where applicable.

### FR-USER-06
The system shall restrict user-management operations according to the user's role.

---

## 6.3 Role-Based Access Requirements

### FR-RBAC-01
The system shall support the following planned roles:

- Admin
- HR
- Employee

### FR-RBAC-02
The system shall restrict sensitive operations according to role permissions.

### FR-RBAC-03
Authorization checks shall be applied at the service or business-logic level and not only by hiding GUI controls.

### FR-RBAC-04
The system shall prevent unauthorized users from performing restricted operations.

---

## 6.4 Employee Management Requirements

### FR-EMP-01
Authorized users shall be able to create employee records.

### FR-EMP-02
Authorized users shall be able to view employee records.

### FR-EMP-03
Authorized users shall be able to search employee records.

### FR-EMP-04
Authorized users shall be able to update employee records.

### FR-EMP-05
Authorized users shall be able to deactivate employee records.

### FR-EMP-06
Employee deactivation should preserve the historical record instead of permanently deleting it.

### FR-EMP-07
The system shall maintain appropriate employee information such as:

- Employee ID
- Employee Code
- Full Name
- Email
- Phone
- Department
- Designation
- Salary
- Joining Date
- Status
- Created At
- Updated At

The final field set may be refined during database design if a genuine requirement or implementation constraint is identified.

---

## 6.5 Search and Filtering Requirements

### FR-SEARCH-01
The system shall provide employee search functionality.

### FR-SEARCH-02
Search shall use relevant employee information such as employee code, name, email, or other appropriate fields.

### FR-SEARCH-03
Search results shall reflect the actual data stored in the database.

### FR-SEARCH-04
Search functionality shall not modify stored employee data.

---

## 6.6 Input Validation Requirements

### FR-VALID-01
Required input fields shall be validated before database operations.

### FR-VALID-02
Employee code shall be validated before insertion or update.

### FR-VALID-03
Email input shall be validated according to the selected format rules.

### FR-VALID-04
Phone input shall be validated according to the selected format rules.

### FR-VALID-05
Salary input shall be validated as numeric data.

### FR-VALID-06
Negative salary values shall not be accepted.

### FR-VALID-07
Joining date input shall be validated according to the required date format.

**Current implementation:** Joining dates are accepted in `DD-MM-YYYY` format and invalid calendar dates are rejected.

### FR-VALID-08
Invalid input shall be rejected with understandable user feedback.

The currently implemented joining-date format is `DD-MM-YYYY`. Other validation formats and length limits may be refined during implementation when a genuine requirement or technical constraint is identified.

---

## 6.7 Audit Logging Requirements

### FR-AUDIT-01
The system shall maintain audit information for important user and system operations.

### FR-AUDIT-02
Audit records should contain appropriate information such as:

- User ID
- Username
- Action
- Target Type
- Target ID
- Description
- Status
- Timestamp

### FR-AUDIT-03
Important operations such as employee changes, account management, authentication events, and backup/recovery operations shall be considered for audit logging.

### FR-AUDIT-04
Audit records shall provide traceability for important operations.

The exact list of audited operations will correspond to the functionality actually implemented.

---

## 6.8 Error Handling Requirements

### FR-ERROR-01
The application shall handle expected application and database failures without unnecessarily terminating the application.

### FR-ERROR-02
Database-related failures shall be handled appropriately.

### FR-ERROR-03
Database transactions shall be rolled back when necessary to prevent partial updates.

### FR-ERROR-04
Users shall receive understandable error messages rather than raw technical exceptions where appropriate.

### FR-ERROR-05
Technical error information shall be retained in an appropriate logging mechanism where required.

---

## 6.9 Backup and Recovery Requirements

### FR-BACKUP-01
The system shall support database backup.

### FR-BACKUP-02
The system should support automatic backup at an appropriate application lifecycle point.

### FR-BACKUP-03
The system should support manual database backup.

### FR-BACKUP-04
The system should maintain backup history where appropriate.

### FR-BACKUP-05
A selected backup should be validated before restoration.

### FR-BACKUP-06
The system should verify that a selected file is a valid SQLite database before restoring it.

### FR-BACKUP-07
A safety backup of the current database should be created before a restore operation.

### FR-BACKUP-08
The restore operation should require explicit confirmation.

### FR-BACKUP-09
Backup and restore operations should be traceable through appropriate logging.

The detailed backup and recovery workflow will be finalized during implementation.

---

# 7. Non-Functional Requirements

## 7.1 Reliability

### NFR-REL-01
The system should preserve valid existing data when an operation fails.

### NFR-REL-02
Database operations should use appropriate transaction handling.

### NFR-REL-03
Important database integrity rules should be enforced using database constraints where appropriate.

### NFR-REL-04
The system should recover safely from expected operational failures.

### NFR-REL-05
Backup and restore mechanisms should reduce the risk of permanent data loss.

### NFR-REL-06
Reliability-related features shall be tested before final release.

---

## 7.2 Security

### NFR-SEC-01
Passwords shall never be stored as plain text.

### NFR-SEC-02
Password handling shall use an appropriate password hashing mechanism.

### NFR-SEC-03
Access to protected functionality shall be controlled by user role.

### NFR-SEC-04
Authorization shall be enforced beyond the visual GUI layer.

### NFR-SEC-05
Inactive accounts shall not be allowed to authenticate.

### NFR-SEC-06
Sensitive administrative operations should require appropriate authorization.

---

## 7.3 Usability

### NFR-USE-01
The application should provide a clear desktop interface.

### NFR-USE-02
Navigation should be understandable to intended users.

### NFR-USE-03
Validation feedback should be clear and understandable.

### NFR-USE-04
Destructive or potentially irreversible operations should provide appropriate confirmation.

### NFR-USE-05
The interface should maintain consistent layout, labels, and controls.

---

## 7.4 Performance

### NFR-PERF-01
Normal operations should respond within a reasonable time on the intended local system.

### NFR-PERF-02
Database queries should be designed appropriately for the expected project data size.

### NFR-PERF-03
The application should avoid unnecessary repeated database operations.

Exact performance targets may be refined after the application structure and expected data volume become clearer.

---

## 7.5 Maintainability

### NFR-MAIN-01
The application should use a modular structure.

### NFR-MAIN-02
Database, business logic, and user-interface responsibilities should be separated where practical.

### NFR-MAIN-03
Important design and development decisions should be documented.

### NFR-MAIN-04
The Git history should contain meaningful development milestones.

---

# 8. Database Requirements

The application shall use SQLite as the primary local database.

The database design is expected to contain areas for:

- Users
- Employees
- Audit logs
- Error logs
- Backup history

Additional tables may be introduced when genuinely required.

The database should use appropriate:

- Primary keys
- Foreign keys
- Unique constraints
- NOT NULL constraints
- CHECK constraints
- Transactions

Database reliability settings will be evaluated during database implementation rather than being assumed at this stage.

---

# 9. Hardware and Software Requirements

## 9.1 Software Requirements

The development environment is expected to include:

- Python
- Python virtual environment (`venv`)
- Git
- GitHub account/repository
- A code editor or IDE
- Supported operating system capable of running Python and CustomTkinter

## 9.2 Hardware Requirements

The application is intended to run on a typical modern desktop or laptop suitable for Python desktop application development.

Expected minimum practical requirements include:

- Standard x64 desktop/laptop processor
- At least 4 GB RAM
- Sufficient local storage for source code, database, backups, and development tools

These requirements are approximate and may be refined if actual application requirements indicate otherwise.

---

# 10. Security Requirements

The security design shall include:

- Username-based authentication
- Password hashing
- Account status management
- Role-based permissions
- Protected administrative functions
- Session/current-user handling
- Logout
- Auditability of important security-related operations

Security controls shall be implemented progressively and tested before being considered complete.

---

# 11. Reliability Requirements

Reliability is the primary TQM focus of this project.

The system should improve reliability through:

- Input validation
- Database constraints
- Safe transactions
- Error handling
- Error recovery
- Backup
- Restore validation
- Safety backup before restore
- Audit logging
- Role-based access control
- Soft employee deactivation
- Functional and reliability testing

Reliability claims shall be based on implemented and tested functionality rather than assumptions.

---

## 11.1 Current Implementation Snapshot

At the current development stage, the following requirements have corresponding implemented functionality:

- User authentication and logout
- Current-user session handling
- Role-based permission mapping and service-level permission enforcement
- Employee creation, viewing, searching, updating, and soft deactivation at the service layer
- Employee input validation for required fields, email, phone, salary, and joining date
- Joining date validation in `DD-MM-YYYY` format
- Audit-log creation for successful authentication events
- Audit-log retrieval and search at the service layer
- Dashboard and Employee Management GUI navigation
- Employee viewing and search through the GUI
- Add Employee operation through the GUI

Features such as User Management GUI, Audit Logs GUI, Backup & Recovery GUI, application-wide error logging/recovery, and the remaining TQM analysis artifacts are planned for later milestones unless a later development log entry records their completion.

---

# 12. TQM Quality Focus

The project focuses on:

**Q01 — Improve Reliability**

The reliability objective is to reduce the likelihood and impact of invalid operations, unauthorized actions, inconsistent data, application failures, and data loss.

The development process will use a continuous improvement approach:

```text
Identify Requirements
        ↓
Design the Solution
        ↓
Implement Incrementally
        ↓
Test
        ↓
Identify Actual Problems
        ↓
Apply Improvements
        ↓
Retest
        ↓
Document Results