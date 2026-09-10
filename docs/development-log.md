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
## Commit 18 — Implement employee listing service

**Objective:**  
Implement reliable retrieval of all employee records from the database.

**Work completed:**
- Added `get_all_employees()` to the employee service.
- Retrieved all employee fields from the `employees` table.
- Reused the existing employee row-to-dictionary conversion.
- Ordered employee records by database ID.
- Ensured database connections are closed after retrieval.

**Testing:**
- Existing employee records were retrieved successfully.
- Employee records were returned as dictionaries.
- Employee count was verified successfully.
- Application startup and login flow remained functional.
- No unexpected error occurred during testing.

**Status:** Completed.
## Commit 19 — Implement employee search service

**Objective:**  
Implement reliable employee search functionality using common employee fields.

**Work completed:**
- Added `search_employees()` to the employee service.
- Added search by employee code.
- Added search by full name.
- Added search by email.
- Added search by department.
- Added partial text matching.
- Added handling for empty search terms.
- Used parameterized SQL queries.
- Ensured database connections are closed after searching.

**Testing:**
- Employee code search was tested successfully.
- Employee name search was tested successfully.
- Department search was tested successfully.
- Partial search was tested successfully.
- No-match search correctly returned an empty list.
- Empty search correctly returned an empty list.
- Application startup and login flow remained functional.
- No unexpected error occurred during testing.

**Status:** Completed.
## Commit 20 — Implement employee update service

**Objective:**  
Implement reliable updating of existing employee records.

**Work completed:**
- Added `update_employee()` to the employee service.
- Added required-field validation.
- Added negative salary validation.
- Updated employee details using the employee database ID.
- Preserved the existing employee ID and creation timestamp.
- Updated `updated_at` when employee details are changed.
- Used parameterized SQL queries.
- Added transaction commit and rollback handling.
- Ensured database connections are closed properly.
- Returned `False` when the specified employee does not exist.

**Testing:**
- Existing employee record was updated successfully.
- Updated employee details were verified successfully.
- Non-existing employee ID correctly returned `False`.
- Negative salary was correctly rejected by validation.
- Application startup and login flow remained functional.
- No unexpected error occurred during testing.

**Status:** Completed.
## Commit 21 — Implement employee deactivation

**Objective:**  
Implement safe employee deactivation using a soft-delete approach.

**Work completed:**
- Added `deactivate_employee()` to the employee service.
- Changed employee status from `Active` to `Inactive`.
- Preserved the employee record instead of permanently deleting it.
- Updated `updated_at` during deactivation.
- Added transaction commit and rollback handling.
- Ensured database connections are closed properly.
- Returned `False` when the employee does not exist or is already inactive.

**Testing:**
- Existing employee was successfully deactivated.
- Employee record remained available in the database after deactivation.
- Employee status was verified as `Inactive`.
- Already inactive employee correctly returned `False`.
- Non-existing employee ID correctly returned `False`.
- Application startup and login flow remained functional.
- No unexpected error occurred during testing.

**Status:** Completed.
## Commit 22 — Implement user management service foundation

**Objective:**  
Create the initial user management service for safely retrieving user records without exposing password hashes.

**Work completed:**
- Created `services/user_service.py`.
- Added user retrieval by database ID.
- Added retrieval of all users.
- Added user row-to-dictionary conversion.
- Excluded password hashes from returned user data.
- Ordered users by database ID.
- Ensured database connections are closed after retrieval.

**Testing:**
- All existing users were retrieved successfully.
- User count was verified successfully.
- Existing user lookup by ID was successful.
- Non-existing user lookup correctly returned `None`.
- Password hashes were not exposed by the service.
- Application startup and login flow remained functional.
- Employee role access restrictions remained functional.
- No unexpected error occurred during testing.

**Status:** Completed.
## Commit 23 — Implement user activation and deactivation

**Objective:**  
Implement safe activation and deactivation of user accounts.

