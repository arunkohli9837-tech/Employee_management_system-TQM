### Error — Commit 14: Session Login

**Date:** 2026-09-05

**Error:** `KeyError: 'is_active'`

**Where:** `services/session.py` inside the `Session.login()` method.

**Cause:** The session implementation attempted to access `user["is_active"]`, but the user dictionary returned by the existing authentication service did not contain an `is_active` field.

**Impact:** Authentication completed, but the application raised an exception while creating the current-user session.

**Resolution:** Updated `Session.login()` to store only the user fields currently provided by the authentication service: `id`, `username`, and `role`.

**Verification:** Retested the login flow with the existing Admin account. Login completed successfully without the error.

**Status:** Resolved
### Error — Commit 29: Employee Management Navigation

**Date:** 2026-09-11

**Error:** `AttributeError: 'DashboardFrame' object has no attribute 'show_dashboard'`

**Where:** `ui/dashboard.py` inside the `open_employee_management()` method.

**Cause:**  
The Employee Management screen was being opened directly from `DashboardFrame`. The method attempted to pass `self.show_dashboard` as the callback for returning to the Dashboard, but the `DashboardFrame` class did not contain a `show_dashboard()` method.

**Impact:**  
Clicking the Employee Management button caused the application to raise an exception, and the Employee Management screen could not be opened correctly.

**Resolution:**  
The navigation responsibility was moved to `main.py`. The Dashboard now receives an `on_employee_management` callback from the main application. The Employee Management button calls this callback instead of the old `open_employee_management()` method.

The `open_employee_management()` method was removed from `DashboardFrame`. `main.py` now handles:
- Clearing the current screen.
- Opening the Employee Management screen.
- Returning to the Dashboard through the `on_back` callback.

The unused `EmployeeManagementFrame` import was also removed from `ui/dashboard.py`.

**Verification:**  
Retested the application after the changes. Login, Employee Management navigation, Back to Dashboard, and Logout worked successfully without the previous exception.

**Status:** Resolved