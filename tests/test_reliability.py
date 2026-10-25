"""Repeatable reliability tests using an isolated temporary SQLite database."""
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import database.database as db
import services.backup_service as backup
from services.audit_service import create_audit_log, get_all_audit_logs
from services.employee_service import (
    create_employee, deactivate_employee, get_all_employees,
    get_employee_by_id, search_employees, update_employee,
)
from services.validation_service import validate_employee_fields
from services.access_control import has_permission, require_permission
from services.error_handler import handle_exception
from services.hr_operations_service import create_payroll_record, get_payroll_records, create_performance_log, get_performance_logs


class ReliabilityTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.data_dir = self.root / "data"
        self.db_path = self.data_dir / "test.db"
        self.backup_dir = self.root / "backups"
        self._admin_user = None
        patches = [
            patch.object(db, "DATA_DIR", self.data_dir),
            patch.object(db, "DATABASE_PATH", self.db_path),
            patch.object(backup, "DATABASE_PATH", self.db_path),
            patch.object(backup, "BACKUP_DIR", self.backup_dir),
        ]
        for item in patches:
            item.start()
            self.addCleanup(item.stop)
        db.initialize_database()

    def tearDown(self):
        self.temp_dir.cleanup()

    def employee(self, **overrides):
        record = {
            "employee_code": "EMP-TEST-001",
            "full_name": "Test Employee",
            "email": "test.employee@example.com",
            "phone": "9876543210",
            "department": "IT",
            "designation": "Developer",
            "salary": 30000,
            "joining_date": "01-01-2025",
        }
        record.update(overrides)
        return record

    def add_employee(self, **overrides):
        return create_employee(**self.employee(**overrides), performed_by=self.create_admin())

    def test_failed_transaction_rolls_back(self):
        with self.assertRaises(RuntimeError):
            with db.transaction() as connection:
                connection.execute(
                    "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                    ("rollback_user", "test_hash", "Admin"),
                )
                raise RuntimeError("Simulated failure")
        connection = db.get_connection()
        try:
            count = connection.execute(
                "SELECT COUNT(*) FROM users WHERE username = ?", ("rollback_user",)
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(count, 0)

    def test_invalid_email_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_employee_fields(**self.employee(email="not-an-email"))

    def test_negative_salary_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_employee_fields(**self.employee(salary=-100))

    def test_duplicate_employee_code_is_rejected(self):
        self.add_employee()
        with self.assertRaises(sqlite3.IntegrityError):
            self.add_employee(email="another@example.com")
        self.assertEqual(len(get_all_employees()), 1)

    def test_backup_restore_recovers_previous_data(self):
        self.add_employee()
        backup_path = backup.create_backup()
        self.assertTrue(backup.validate_backup(backup_path))
        self.add_employee(employee_code="EMP-TEST-002", email="second@example.com")
        self.assertEqual(len(get_all_employees()), 2)
        safety_backup = backup.restore_backup(backup_path)
        self.assertTrue(safety_backup.exists())
        self.assertTrue(backup.validate_backup(safety_backup))
        self.assertEqual(len(get_all_employees()), 1)

    def test_corrupt_backup_is_rejected_without_changing_database(self):
        self.add_employee()
        corrupt = self.backup_dir / "corrupt.db"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        corrupt.write_text("not a database", encoding="utf-8")
        self.assertFalse(backup.validate_backup(corrupt))
        with self.assertRaises(ValueError):
            backup.restore_backup(corrupt)
        self.assertEqual(len(get_all_employees()), 1)

    def test_employee_create_read_search_update_deactivate(self):
        employee_id = self.add_employee()
        self.assertEqual(get_employee_by_id(employee_id)["employee_code"], "EMP-TEST-001")
        self.assertEqual(len(search_employees("Test Employee")), 1)
        updated = update_employee(
            employee_id, **self.employee(full_name="Updated Employee"), performed_by=self.create_admin()
        )
        self.assertTrue(updated)
        self.assertEqual(get_employee_by_id(employee_id)["full_name"], "Updated Employee")
        self.assertTrue(deactivate_employee(employee_id, performed_by=self.create_admin()))
        self.assertEqual(get_employee_by_id(employee_id)["status"], "Inactive")

    def test_audit_log_is_persisted_and_retrievable(self):
        create_audit_log(None, "test_user", "TEST_ACTION", "Employee", 1, "Test record", "Success")
        logs = get_all_audit_logs()
        self.assertTrue(any(log["action"] == "TEST_ACTION" for log in logs))


    def test_employee_mutations_require_authorized_actor(self):
        with self.assertRaises(PermissionError):
            create_employee(**self.employee())
        with self.assertRaises(PermissionError):
            create_employee(**self.employee(), performed_by={"id": 99, "username": "employee", "role": "Employee"})

    def test_role_permissions_deny_unauthorized_actions(self):
        employee_user = {"id": 2, "username": "employee", "role": "Employee"}
        self.assertFalse(has_permission(employee_user, "manage_users"))
        with self.assertRaises(PermissionError):
            require_permission(employee_user, "manage_users")


    def create_admin(self):
        if self._admin_user is not None:
            return self._admin_user
        with db.transaction() as connection:
            cursor = connection.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                ("admin_test", "test_hash", "Admin"),
            )
        self._admin_user = {"id": cursor.lastrowid, "username": "admin_test", "role": "Admin"}
        return self._admin_user

    def test_payroll_record_calculates_net_and_prevents_duplicate_period(self):
        employee_id = self.add_employee()
        admin = self.create_admin()
        create_payroll_record(employee_id, "2026-10", 1000, 500, admin)
        rows = get_payroll_records(admin)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][7], 29500.0)
        with self.assertRaises(sqlite3.IntegrityError):
            create_payroll_record(employee_id, "2026-10", 0, 0, admin)

    def test_performance_log_validation_and_persistence(self):
        employee_id = self.add_employee()
        admin = self.create_admin()
        create_performance_log(employee_id, "25-10-2026", 4, "Meets expectations", admin)
        rows = get_performance_logs(admin)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][4], 4)
        with self.assertRaises(ValueError):
            create_performance_log(employee_id, "25-10-2026", 6, "Invalid rating", admin)

    def test_hr_operations_are_forbidden_for_employee_role(self):
        employee_id = self.add_employee()
        employee_user = {"id": 2, "username": "employee", "role": "Employee"}
        with self.assertRaises(PermissionError):
            create_payroll_record(employee_id, "2026-10", 0, 0, employee_user)

    def test_error_handler_returns_safe_message_when_logging_fails(self):
        with patch("pathlib.Path.mkdir", side_effect=OSError("no access")):
            message = handle_exception("test", ValueError("example failure"))
        self.assertIn("Please try again", message)


if __name__ == "__main__":
    unittest.main(verbosity=2)
