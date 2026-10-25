# Employee Management System — User Manual

## 1. Purpose

This desktop application maintains employee records and provides user administration, audit-log review, and backup/recovery functions. The project quality focus is Q01 — Improve Reliability.

## 2. Install and start

Windows PowerShell, from the project root:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m scripts.create_admin  # first run only, if no user exists
python main.py
```

If `python` is not recognized, install Python 3 and select the option to add Python to PATH. Do not commit the `.venv` folder or the local SQLite database.

## 3. First login

Use the administrator credentials configured for your local development database. Do not guess credentials or put passwords in the README. On a fresh installation with no users, run `python -m scripts.create_admin` from the project root and follow the prompts. The script asks for a username and password and refuses to create a bootstrap administrator if any account already exists. Never put passwords in the README or commit them.

## 4. Employee management

1. Sign in with an account that has employee permissions.
2. Open **Employees** from the sidebar.
3. Enter the employee code, name, email, phone, department, designation, salary and joining date.
4. Save the record; required fields and formats are validated.
5. Use search to find a record, select it to update, and save the changes.
6. Use deactivation when an employee should no longer be active. Deactivation preserves the record rather than permanently deleting it.

Use fictional sample data for demonstrations.

## 5. User management

Only an administrator should see and use User Management. Assign only the role needed for the task. Passwords should be supplied through the application, never stored in plain text in a document.

## 6. Audit logs

Open **Audit Logs** to review recorded activities. Search by username, action, target or description, and use the status filter where available.

## 7. Backup and restore

1. Open **Backups** as an administrator.
2. Select **Create Backup** and confirm the backup appears in the list.
3. Validate/select the intended backup before restoring.
4. Restore replaces the active database with the selected backup; a safety copy is created first. Use a test database during demonstrations and never experiment on the only copy of important records.

Automatic backup is also attempted during application startup and logout. If the database is missing or inaccessible, review the user-facing message and application log.

## 8. Payroll and performance logs

Admin and HR users can open **Payroll & Performance** from the sidebar.

- Payroll: select an active employee, enter a pay period in `YYYY-MM`, deductions and bonus. Net salary is calculated from the employee's stored salary. Duplicate employee/pay-period records are rejected.
- Performance: select an employee, enter a review date in `DD-MM-YYYY`, choose a rating from 1 to 5 and add comments.
- Both actions are recorded in the audit log.

This is an academic demonstration workflow, not a statutory payroll engine. It does not calculate income tax, PF, ESI, overtime or other jurisdiction-specific payroll rules.

## 9. Run automated tests

```powershell
python -m compileall -q .
python -m unittest discover -s tests -v
```

## 10. Known limitations

Payroll and performance logging are basic academic workflows only. Statutory payroll calculations and advanced appraisal workflows are outside the current scope. Screenshots and measured results in the report must be captured from actual execution; do not fabricate evidence.
