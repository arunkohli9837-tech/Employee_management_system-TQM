# Development Log

## Project: Employee Management System

This document records the actual development progress of the Employee Management System. Each entry corresponds to a meaningful development commit.

---

## Commit 01 — Initialize project foundation

**Objective:**  
Initialize the Employee Management System project and establish the basic project foundation.

**Work completed:**
- Created the initial project repository structure.
- Established the starting point for further development.

**Status:** Completed.

---

## Commit 02 — Add README and project overview

**Objective:**  
Document the project purpose and provide an initial overview of the Employee Management System.

**Work completed:**
- Added README documentation.
- Documented the project overview and initial purpose.

**Status:** Completed.

---

## Commit 03 — Add project requirements documentation

**Objective:**  
Document the functional and reliability requirements of the system.

**Work completed:**
- Added project requirements documentation.
- Defined the initial system requirements and scope.

**Status:** Completed.

---

## Commit 04 — Set up Python virtual environment and dependencies

**Objective:**  
Prepare an isolated Python development environment and define project dependencies.

**Work completed:**
- Set up the Python virtual environment.
- Configured project dependencies.

**Status:** Completed.

---

## Commit 05 — Create initial CustomTkinter application entry point

**Objective:**  
Create the initial executable application entry point.

**Work completed:**
- Created the initial CustomTkinter application.
- Established the main application entry point.

**Status:** Completed.

---

## Commit 06 — Define application architecture

**Objective:**  
Establish a modular architecture for the Employee Management System.

**Work completed:**
- Defined the application architecture.
- Organized the project into appropriate application layers/modules.

**Status:** Completed.

---

## Commit 07 — Add initial system flow documentation

**Objective:**  
Document the expected system flow before implementing additional functionality.

**Work completed:**
- Added system flow documentation.
- Documented the initial application process.

**Status:** Completed.

---

## Commit 08 — Document initial database design

**Objective:**  
Document the initial database structure and data design.

**Work completed:**
- Added initial database design documentation.
- Defined the initial database structure required by the application.

**Status:** Completed.

---

## Commit 09 — Implement SQLite database connection

**Objective:**  
Provide the application with a reusable SQLite database connection.

**Work completed:**
- Implemented the SQLite database connection layer.
- Established the database access foundation.

**Status:** Completed.

---

## Commit 10 — Create initial SQLite database schema

**Objective:**  
Create the initial database schema required by the system.

**Work completed:**
- Added the initial SQLite schema.
- Established the initial database tables and constraints.

**Status:** Completed.

---

## Commit 11 — Implement authentication service foundation

**Objective:**  
Create the authentication service responsible for validating user login credentials.

**Work completed:**
- Implemented the authentication service foundation.
- Connected authentication logic with the database user information.

**Status:** Completed.

---

## Commit 12 — Implement secure password handling

**Objective:**  
Improve password security by implementing secure password handling.

**Work completed:**
- Added password hashing functionality.
- Added secure password verification functionality.
- Integrated password handling with authentication.

**Status:** Completed.

---

## Commit 13 — Add login UI

**Objective:**  
Provide a graphical login interface for the authentication system.

**Work completed:**
- Added the login user interface using CustomTkinter.
- Added username and password input fields.
- Added password masking.
- Added login validation.
- Connected the login UI with the existing authentication service.
- Added successful-login callback handling.

**Testing:**
- Login functionality was tested using the existing Admin account.

**Status:** Completed.

---

## Commit 14 — Add current user session handling

**Objective:**  
Maintain the identity and role of the authenticated user during application execution.

**Work completed:**
- Added a session management component.
- Added current-user storage.
- Added login state checking.
- Added session logout support.
- Connected successful authentication with the application session.

**Testing:**
- Existing Admin login was tested successfully.

**Issue encountered:**
- A `KeyError: 'is_active'` occurred during session creation because the authentication result did not contain an `is_active` field.

**Resolution:**
- Updated session handling to store only the user fields currently provided by the authentication service: `id`, `username`, and `role`.

**Verification:**
- Admin login was retested successfully after the correction.

**Status:** Completed.

---

## Commit 15 — Implement initial Role-Based Access Control

**Objective:**  
Establish the initial Role-Based Access Control (RBAC) foundation for controlling system permissions according to user roles.

**Planned roles:**
- Admin
- HR
- Employee

**Work completed:**
- Added centralized role-permission mapping.
- Added permission checking functionality.
- Added role checking functionality.
- Added support for checking multiple allowed roles.
- Connected RBAC checks with the current-user session role.

**Testing:**
- Admin role was tested successfully.
- Admin permissions were verified successfully.
- HR and Employee accounts were created for authentication testing.
- HR and Employee login were tested successfully.

**Status:** Completed.
## Commit 16 — Create employee database functionality

**Objective:**  
Create the database service foundation for accessing employee records.

**Work completed:**
- Added `services/employee_service.py`.
- Added employee database-row to dictionary conversion.
- Added employee lookup by database ID.
- Used the existing SQLite database connection layer.
- Ensured database connections are closed after the operation.

**Testing:**
- Application startup was tested successfully.
- Admin login was tested successfully.
- HR login was tested successfully.
- Employee login was tested successfully.
- Employee lookup with a non-existing ID was tested and correctly returned `None`.
- No unexpected error occurred during testing.

**Status:** Completed.
## Commit 17 — Implement employee creation service

**Objective:**  
Implement reliable employee record creation through the employee service layer.

**Work completed:**
- Added `create_employee()` to the employee service.
- Added required-field validation.
- Added negative salary validation.
- Added database insertion using parameterized SQL.
- Added transaction commit on successful insertion.
- Added transaction rollback on insertion failure.
- Ensured database connections are closed properly.
- Returned the newly created employee database ID.

**Testing:**
- New employee record was created successfully.
- Created employee was retrieved successfully using its database ID.
- Duplicate employee code was correctly rejected by the database unique constraint.
- Application startup and login flow remained functional.
- No unexpected error occurred during testing.

**Status:** Completed.