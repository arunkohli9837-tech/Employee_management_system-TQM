# Employee Management System — System Flow

## Purpose

This diagram represents the current application flow after the implemented authentication, session, dashboard, Employee Management, search, and Add Employee milestones.

Features not yet implemented in the GUI are explicitly marked as planned rather than shown as completed flows.

---

## Current High-Level Flow

```mermaid
flowchart TD
    A[Start Application] --> B[Login Screen]
    B --> C[Enter Username and Password]
    C --> D{Authentication Successful?}

    D -- No --> E[Show Login Feedback]
    E --> B

    D -- Yes --> F[Create Current User Session]
    F --> G[Dashboard]

    G --> H{Select Authorized Option}

    H --> I[Employee Management]
    H --> J[Planned User Management]
    H --> K[Planned Audit Logs]
    H --> L[Planned Backup & Recovery]

    I --> M[Load Employee Records]
    M --> N{Search Required?}
    N -- Yes --> O[Search Employee Records]
    N -- No --> P[Display Employee Records]
    O --> P

    P --> Q{Employee Operation}
    Q --> R[Add Employee]
    Q --> S[Planned Select / Update / Deactivate GUI Actions]

    R --> T[Validate Employee Input]
    T --> U{Input Valid?}
    U -- No --> V[Show Validation Feedback]
    V --> R
    U -- Yes --> W[Create Employee Service]
    W --> X[SQLite Database]
    X --> Y[Refresh Employee Records]
    Y --> P

    P --> Z[Back to Dashboard]
    Z --> G

    G --> AA[Logout]
    AA --> AB[Clear Session]
    AB --> B
```

---

## 2. Current Layered Operation Flow

```text
GUI
 ↓
Service Layer
 ↓
Validation / Business Rules
 ↓
Database Layer
 ↓
SQLite
```

For employee creation, the current flow is:

```text
Add Employee Form
       ↓
Collect Input
       ↓
validate_employee_fields()
       ↓
Valid? ── No → User Feedback
       ↓ Yes
create_employee()
       ↓
SQLite INSERT
       ↓
Commit
       ↓
Refresh Employee List
```

---

## 3. Navigation Flow

Top-level navigation is coordinated by `main.py` through callbacks.

```text
Login
  ↓
Dashboard
  ↓
Employee Management
  ↓
Back
  ↓
Dashboard
  ↓
Logout
  ↓
Login
```

---

## 4. Planned Extensions

The following flows will be documented in more detail when their implementation milestones are completed:

- User Management
- Audit Log viewing
- Backup and Recovery
- Centralized application error logging and recovery
- TQM reliability analysis workflow
