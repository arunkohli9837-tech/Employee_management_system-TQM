### Error — Commit 14: Session Login

**Date:** 2026-09-05

**Error:** `KeyError: 'is_active'`

**Where:** `services/session.py` inside the `Session.login()` method.

**Cause:** The session implementation attempted to access `user["is_active"]`, but the user dictionary returned by the existing authentication service did not contain an `is_active` field.

**Impact:** Authentication completed, but the application raised an exception while creating the current-user session.

**Resolution:** Updated `Session.login()` to store only the user fields currently provided by the authentication service: `id`, `username`, and `role`.

**Verification:** Retested the login flow with the existing Admin account. Login completed successfully without the error.

**Status:** Resolved