**Work completed:**
- Added `deactivate_user()` to the user service.
- Added `activate_user()` to the user service.
- Changed user account status without deleting user records.
- Added transaction commit and rollback handling.
- Ensured database connections are closed properly.
- Returned `False` when the requested status change was not applicable.

**Testing:**
- Employee test account was successfully deactivated.
- Inactive status was verified in the database.
- Already inactive account correctly returned `False`.
- Employee test account was successfully reactivated.
- Active status was verified after reactivation.
- Already active account correctly returned `False`.
- Non-existing user correctly returned `False`.
- Employee login worked successfully after reactivation.
- No unexpected error occurred during testing.

**Status:** Completed.
## Commit 24 — Strengthen role restrictions and RBAC

**Objective:**  
Strengthen role-based access control by adding explicit permission enforcement for protected operations.

**Work completed:**
- Enhanced `services/access_control.py`.
- Added `require_permission()` for enforcing permission checks.
- Kept role-based permission mappings for Admin, HR, and Employee.
- Added safe handling for missing users and invalid roles.
- `require_permission()` raises `PermissionError` when a user does not have the required permission.

**Testing:**
- Admin was allowed to manage users.
- Admin was allowed to manage employees.
- HR was denied user-management permission.
- HR was allowed to manage employees.
- Employee was denied user-management permission.
- Employee was allowed to view employees.
- `require_permission()` successfully allowed authorized operations.
- Unauthorized Employee access to `manage_users` correctly raised `PermissionError`.
- `services/access_control.py` compiled successfully.
- `main.py` compiled successfully.
- No unexpected project error occurred during testing.

**Status:** Completed.
## Commit 25 — Implement audit logging foundation

**Objective:**  
Implement a reusable audit logging service and record successful user login activity.

**Work completed:**
- Added `services/audit_service.py`.
- Implemented `create_audit_log()` for storing system activity.
- Added transaction commit and rollback handling.
- Ensured database connections are closed properly.
- Integrated successful login auditing into `authenticate_user()`.
- Recorded user ID, username, action, target type, target ID, description, and status.

**Testing:**
- Audit logging service compiled successfully.
- Direct audit-log insertion was verified in the database.
- Application login using the `employee_test` account completed successfully.
- A real `LOGIN` audit record was created and verified in the database.
- Verified audit record:
  - User ID: `3`
  - Username: `employee_test`
  - Action: `LOGIN`
  - Target Type: `User`
  - Target ID: `3`
  - Status: `Success`
- No unexpected error occurred during testing.

**Status:** Completed.
## Commit 26 — Implement audit log viewer and search service

**Objective:**  
Implement service-layer functionality to retrieve and search audit log records.

**Work completed:**
- Added audit log row-to-dictionary conversion.
- Implemented `get_all_audit_logs()`.
- Implemented `search_audit_logs()`.
- Added searching by username, action, target type, and description.
- Added newest-first ordering for audit records.
- Used parameterized SQL queries for search operations.
- Safely handled empty search terms.

**Testing:**
- Audit log retrieval completed successfully.
- Existing audit records were returned correctly.
- `LOGIN` action search worked correctly.
- Username search for `employee_test` worked correctly.
- Empty search returned an empty list.
- All affected Python files compiled successfully.
- No unexpected error occurred during testing.

**Status:** Completed.
## Commit 27 — Implement input validation

**Objective:**  
Strengthen employee data validation before database operations.

**Work completed:**
- Added `services/validation_service.py`.
- Implemented reusable required-field validation.
- Added email format validation.
- Added phone format validation.
- Added numeric and non-negative salary validation.
- Integrated common validation into employee creation.
- Integrated common validation into employee update.
- Preserved existing database constraints.

**Testing:**
- Valid email, phone, and salary values were accepted.
- Invalid email was rejected.
- Invalid phone was rejected.
- Negative salary was rejected.
- Non-numeric salary was rejected.
- Valid employee creation completed successfully.
- Created employee was successfully retrieved from SQLite.
- Application startup and existing functionality remained operational.
- No unexpected error occurred during testing.

**Status:** Completed.