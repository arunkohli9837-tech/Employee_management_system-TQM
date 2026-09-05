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
- Added a centralized role-permission mapping.
- Added permission checking functionality.
- Added role checking functionality.
- Added support for checking whether a user belongs to any of a set of allowed roles.
- Connected RBAC checks with the role information maintained by the current-user session.

**Testing:**
- Existing Admin account is used for RBAC testing.
- Admin role and Admin permissions are verified.
- HR and Employee login testing is not performed at this stage because those accounts have not yet been created.

**Status:** In progress.